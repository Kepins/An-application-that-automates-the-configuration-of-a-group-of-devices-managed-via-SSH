# Pull base image
FROM python:3.11.4-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./docker/django/local/start.sh /start.sh
RUN chmod +x /start.sh

# Create non-root user
RUN useradd -ms /bin/bash django
USER django

# Set work directory
WORKDIR /home/django/code

# Install dependencies
COPY requirements requirements
RUN pip install -r requirements/local.txt


# Copy project
COPY . .







