#!/bin/sh

SOURCE_DIR="${SOURCE_DIR:-/var/lib/source}"
TARGET_DIR="${TARGET_DIR:-/var/lib/target}"

cd $SOURCE_DIR || exit 1

# using find to search for directory and execute the bash commands
find . -type f -iname '*.pdf' -exec bash -c '
	basename=$(basename "$0" .pdf)
	target_file="$TARGET_DIR/$basename.pdf"
	if [ ! -f $target_file ]; then
		echo "Processing $basename.pdf to $target_file"
		pkgx ocrmypdf "$basename.pdf" "$target_file"
		echo "Processed $basename.pdf"
	fi

' {} \;
