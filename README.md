# gitler
Gitler - Line endings resolver for git.

gitler will help safely you to solve the git problem about line endings in different operating system (especially Windows).

All implementation is referenced by this [document](https://help.github.com/articles/dealing-with-line-endings/).

### Usage
```
python gitler.py [-h] [-c] [-s] [-o]

optional arguments:
  -h, --help            show this help message and exit
  -c , --config-only
                        Confiture git and generate(or modify) ".gitattributes" only.
  -s , --stash
                        Stash all current contents before start. (Default=True)
  -o , --overwrite-attr 
                        Overwrite .gitattributes. (Default=False - "Append")
```                        

### How to run
- set 'git config core.autocrlf' to true
- Automatically generates .gitattributes based on real file formats('text' or 'binary')
- Fix and clean your exists git repo safely.
- Commit resolved changes.

An generation example of .gitattributes
```
* text=auto

*.sketch binary
*.ipa binary
*.gz binary
*.jpg binary
*.7z binary
*.orig binary
*.zip binary
*.zxp binary
*.swp binary
*.psd binary
*.ase binary
*.png binary
*.a binary
*.idx binary
*.aco binary
*.eps binary
*.pdf binary
*.caf binary
*.pack binary
*.ai text
*.lock text
*.xcscheme text
*.sample text
*.modulemap text
*.xcworkspacedata text
*.txt text
*.xml text
*.xib text
*.pbxproj text
*.py text
*.json text
*.plist text
*.pch text
*.html text
*.stackdump text
*.m text
*.js text
*.jsx text
*.svg text
*.strings text
*.sh text
*.h text
*.aia text
```
