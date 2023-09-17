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

Remember to use same secrets after migrating your application. Since fields are encrypted using
**FIELD_ENCRYPTION_KEY** you need to use same value in the new environment.

### Export
1. Stop running application
2. Run this command
```
docker run --rm -v ssh-configurator_postgres_data:/data -v .:/export ubuntu tar czf /export/dump_$(date +"%Y-%m-%d_%H_%M_%S").tar.gz -C /data .
```
3. Dump will be created in your current working directory.

### Import
1. Stop running application.
2. Make sure Docker volume ssh-configurator_postgres_data exists.
3. Run this command
```
docker run --rm -v ssh-configurator_postgres_data:/data -v .:/import ubuntu tar xzf /import/{DUMP_NAME} -C /data
```