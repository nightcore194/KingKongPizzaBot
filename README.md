# DB

-----

Driver - MySQL <br>
ORM - SQLAlchemy <br>
Migrations - alembic


## Migrations

------

MAKE MIGRATIONS IN *bot*
> <code>
> alembic init migrations <br>
> alembic revision --autogenerate -m 'your message' <br> 
> alembic upgrade heads
> </code>

## ORM

----

all models is mapped in bot/models.py

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