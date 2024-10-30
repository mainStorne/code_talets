#!/bin/bash

echo "Применение миграций"
alembic upgrade head

exec "$@"