# Pull base image
FROM python:3.11.4-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings.local

COPY ./docker/django/local/start.sh /start.sh
RUN chmod +x /start.sh

# Create non-root user
RUN useradd -ms /bin/bash django
USER django

# Set work directory
WORKDIR /home/django/app

# Set work directory
WORKDIR /diploma/app

# Install dependencies
COPY requirements requirements
RUN pip install -r requirements/local.txt


# Copy project
COPY . .

EXPOSE 8000

ENTRYPOINT ["/start.sh"]
