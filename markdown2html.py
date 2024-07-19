#!/usr/bin/python3
"""
This is necessary to pass pep8 checker
"""


import sys
import os
import markdown


def print_usage():
    """Prints the usage message."""
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)


def print_missing(filename):
    """Prints the missing file message."""
    print(f"Missing {filename}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    md_filename = sys.argv[1]
    html_filename = sys.argv[2]

    if not os.path.exists(md_filename):
        print_missing(md_filename)
        sys.exit(1)

    with open(md_filename, 'r') as md_file:
        md_content = md_file.read()

    html_content = markdown.markdown(md_content)

    with open(html_filename, 'w') as html_file:
        html_file.write(html_content)

    sys.exit(0)
