# An-application-that-automates-the-configuration-of-a-group-of-devices-managed-via-SSH

## Prerequisites
- Docker

## Running production
1. Download `production.yml` file.
2. Create `.env` file based on `.env.example`. There are two sections the _REQUIRED_
and _OPTIONAL - FOR ADVANCED CONFIGURATION_. As the name suggest you need to set only
the required part as the optionals are defaults in app settings. Please do it **thoughtfully** 
as your app security depends on it.
3. Run docker compose up command
```
docker compose -f=production.yml up --detach
```

## Exporting/importing application state

### Export
```
docker run --rm -v ssh-configurator_postgres_data:/data -v .:/export ubuntu tar czf /export/dump_$(date +"%Y-%m-%d_%H_%M_%S").tar.gz -C /data .
```

### Import
```
docker run --rm -v ssh-configurator_postgres_data:/data -v .:/import ubuntu tar xzf /import/{DUMP_NAME} -C /data
```