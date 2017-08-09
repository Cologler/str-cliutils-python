# str.toolkits.cologler

str operator for command line.

`str.py` handle all input as single text, `mstr.py` handle each line from input as single text.

## import

before use, put [py.jasily.cologler](https://github.com/Cologler/py.jasily.cologler) into your python path.

this script need import cmd framework from `py.jasily.cologler`.

## sub cmds

sub cmd|desc|input|output
:---|:---|:---|:---
len|get len of str from source|`echo abc|str len`|`4` (`echo` endswith `\n`)
skip|skip number of char from source|`echo abc|str skip 1`|`bc`
take|take number of char from source|`echo abc|str take 1`|`a`
replace||`echo abc|str replace a 1`|`1bc`
upper|to upper case|`echo abc|str upper`|`ABC`
lower|to lower case|`echo ABC|str lower`|`abc`
index-of|find index of value from source|`echo ABC|str index-of B`|`1`
split|split value by spliter|`echo ABC|str split B`|`A\nC`
join|join lines by spliter|`echo ABC|str split B|strm join D`|`ADCD`

For more function, try to type `str` and read the usage.
