FROM docker.io/jbarlow83/ocrmypdf-alpine
COPY script.sh ./
CMD [ "./script.sh" ]
