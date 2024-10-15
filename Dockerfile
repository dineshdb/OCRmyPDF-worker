FROM docker.io/jbarlow83/ocrmypdf-alpine
RUN pip install pdfplumber; apk add file
RUN mkdir -p /var/lib/source /var/lib/target
COPY . .
ENTRYPOINT [ "/bin/sh" ]
CMD [ "./scripts/script.sh" ]
