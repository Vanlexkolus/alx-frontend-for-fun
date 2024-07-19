#!/usr/bin/python3
"""
markdown2html.py - Converts a Markdown file to HTML,
supporting heading and ordered/unordered list syntax.

Usage:
    ./markdown2html.py README.md README.html

If the number of arguments is less than 2:
    print "Usage: ./markdown2html.py README.md README.html"
    to STDERR and exit with status 1.
If the Markdown file doesn’t exist:
    print "Missing <filename>" to STDERR and exit with status 1.
Otherwise, converts the Markdown file to HTML and writes it
to the output file.
"""

import sys
import os


def print_usage():
    """Prints the usage message to STDERR."""
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)


def print_missing(filename):
    """Prints a missing file message to STDERR."""
    print(f"Missing {filename}", file=sys.stderr)


def parse_markdown(md_content):
    """Parses Markdown content and converts it to HTML.

    Args:
        md_content (str): The content of the Markdown file.

    Returns:
        str: The converted HTML content.
    """
    html_lines = []
    in_unordered_list = False
    in_ordered_list = False

    for line in md_content.splitlines():
        line = line.strip()
        if line.startswith('#'):
            if in_unordered_list:
                html_lines.append('</ul>')
                in_unordered_list = False
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
            heading_level = len(line.split(' ')[0])
            heading_text = line[heading_level:].strip()
            html_line = f'<h{heading_level}>{heading_text}</h{heading_level}>'
            html_lines.append(html_line)
        elif line.startswith('-'):
            if not in_unordered_list:
                html_lines.append('<ul>')
                in_unordered_list = True
            list_item_text = line[1:].strip()
            html_line = f'<li>{list_item_text}</li>'
            html_lines.append(html_line)
        elif line.startswith('*'):
            if not in_ordered_list:
                html_lines.append('<ol>')
                in_ordered_list = True
            list_item_text = line[1:].strip()
            html_line = f'<li>{list_item_text}</li>'
            html_lines.append(html_line)
        else:
            if in_unordered_list:
                html_lines.append('</ul>')
                in_unordered_list = False
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
            html_lines.append(line)
    if in_unordered_list:
        html_lines.append('</ul>')
    if in_ordered_list:
        html_lines.append('</ol>')
    return '\n'.join(html_lines)


def markdown_to_html(md_filename, html_filename):
    """Converts a Markdown file to HTML and writes it to an output file.

    Args:
        md_filename (str): The input Markdown file name.
        html_filename (str): The output HTML file name.
    """
    with open(md_filename, 'r') as md_file:
        md_content = md_file.read()

    html_content = parse_markdown(md_content)

    with open(html_filename, 'w') as html_file:
        html_file.write(html_content)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    md_filename = sys.argv[1]
    html_filename = sys.argv[2]

    if not os.path.exists(md_filename):
        print_missing(md_filename)
        sys.exit(1)

    markdown_to_html(md_filename, html_filename)
    sys.exit(0)
