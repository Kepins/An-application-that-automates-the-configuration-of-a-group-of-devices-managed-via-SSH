#!/bin/bash

celery -A config worker --loglevel=INFO
