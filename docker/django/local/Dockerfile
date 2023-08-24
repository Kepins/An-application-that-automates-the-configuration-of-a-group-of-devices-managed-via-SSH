# Pull base image
FROM python:3.11.4-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings.local

# Copy startup scripts
COPY ./docker/django/local/scripts /scripts
# Make startup scripts runnable
RUN find /scripts -type f -exec chmod +x {} \;


# Set work directory
WORKDIR /diploma/app

# Install dependencies
COPY requirements requirements
RUN pip install -r requirements/local.txt


# Copy project
COPY . .
