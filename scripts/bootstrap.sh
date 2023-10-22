#!/usr/bin/env bash
set -eo pipefail

cd /srv/root

if [ -z "$APP_ENV" ]; then
  echo "Please set APP_ENV"
  exit 1
fi

if [ -z "$APP_COMPONENT" ]; then
  echo "Please set APP_COMPONENT"
  exit 1
fi

if [[ $PULL_SECRETS_FROM_VAULT -eq 1 ]]; then
  echo "Installing akatsuki-cli"
  pip install --index-url $PYPI_INDEX_URL akatsuki-cli
  echo "Installed akatsuki-cli"

  echo "Fetching secrets from vault"
  akatsuki vault get profile-history-service $APP_ENV -o .env
  echo "Fetched secrets from vault"
  source .env
  echo "Sourced secrets from vault"
fi

# await database availability
/scripts/await-service.sh $READ_DB_HOST $READ_DB_PORT $SERVICE_READINESS_TIMEOUT
/scripts/await-service.sh $WRITE_DB_HOST $WRITE_DB_PORT $SERVICE_READINESS_TIMEOUT

# await redis availability
/scripts/await-service.sh $REDIS_HOST $REDIS_PORT $SERVICE_READINESS_TIMEOUT

if [[ $APP_COMPONENT == "api" ]]; then
    exec /scripts/run-api.sh
else
  echo "Unknown APP_COMPONENT: $APP_COMPONENT"
  exit 1
fi
