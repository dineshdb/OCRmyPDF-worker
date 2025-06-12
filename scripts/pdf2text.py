#!/usr/bin/env -S uv run
# -*- coding: utf-8 -*-

# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "pdfminer.six",
# ]
# ///

import argparse
import os
import pathlib
import subprocess
from pdfminer.high_level import extract_text as extract_text_pdfminer


def is_pdf_file(file_path: str) -> bool:
    try:
        file_type_check = subprocess.run(
            ["file", "-b", "--mime-type", file_path],
            check=True,
            capture_output=True,
            text=True,
        )
        file_type = file_type_check.stdout.strip()
        if file_type != "application/pdf":
            print(f"Error: Input file '{file_path}' is not a PDF but {file_type}.")
            return False
        return True
    except subprocess.CalledProcessError:
        print(f"Error: Unable to determine file type of '{file_path}'.")
        return False


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract text from PDF files using different methods."
    )
    parser.add_argument("input_file", help="Input PDF file")
    parser.add_argument(
        "-s",
        "--source",
        dest="source_dir",
        default=os.environ.get("SOURCE_DIR", os.getcwd()),
        help="Source directory (default: current directory or SOURCE_DIR env var)",
    )
    parser.add_argument(
        "-t",
        "--target",
        dest="target_dir",
        default=os.environ.get("TARGET_DIR", os.getcwd()),
        help="Target directory (default: current directory or TARGET_DIR env var)",
    )
    parser.add_argument(
        "--pdfminer",
        action="store_true",
        help="Use pdfminer.six engine for text extraction",
    )
    parser.add_argument(
        "--ocr", action="store_true", help="Enable OCR processing (default: False)"
    )

    args = parser.parse_args()

    if not args.pdfminer:
        print(
            "Error: The engine (--pdfminer) must be selected."
        )
        parser.print_help()
        exit(1)

    return args


def validate_input_file(input_file_path: str) -> None:
    if not os.path.exists(input_file_path):
        print(f"Error: Input file '{input_file_path}' does not exist.")
        exit(1)
    if not is_pdf_file(input_file_path):
        print(f"Error: The input file '{input_file_path}' is not a valid PDF file.")
        exit(1)


def process_ocr(args: argparse.Namespace, input_file_path: str, base_name: str) -> str:
    file_to_process = input_file_path
    if args.ocr:
        base_file_name = base_name.split('.pdf')[0] if '.pdf' in base_name else base_name
        ocr_file = os.path.join(args.target_dir, f"{base_file_name}.tesseract.pdf")
        txt_file = os.path.join(args.target_dir, f"{base_file_name}.tesseract.txt")
        regenerate = False
        if not os.path.exists(ocr_file):
            regenerate = True
        else:
            source_mtime = os.path.getmtime(input_file_path)
            ocr_mtime = os.path.getmtime(ocr_file)
            if source_mtime > ocr_mtime:
                regenerate = True
            else:
                print(f"Skipping OCR: '{ocr_file}' is up to date.")

        if regenerate:
            ocr_command = [
                "ocrmypdf",
                "--skip-text",
                "--rotate-pages",
                "--deskew",
                "--clean",
                "--sidecar",
                txt_file,
                "-l=eng+deu",
                input_file_path,
                ocr_file,
            ]
            try:
                result = subprocess.run(
                    ocr_command,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                print(f"OCRed: '{input_file_path}' to '{ocr_file}'.")
            except subprocess.CalledProcessError as e:
                print(f"Error during OCR processing: {e.stderr}")
                exit(1)
        file_to_process = ocr_file
    else:
        print("OCR: disabled. Using original file for text extraction.")

    return file_to_process


"""
extract_text_with_engine - Extract text using the specified engine if output doesn't exist.
:param engine_name: Name of the engine (pdfplumber or pdfminer).
:param engine_func: Function to call for text extraction.
:param file_to_process: Path to the file to extract text from.
:param output_file: Path to the output file.
:return: None
"""


def extract_text_with_engine(
    engine_name: str, engine_func, file_to_process: str, output_file: str
) -> None:
    regenerate = False
    if not os.path.exists(output_file):
        regenerate = True
    else:
        source_mtime = os.path.getmtime(file_to_process)
        output_mtime = os.path.getmtime(output_file)
        if source_mtime > output_mtime:
            regenerate = True
        else:
            print(f"Skipping {engine_name}: '{output_file}' is up to date.")

    if regenerate:
        text = engine_func(file_to_process)
        with open(output_file, "w+", encoding="utf-8") as file:
            file.write(text)
        print(f"Text extraction completed using {engine_name} to '{output_file}'.")


def main() -> None:
    args = parse_arguments()

    input_file_path = (
        os.path.join(args.source_dir, args.input_file)
        if not os.path.isabs(args.input_file)
        else args.input_file
    )
    validate_input_file(input_file_path)

    base_name = os.path.basename(args.input_file)
    base_file_name = base_name.split('.pdf')[0] if '.pdf' in base_name else base_name
    # Ensure target directory exists
    pathlib.Path(args.target_dir).mkdir(parents=True, exist_ok=True)
    file_to_process = process_ocr(args, input_file_path, base_name)

    # Extract text using selected engine
    if args.pdfminer:
        output_file = os.path.join(args.target_dir, f"{base_file_name}.pdfminer.txt")
        extract_text_with_engine(
            "pdfminer", extract_text_pdfminer, file_to_process, output_file
        )


if __name__ == "__main__":
    main()
