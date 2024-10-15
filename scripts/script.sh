#!/bin/sh

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
			python scripts/pdf2text.py "$target_pdf" "$target_txt"
		fi
	fi
' {} \;
