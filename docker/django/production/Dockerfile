# Pull base image
FROM python:3.11.4-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create non-root user
RUN useradd -ms /bin/bash django
USER django

# Set work directory
WORKDIR /home/django/code

# Install dependencies
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt


# Copy project
COPY ../../.. .

CMD ["python", "manage.py", "migrate", "--settings=config.settings.production"]
CMD ["python", "manage.py", "runserver", "--settings=config.settings.production"]

