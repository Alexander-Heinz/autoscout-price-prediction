#!/bin/bash

export PROJECT_NAME=mage_modeling 
export MAGE_CODE_PATH=/home/src 
export SMTP_EMAIL=$SMTP_EMAIL 
export SMTP_PASSWORD=$SMTP_PASSWORD 
docker compose up
