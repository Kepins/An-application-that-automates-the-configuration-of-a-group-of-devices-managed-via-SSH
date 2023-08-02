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
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

