# An-application-that-automates-the-configuration-of-a-group-of-devices-managed-via-SSH

## Prerequisites
- Docker

## Installation
1. Clone the project into your workspace
```
git clone git@github.com:Kepins/An-application-that-automates-the-configuration-of-a-group-of-devices-managed-via-SSH.git
```

2. Create .env file based on .env.example and set your variables
3. Run migrations
```
docker-compose run django python manage.py migrate
```
4. Create superuser
```
docker-compose run django python manage.py createsuperuser
```
5. Run docker compose
```
docker compose up
```