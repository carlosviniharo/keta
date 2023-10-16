FROM python:3.11-slim-buster

ENV PYTHONBUFFERED=1

RUN apt-get update \
    && apt-get install -y \
        curl \
        libxrender1 \
        libjpeg62-turbo \
        fontconfig \
        libxtst6 \
        xfonts-75dpi \
        xfonts-base \
        xz-utils
RUN curl "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb" -L -o "wkhtmltopdf.deb"

RUN dpkg -i wkhtmltopdf.deb

#RUN wget https://s3.amazonaws.com/shopify-managemant-app/wkhtmltopdf-0.9.9-static-amd64.tar.bz2
#RUN tar xvjf wkhtmltopdf-0.9.9-static-amd64.tar.bz2
#RUN mv wkhtmltopdf-amd64 /usr/local/bin/wkhtmltopdf
#RUN chmod +x /usr/local/bin/wkhtmltopdf

WORKDIR /keta
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD python manage.py runserver 0.0.0.0:8000





