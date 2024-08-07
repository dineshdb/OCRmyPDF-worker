#!/bin/sh

SOURCE_DIR="${SOURCE_DIR:-/var/lib/source}"
TARGET_DIR="${TARGET_DIR:-/var/lib/target}"

cd $SOURCE_DIR || exit 1

echo "Watching $SOURCE_DIR for new PDF files..."

# using find to search for directory and execute the bash commands
find . -type f -iname '*.pdf' -exec bash -c '
	basename=$(basename "$0" .pdf)
	target_file="$TARGET_DIR/$basename.pdf"
	echo "Found $target_file"
	if [ ! -f $target_file ]; then
		echo "Processing $basename.pdf to $target_file"
		ocrmypdf "$basename.pdf" "$target_file"
		echo "Processed $basename.pdf"
	fi

' {} \;
