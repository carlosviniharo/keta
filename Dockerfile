# syntax=docker/dockerfile:1
# Stage 1: Build environment
FROM ubuntu:latest AS builder

# Update package lists and install required packages
RUN apt-get update && apt-get install -y \
    wget \
    netcat-openbsd \
    fontconfig \
    libfreetype6 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    xfonts-75dpi \
    xfonts-base \
    libjpeg-turbo8 \
    apt-utils \
    vim \
    curl \
    apache2 \
    apache2-utils \
    python3 \
    python3-venv \
    libapache2-mod-wsgi-py3 \
    cron  # Install cron

# Download and install wkhtmltopdf
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb && \
    dpkg -i wkhtmltox_0.12.6.1-2.jammy_amd64.deb && \
    ln -s /usr/local/bin/wkhtmltopdf /usr/bin && \
    ln -s /usr/local/bin/wkhtmltoimage /usr/bin && \
    rm wkhtmltox_0.12.6.1-2.jammy_amd64.deb

# Install Python dependencies
RUN apt-get -y install python3-pip

# Copy requirements.txt
COPY requirements.txt requirements.txt

# Create and activate a virtual environment, then install dependencies
RUN python3 -m venv /venv

RUN /bin/bash -c "source venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt"

# Stage 2: Production environment
FROM ubuntu:latest

# Set environment variable to prevent buffering of Python's standard output
ENV PYTHONUNBUFFERED=1

# Copy all dependencies from the builder stage
COPY --from=builder / /

# Set the working directory
WORKDIR /var/www/html

# Copy your project files
COPY keta .

# Permissions for temp files in the docker
RUN chmod 703 /var/www/html

# Copy Apache configuration
COPY site-config.conf /etc/apache2/sites-available/000-default.conf

# Copy the cron job file into the container
COPY django-cron /etc/cron.d/django-cron

# Set permissions for the cron job file
RUN chmod 0777 /etc/cron.d/django-cron

# Apply the cron job
RUN crontab /etc/cron.d/django-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Expose ports
EXPOSE 80 3500
CMD ["apache2ctl", "-D", "FOREGROUND"]