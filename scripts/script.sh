#!/bin/sh

# Parse command line options
OPTIONS=$(getopt -o s:t:h -l source:,target:,help -- "$@")
if [ $? -ne 0 ]; then
  echo "Error: Invalid option or missing argument" >&2
  echo "Usage: $0 [-s|--source source_dir] [-t|--target target_dir] [-h|--help]" >&2
  exit 1
fi

eval set -- "$OPTIONS"
while true; do
  case "$1" in
    -s|--source) SOURCE_DIR="$2"; shift 2 ;;
    -t|--target) TARGET_DIR="$2"; shift 2 ;;
    -h|--help) echo "Usage: $0 [-s|--source source_dir] [-t|--target target_dir] [-h|--help]" >&2
               echo "  -s, --source: Set source directory (default: /var/lib/source or SOURCE_DIR env var)" >&2
               echo "  -t, --target: Set target directory (default: /var/lib/target or TARGET_DIR env var)" >&2
               echo "  -h, --help: Show this help message" >&2
               exit 0 ;;
    --) shift; break ;;
    *) echo "Invalid option: $1" >&2; exit 1 ;;
  esac
done

# Fallback to environment variables or default values if not set via command line
SOURCE_DIR="${SOURCE_DIR:-/var/lib/source}"
TARGET_DIR="${TARGET_DIR:-/var/lib/target}"
ENABLE_PDF_TO_TEXT="${ENABLE_PDF_TO_TEXT:-false}"

echo "Watching $SOURCE_DIR -> $TARGET_DIR"

# using find to search for directory and execute the sh commands
find "$SOURCE_DIR" -type f -iname '*.pdf' -exec sh -c '
	basename=$(basename "$0" .pdf)
	source_pdf="$SOURCE_DIR/$basename.pdf"
	target_pdf="$TARGET_DIR/$basename.pdf"
	target_txt="$TARGET_DIR/$basename.txt"
	echo "Found $basename.pdf"

	file_type=$(file -b --mime-type "$source_pdf")
	if [ "$file_type" != "application/pdf" ]; then
		echo "Skipping $source_pdf ($file_type, not a PDF)"
		exit 1
	fi

	if [ ! -f $target_pdf ]; then
		echo "OCR: Processing $source_pdf"
		ocrmypdf --skip-text "$source_pdf" "$target_pdf"
	fi

	## pdf2text
	if [ "$ENABLE_PDF_TO_TEXT" = true ]; then
		if [ ! -f $target_txt ]; then
			echo "PDF2Text: Processing $target_pdf"
			python scripts/pdf2text.py pdfplumber "$target_pdf" "$target_txt"
		fi
	fi
' {} \;
