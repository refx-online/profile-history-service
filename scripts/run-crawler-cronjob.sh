#!/usr/bin/env bash
set -eo pipefail

exec python3 -m app.workers.cronjobs.crawler
