# syntax=docker/dockerfile:1
FROM ubuntu:latest

# Set environment variable to prevent buffering of Python's standard output
ENV PYTHONUNBUFFERED=1

# Update package lists and install wget
RUN apt-get update && apt-get install -y  \
    wget  \
    netcat \
    fontconfig  \
    libfreetype6  \
    libx11-6  \
    libxext6  \
    libxrender1  \
    xfonts-75dpi  \
    xfonts-base \
    libjpeg-turbo8 \
    apt-utils  \
    vim  \
    curl  \
    apache2  \
    apache2-utils \
    python3  \
    libapache2-mod-wsgi-py3

# Download wkhtmltopdf
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
RUN dpkg -i wkhtmltox_0.12.6.1-2.jammy_amd64.deb
RUN ln -s /usr/local/bin/wkhtmltopdf /usr/bin
RUN ln -s /usr/local/bin/wkhtmltoimage /usr/bin

# Cleanup - remove the downloaded archive
RUN rm wkhtmltox_0.12.6.1-2.jammy_amd64.deb

# Create a symlink for Python 3 if it doesn't exist
RUN ln -s /usr/bin/python3 /usr/bin/python || true

RUN apt-get -y install python3-pip

# Create a symlink for pip3 to pip if it doesn't exist
RUN ln -s /usr/bin/pip3 /usr/bin/pip || true

#Clean up
RUN rm -rf /var/lib/apt/lists/*

# Upgrade pip inside the virtual environment
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
# Set the working directory
WORKDIR /var/www/html

# Copy your project files
COPY keta  .

# Permissions for temp files in the docker
RUN chmod 703 /var/www/html

# Copy Apache configuration
COPY site-config.conf /etc/apache2/sites-available/000-default.conf

#EXPOSE 8000

## Expose ports and start Apache
EXPOSE 80 3500
CMD ["apache2ctl", "-D", "FOREGROUND"]
