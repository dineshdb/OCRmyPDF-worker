#!/bin/sh

# Fallback to environment variables or default values if not set via command line
SOURCE_DIR="${SOURCE_DIR:-/var/lib/source}"
TARGET_DIR="${TARGET_DIR:-/var/lib/target}"

echo "Watching $SOURCE_DIR -> $TARGET_DIR"

# using find to search for directory and execute the sh commands
find "$SOURCE_DIR" -type f -iname '*.pdf' -exec sh -c '
	basename=$(basename "$0" .pdf)
	source_pdf="$SOURCE_DIR/$basename.pdf"

	echo "PDF2Text: Processing $source_pdf"
	python scripts/pdf2text.py \
		--pdfplumber \
		--pdfminer \
		-s "$SOURCE_DIR" \
		-t "$TARGET_DIR" \
		"$basename.pdf"
' {} \;
