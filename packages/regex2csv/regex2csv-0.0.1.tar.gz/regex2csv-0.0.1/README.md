# regex2csv

This script is a python utility that matches the capture groups of a defined regex within a file and puts it into csv format for easy viewing.

Author: @marcolongol

Input: `regex2csv.py <regex> <file>`

Output: csv format of the regex capture groups consisting of the line number, capture group name, and the capture group value for each line in the file

Example:

`python regex2csv.py "(?P<word1>\w+):(?P<word2>\w+)" "test.txt"`

Example Output:

```txt
line,word1,word2
1,hello,world
2,foo,bar
3,foo,bar
```
