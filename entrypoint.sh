#!/bin/bash
echo "Waiting for MySQL..."
while ! python -c "import pymysql; pymysql.connect(host='db', user='root', password='root', database='iris_db')" 2>/dev/null; do
  echo "MySQL not ready - waiting 2 seconds..."
  sleep 2
done
echo "MySQL is ready!"
python manage.py migrate
python manage.py runserver 0.0.0.0:8000