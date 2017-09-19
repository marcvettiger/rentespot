FROM python:2.7-slim


ADD requirements.txt /

RUN pip install -r requirements.txt

ADD . /

CMD [ "python", "networkLoadTest.py" ]
