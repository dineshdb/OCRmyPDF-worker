#!/usr/bin/env -S uv run
# -*- coding: utf-8 -*-

# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "pdfplumber",
# ]
# ///

"""
This script is used to extract the full text from a PDF file.
It uses the pdfplumber library to read the PDF file and extract the text from each page.
The extracted text is then returned as a string.
"""

import pdfplumber
import argparse

"""
get_full_text Get full text from a pdf file using pdfplumber.
:param file: The path to the PDF file.
:return: The full text extracted from the PDF file.
:rtype: str
"""


def get_full_text(file: str) -> str:
    full_text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text()
    return full_text


parser = argparse.ArgumentParser(description="Extract text from PDF files using different methods.")
subparsers = parser.add_subparsers(dest="command", help="Subcommand to execute")

# Subcommand for pdfplumber
pdfplumber_parser = subparsers.add_parser("pdfplumber", help="Extract text using pdfplumber")
pdfplumber_parser.add_argument("input_file", help="Input PDF file")
pdfplumber_parser.add_argument("output_file", help="Output text file")

args = parser.parse_args()

if args.command == "pdfplumber":
    text = get_full_text(args.input_file)
    # Open the file in write mode
    with open(args.output_file, "w+", encoding="utf-8") as file:
        file.write(text)
else:
    parser.print_help()
    exit(1)
