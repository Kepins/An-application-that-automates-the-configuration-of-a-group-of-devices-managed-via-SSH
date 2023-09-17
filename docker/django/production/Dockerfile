# Pull base image
FROM python:3.11.4-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings.production


# Create a directory to hold application code
RUN mkdir -p /home/django/code

# Set work directory
WORKDIR /home/django/code

# Install dependencies
COPY requirements requirements
RUN pip install -r requirements/production.txt

# Copy project
COPY . .

# Make startup scripts runnable
RUN find docker/django/production/scripts -type f -exec chmod +x {} \;

# Create a non-root user to run the application
RUN useradd -ms /bin/bash django

# Give ownership of the home directory to the django user
RUN chown -R django /home/django

# Switch to the django user
USER django