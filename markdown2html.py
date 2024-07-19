#!/usr/bin/python3
"""
markdown2html.py - Converts a Markdown file to HTML, supporting heading,
ordered/unordered list, paragraph, and bold syntax.

Usage:
    ./markdown2html.py README.md README.html

If the number of arguments is less than 2:
    print "Usage: ./markdown2html.py README.md README.html" to STDERR
    and exit with status 1.
If the Markdown file doesn’t exist:
    print "Missing <filename>" to STDERR and exit with status 1.
Otherwise, converts the Markdown file to HTML and writes it to the output file.
"""

import sys
import os
import re


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
    paragraph_lines = []

    def close_paragraph():
        """Helper function to close a paragraph and add it to html_lines."""
        if paragraph_lines:
            html_lines.append("<p>")
            html_lines.append("<br/>".join(paragraph_lines))
            html_lines.append("</p>")
            paragraph_lines.clear()

    def apply_text_styles(text):
        """Apply text styles for bold and italic."""
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)
        return text

    for line in md_content.splitlines():
        line = line.strip()
        line = apply_text_styles(line)
        if line.startswith('#'):
            close_paragraph()
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
            close_paragraph()
            if not in_unordered_list:
                html_lines.append('<ul>')
                in_unordered_list = True
            list_item_text = line[1:].strip()
            html_line = f'<li>{list_item_text}</li>'
            html_lines.append(html_line)
        elif line.startswith('*'):
            close_paragraph()
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
            if line:  # If the line is not empty
                paragraph_lines.append(line)
            else:  # Empty line indicates the end of a paragraph
                close_paragraph()

    # Close any open paragraph, unordered list,
    # or ordered list at the end of the file
    close_paragraph()
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
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    md_filename = sys.argv[1]
    html_filename = sys.argv[2]

    if not os.path.exists(md_filename):
        print_missing(md_filename)
        sys.exit(1)

    markdown_to_html(md_filename, html_filename)
    sys.exit(0)
