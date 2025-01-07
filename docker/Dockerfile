FROM python:3.13

WORKDIR app

COPY requirements/  requirements/

RUN pip install --upgrade pip & pip install -r requirements/base.txt

COPY ./  /app

CMD ["python","main.py"]