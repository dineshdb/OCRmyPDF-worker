FROM docker.io/jbarlow83/ocrmypdf-alpine
COPY script.sh ./
ENTRYPOINT [ "/bin/sh" ]
CMD [ "./script.sh" ]
