# DB

-----

Driver - MySQL <br>
ORM - SQLAlchemy <br>
Migrations - alembic <br>
Telegram bot - aiogram 3 <br>


## Migrations

------

https://habr.com/ru/articles/585228/ <br>
MAKE MIGRATIONS IN *bot*
> <code>
> alembic init migrations <br>
> alembic revision --autogenerate -m 'your message' <br> 
> alembic upgrade heads
> </code>

## ORM

----

all models is mapped in models.py

# BOT

----

Bot is based on webhook, deployment on wsgi/gunicorn<br> 
if you dont need an backend http server, then run from *bot/__init__.py*, function run()

## Run

----

Run local, from python env of project: <br>
<code>
python -c "from bot import run; run()"
</code><br>
Run env: <br>
1. Unix-like os - <code>source *your_venv*/bin/activate</code>
2. Windows - <code>*your_venv*/Scripts/activate</code>

Second type of running - run file <code>long_pool.py</code>