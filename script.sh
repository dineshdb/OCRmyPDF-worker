#!/bin/sh

SOURCE_DIR="${SOURCE_DIR:-/var/lib/source}"
TARGET_DIR="${TARGET_DIR:-/var/lib/target}"

cd $SOURCE_DIR || exit 1

# using find to search for directory and execute the bash commands
find . -type f -iname '*.pdf' -exec bash -c '
	basename=$(basename "$0" .pdf)

	echo "Processing $basename.pdf"

	ocrmypdf "$basename.pdf" "$basename.ocr.pdf"
	mv "$basename.ocr.pdf" "$TARGET_DIR/$basename.pdf"

	echo "Processed $basename.pdf"
' {} \;
