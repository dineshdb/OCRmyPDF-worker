FROM docker.io/jbarlow83/ocrmypdf-alpine
RUN pip install pdfplumber pdfminer.six; apk add file tesseract-ocr-data-deu
RUN mkdir -p /var/lib/source /var/lib/target
COPY . .
ENTRYPOINT [ "/bin/sh" ]
CMD [ "./scripts/script.sh" ]
