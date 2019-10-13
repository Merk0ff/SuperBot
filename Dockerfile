FROM python:3
ADD SRC /
ADD requirements.txt /
RUN pip install -r requirements.txt
CMD [ "python", "./src/main.py user" ]
CMD tail -f /dev/null