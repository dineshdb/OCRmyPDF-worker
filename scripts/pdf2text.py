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

"""
is_pdf_file - Check if the given file is a PDF.
:param file_path: The path to the file to check.
:return: True if the file is a PDF, False otherwise.
:rtype: bool
"""
def is_pdf_file(file_path: str) -> bool:
    import subprocess
    try:
        file_type_check = subprocess.run(["file", "-b", "--mime-type", file_path], check=True, capture_output=True, text=True)
        file_type = file_type_check.stdout.strip()
        if file_type != "application/pdf":
            print(f"Error: Input file '{file_path}' is not a PDF (detected type: {file_type}).")
            return False
        return True
    except subprocess.CalledProcessError:
        print(f"Error: Unable to determine file type of '{file_path}'.")
        return False


parser = argparse.ArgumentParser(description="Extract text from PDF files using different methods.")
parser.add_argument("input_file", help="Input PDF file")
parser.add_argument("-s", "--source", dest="source_dir", default=os.environ.get("SOURCE_DIR", os.getcwd()), help="Source directory (default: current directory or SOURCE_DIR env var)")
parser.add_argument("-t", "--target", dest="target_dir", default=os.environ.get("TARGET_DIR", os.getcwd()), help="Target directory (default: current directory or TARGET_DIR env var)")
parser.add_argument("--pdfplumber", action="store_true", help="Use pdfplumber engine for text extraction")
parser.add_argument("--pdfminer", action="store_true", help="Use pdfminer.six engine for text extraction")
parser.add_argument("--ocr", action="store_true", help="Enable OCR processing (default: False)")

args = parser.parse_args()

if not args.pdfplumber and not args.pdfminer:
    print("Error: At least one engine (--pdfplumber or --pdfminer) must be selected.")
    parser.print_help()
    exit(1)

input_file_path = os.path.join(args.source_dir, args.input_file) if not os.path.isabs(args.input_file) else args.input_file
# Check if the input file exists
if not os.path.exists(input_file_path):
    print(f"Error: Input file '{input_file_path}' does not exist.")
    exit(1)
# Check if the input file is a PDF
if not is_pdf_file(input_file_path):
    print(f"Error: The input file '{input_file_path}' is not a valid PDF file.")
    exit(1)

base_name = os.path.basename(args.input_file)
ocr_file = os.path.join(args.target_dir, f"{base_name}.ocr.pdf")
# Ensure target directory exists
pathlib.Path(args.target_dir).mkdir(parents=True, exist_ok=True)
# Run Tesseract OCR via ocrmypdf to generate OCRed PDF only if it doesn't already exist and if OCR is enabled
import subprocess
file_to_process = input_file_path
if args.ocr:
    if not os.path.exists(ocr_file):
        ocr_command = ["ocrmypdf", "--skip-text", input_file_path, ocr_file]
        subprocess.run(ocr_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"OCR processing completed for '{input_file_path}' to '{ocr_file}'.")
    else:
        print(f"Skipping OCR: '{ocr_file}' already exists.")
    file_to_process = ocr_file
else:
    print("OCR processing disabled. Using original file for text extraction.")

# Use the selected file for text extraction with selected engines, skipping if output already exists
if args.pdfplumber:
    output_file = os.path.join(args.target_dir, f"{base_name}.pdfplumber.txt")
    if not os.path.exists(output_file):
        text = get_full_text(file_to_process)
        # Open the file in write mode
        with open(output_file, "w+", encoding="utf-8") as file:
            file.write(text)
        print(f"Text extraction completed using pdfplumber to '{output_file}'.")
    else:
        print(f"Skipping pdfplumber: '{output_file}' already exists")

if args.pdfminer:
    output_file = os.path.join(args.target_dir, f"{base_name}.pdfminer.txt")
    if not os.path.exists(output_file):
        text = get_full_text_pdfminer(file_to_process)
        # Open the file in write mode
        with open(output_file, "w+", encoding="utf-8") as file:
            file.write(text)
        print(f"Text extraction completed using pdfminer to '{output_file}'.")
    else:
        print(f"Skipping pdfminer: '{output_file}' already exists")
