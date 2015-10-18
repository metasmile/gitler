"""
Line endings resolver for git

Copyright (c) 2015 metasmile cyrano905@gmail.com (github.com/metasmile)
"""

import time, os, sys, re, textwrap, argparse, pprint, subprocess
from os.path import expanduser

parser = argparse.ArgumentParser(description='Line endings resolver for git.')
parser.add_argument('-c','--config-only', help='Confiture git and generate(or modify) ".gitattributes" only.', required=False, default=False, nargs='?')
parser.add_argument('-s','--stash', help='Stash all current contents before start.(Default=True)', required=False, default=True, nargs='?')
parser.add_argument('-o','--overwrite-attr', help='Overwrite .gitattributes.(Default=False - "Append")', required=False, default=False, nargs='?')
args = vars(parser.parse_args())

def main():
    start = time.time()

    perform_stash = args['stash'] is not False
    performed_stash = False
    if perform_stash:
        performed_stash = subprocess.call('git stash', shell=True)==0

    print '> Configure git ...'
    resolve_global()

    print '> Configure .gitattributes ...'
    print write_attributes(make_attributes())

    if args['config_only'] is False:
        print '> Now commit working content safely and clean ...'
        resolve_current_repo()

    print 'done.', (time.time() - start)
    print '(i) : Your uncommited changes is been stashed safely.\nPlease excute "git stash pop" to restore.'

def check_ignore(file):
    return not os.path.isfile(file) or 1 > os.path.getsize(file)

def resolve_global():
    subprocess.check_call('git config --global core.autocrlf true', shell=True)

def resolve_current_repo():
    subprocess.call('git add . -u', shell=True)
    subprocess.call('git commit -m "Saving files before refreshing line endings"', shell=True)
    subprocess.call('git rm --cached -r .', shell=True)
    subprocess.call('git reset --hard', shell=True)
    subprocess.call('git add .', shell=True)
    subprocess.call('git commit -m "Normalize all the line endings (configured .gitattributes)"', shell=True)

# references from : https://help.github.com/articles/dealing-with-line-endings/
def make_attributes():
    exts = {}
    for dir, dirs, files in os.walk(expanduser('./'), topdown=True):
        for file in files:
            _file = os.path.join(dir, file)
            if not check_ignore(_file):
                try:
                    ext = os.path.splitext(file)[1][1:]
                    if ext and not ext in exts:
                        exts[ext] = 'text' if istextfile(open(_file)) else 'binary'
                except IOError, e:
                    continue

    #pre-defines
    result = textwrap.dedent(
        """\
        * text=auto

        """)
    #configure gitattributes by extension
    for ext in sorted(exts, key=exts.get):
        result += textwrap.dedent(
            """\
            *.{0} {1}
            """\
        .format(ext, exts[ext]))

    return result

def write_attributes(content):
    path = os.path.join(expanduser('./'), '.gitattributes')
    f = open(path, 'a' if args['overwrite_attr'] is False else 'w')
    f.write(content)
    f.close()
    return content

'''
http://eli.thegreenplace.net/2011/10/19/perls-guess-if-file-is-text-or-binary-implemented-in-python

# A function that takes an integer in the 8-bit range and returns
# a single-character byte object in py3 / a single-character string
# in py2.
'''
PY3 = sys.version_info[0] == 3

int2byte = (lambda x: bytes((x,))) if PY3 else chr

_text_characters = (
        b''.join(int2byte(i) for i in range(32, 127)) +
        b'\n\r\t\f\b')

def istextfile(fileobj, blocksize=512):
    """ Uses heuristics to guess whether the given file is text or binary,
        by reading a single block of bytes from the file.
        If more than 30% of the chars in the block are non-text, or there
        are NUL ('\x00') bytes in the block, assume this is a binary file.
    """
    block = fileobj.read(blocksize)
    if b'\x00' in block:
        # Files with null bytes are binary
        return False
    elif not block:
        # An empty file is considered a valid text file
        return True

    # Use translate's 'deletechars' argument to efficiently remove all
    # occurrences of _text_characters from the block
    nontext = block.translate(None, _text_characters)
    return float(len(nontext)) / len(block) <= 0.30

if __name__ == "__main__":
    main()
