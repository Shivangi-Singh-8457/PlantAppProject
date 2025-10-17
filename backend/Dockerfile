FROM python:3.10.10

EXPOSE 5000

WORKDIR /backend

COPY requirements.txt /backend
RUN pip install -r requirements.txt
COPY . /backend

CMD python app.py