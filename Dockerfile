FROM docker.io/jbarlow83/ocrmypdf-alpine
RUN apk add file tesseract-ocr-data-deu tesseract-ocr-data-osd py3-pdfminer
RUN mkdir -p /var/lib/source /var/lib/target
COPY . .
ENTRYPOINT [ "/bin/sh" ]
CMD [ "./scripts/script.sh" ]
