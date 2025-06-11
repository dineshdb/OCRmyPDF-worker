#!/usr/bin/env -S uv run
# -*- coding: utf-8 -*-

# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "pdfplumber",
#   "pdfminer.six",
# ]
# ///

"""
This script is used to extract the full text from a PDF file.
It uses the pdfplumber library to read the PDF file and extract the text from each page.
The extracted text is then returned as a string.
"""

import pdfplumber
import argparse
import os
import pathlib

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


"""
get_full_text_pdfminer - Get full text from a pdf file using pdfminer.six.
:param file: The path to the PDF file.
:return: The full text extracted from the PDF file.
:rtype: str
"""
def get_full_text_pdfminer(file: str) -> str:
    from pdfminer.high_level import extract_text
    return extract_text(file)


parser = argparse.ArgumentParser(description="Extract text from PDF files using different methods.")
parser.add_argument("input_file", help="Input PDF file")
parser.add_argument("-s", "--source", dest="source_dir", default=os.environ.get("SOURCE_DIR", os.getcwd()), help="Source directory (default: current directory or SOURCE_DIR env var)")
parser.add_argument("-t", "--target", dest="target_dir", default=os.environ.get("TARGET_DIR", os.getcwd()), help="Target directory (default: current directory or TARGET_DIR env var)")
parser.add_argument("--pdfplumber", action="store_true", help="Use pdfplumber engine for text extraction")
parser.add_argument("--pdfminer", action="store_true", help="Use pdfminer.six engine for text extraction")

args = parser.parse_args()

if not args.pdfplumber and not args.pdfminer:
    print("Error: At least one engine (--pdfplumber or --pdfminer) must be selected.")
    parser.print_help()
    exit(1)

input_file_path = os.path.join(args.source_dir, args.input_file) if not os.path.isabs(args.input_file) else args.input_file
base_name = os.path.basename(args.input_file)
ocr_file = os.path.join(args.target_dir, f"{base_name}.ocr.pdf")
# Ensure target directory exists
pathlib.Path(args.target_dir).mkdir(parents=True, exist_ok=True)
# Run Tesseract OCR via ocrmypdf to generate OCRed PDF
import subprocess
ocr_command = ["ocrmypdf", "--skip-text", input_file_path, ocr_file]
subprocess.run(ocr_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Use the OCRed file for text extraction with selected engines
if args.pdfplumber:
    text = get_full_text(ocr_file)
    output_file = os.path.join(args.target_dir, f"{base_name}.pdfplumber.txt")
    # Open the file in write mode
    with open(output_file, "w+", encoding="utf-8") as file:
        file.write(text)

if args.pdfminer:
    text = get_full_text_pdfminer(ocr_file)
    output_file = os.path.join(args.target_dir, f"{base_name}.pdfminer.txt")
    # Open the file in write mode
    with open(output_file, "w+", encoding="utf-8") as file:
        file.write(text)
