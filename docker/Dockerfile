FROM python:3.13

WORKDIR app

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    && apt-get clean



COPY requirements/  requirements/

RUN pip install --upgrade pip & pip install -r requirements/base.txt

COPY ./  /app

CMD ["python","main.py"]
