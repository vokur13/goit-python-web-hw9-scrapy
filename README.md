# goit-python-web-hw9-scrapy

Скраппинг сайта выполнен на фреймворке Scrapy, запускается в модуле main.py

В задание добавлен пакет db из предыдущего домашнего задания, для наполения базы данных запустить скрипт в модуле seeds.py.
Для подключения базы данных (MongoDB) в корне проекта необходим файл config.ini со следущей конфигурацией:

[DB]
USER=<db_user>
PASSWORD=<db_password>
DB_DOMAIN=<db_domain>
DB_NAME=<db_name>
