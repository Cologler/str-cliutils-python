# str.toolkits.cologler

str operator for command line.

`str.py` handle all input as single text, `mstr.py` handle each line from input as single text.

## import

before use, put [py.jasily.cologler](https://github.com/Cologler/py.jasily.cologler) into your python path.

this script need import cmd framework from `py.jasily.cologler`.

## sub cmds

sub cmd|description|input|output
:---|:---|:---|:---
skip|skip number of char in input|`echo abc|str skip 1`|`bc`
take|take number of char in input|`echo abc|str take 1`|`a`
