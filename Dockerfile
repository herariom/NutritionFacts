FROM python:3.7-stretch

WORKDIR /python-docker

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get install build-essential make gcc -y \
    && apt-get install dpkg-dev libgl1 tesseract-ocr -y \
    && pip install -r requirements.txt

COPY . .

# ENV DATABASE_URI NULL
# ENV S3_ACCESS_KEY NULL
# ENV S3_SECRET_KEY NULL
# ENV S3_BUCKET NULL
# ENV TESSDATA_PREFIX NULL


CMD gunicorn app:app --bind 0.0.0.0:8000