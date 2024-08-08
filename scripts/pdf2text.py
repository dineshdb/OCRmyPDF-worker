#!/bin/env python3
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


parser = argparse.ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("output_file")
args = parser.parse_args()

text = get_full_text(args.input_file)

# Open the file in write mode
with open(args.output_file, "w+", encoding="utf-8") as file:
    file.write(text)
