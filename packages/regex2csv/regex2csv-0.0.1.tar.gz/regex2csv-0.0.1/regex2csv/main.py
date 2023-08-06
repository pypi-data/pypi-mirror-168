# This script is a python utility that matches the capture groups of a defined regex within a file and puts it into csv format for easy viewing.
# Author: @marcolongol
# Input: regex2csv.py <regex> <string>
# Output: csv format of the regex capture groups consisting of the line number, capture group name, and the capture group value for each line in the file
# Example: python regex2csv.py "(?P<word1>\w+):(?P<word2>\w+)" "test.txt"
# Example Output:
# line,word1,word2
# 1,hello,world
# 2,foo,bar
# 3,foo,bar

import argparse
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser(
        description=(
            "This script is a python utility that matches the capture groups of a"
            " defined regex within a file and puts it into csv format for easy viewing."
        )
    )
    parser.add_argument(
        "regex", help="The regex to be used to match the capture groups"
    )
    parser.add_argument("file", help="The file to be used to match the regex")
    args = parser.parse_args()

    regex = args.regex
    file = args.file

    regex2csv(regex, file)


def regex2csv(regex, file):
    # Check if the file exists
    if not Path(file).is_file():
        print("The file does not exist")
        exit()

    # Check if the regex is valid
    try:
        regex = re.compile(regex)
    except re.error:
        print("The regex is invalid")
        exit()

    # Open the file and read the lines
    with open(file, "r") as f:
        lines = f.readlines()

    # Match the regex to the lines and get the capture groups
    matches = []
    for i, line in enumerate(lines):
        match = regex.search(line)
        if match:
            matches.append(match.groupdict())

    # Get the capture group names
    capture_group_names = []
    for match in matches:
        for key in match:
            if key not in capture_group_names:
                capture_group_names.append(key)

    # Print the csv header
    print("line," + ",".join(capture_group_names))

    # Print the csv rows
    for i, match in enumerate(matches):
        print(str(i + 1) + "," + ",".join([match[key] for key in capture_group_names]))


if __name__ == "__main__":
    main()
