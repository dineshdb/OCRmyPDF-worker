# README

## Getting Started

A worker container that scans all the files in `$SOURCE_DIR` and moves them to
`$TARGET_DIR` after making them OCR compatible using `OCRmyPDF`.

## Environment variables

- `SOURCE_DIR`: `/var/lib/source`
- `TARGET_DIR`: `/var/lib/target`
- `ENABLE_PDF_TO_TEXT`: `false`

## License

MIT
