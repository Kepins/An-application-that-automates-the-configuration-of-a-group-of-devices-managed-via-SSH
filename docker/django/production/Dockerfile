# Pull base image
FROM python:3.11.4-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings.production

# Copy startup scripts
COPY ./docker/django/production/scripts /scripts
# Make startup scripts runnable
RUN find /scripts -type f -exec chmod +x {} \;

# Create non-root user
#RUN useradd -ms /bin/bash django
#USER django

# Set work directory
WORKDIR /diploma/app

# Install dependencies
COPY requirements requirements
RUN pip install -r requirements/production.txt

# Copy project
COPY . .
