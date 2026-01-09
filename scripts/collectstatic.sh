#!/bin/sh

echo '🔵 Executando collectstatis.sh'
python manage.py collectstatic --noinput
