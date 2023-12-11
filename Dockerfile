FROM python:3.11-alpine
WORKDIR /webapp
COPY requirements.txt /webapp
RUN pip install -r requirements.txt --no-cache-dir
COPY ./webapp /webapp
CMD python app.py