import datetime
import json

from sqlalchemy import create_engine
from sqlalchemy import String, Integer, ForeignKey, Text, Date, Boolean, DateTime, ARRAY, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship, scoped_session, sessionmaker, DeclarativeBase

from typing import List
from settings.settings import *

""" 
DO NOT FORGET TO PASTE YOUR OWN DB URI IN config.json 
ALSO SET IT UP IN alembic.ini, varibale - sqlalchemy.url
"""

# for mysql using pymysql

config = json.load(open(CONFIG_FILE))

engine = create_engine(f'{config["db"]["driver"]}://{config["db"]["username"]}:{config["db"]["password"]}'
                       f'@{config["db"]["ip"]}:{config["db"]["port"]}/{config["db"]["name"]}', pool_recycle=3600,
                       pool_pre_ping=True)

db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine))


class Base(DeclarativeBase):
    pass


class Campaign(Base):
    __tablename__ = "Campaign"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(String(30), nullable=True)
    phone: Mapped[str] = mapped_column(String(12), nullable=True)
    owner_name: Mapped[str] = mapped_column(String(25), nullable=True)

    def __str__(self):
        return self.name


class Employee(Base):
    __tablename__ = "Employee"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=True)  # IMPROVEMENT FOR TG
    campaign_id: Mapped[int] = mapped_column(ForeignKey("Campaign.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(25), nullable=True)
    phone: Mapped[str] = mapped_column(String(12), nullable=True)
    role: Mapped[str] = mapped_column(String(30), nullable=True)  # ADMIN OR COOKING

    def __str__(self):
        return self.name


class Client(Base):
    __tablename__ = "Client"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=True)  # IMPROVEMENT FOR TG
    name: Mapped[str] = mapped_column(String(25), nullable=True)
    phone: Mapped[str] = mapped_column(String(12), nullable=True)

    def __str__(self):
        return self.name


class Food(Base):
    __tablename__ = "Food"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("Recipe.id"), nullable=True)

    def __str__(self):
        return self.name

class Recipe(Base):
    __tablename__ = "Recipe"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[float] = mapped_column(Float, nullable=True)

    food: Mapped["Food"] = mapped_column()

    def __str__(self):
        return f'Рецепт {self.food.name}'


class Order(Base):
    __tablename__ = "Order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("Client.id"), nullable=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("Employee.id"), nullable=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("Food.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    type: Mapped[str] = mapped_column(String(30), nullable=True)  # DROPOFF OR DELIVERY
    date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now())
    price: Mapped[float] = mapped_column(Float, nullable=True)
    address: Mapped[str] = mapped_column(String(30), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="Created")
    deliver_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    def __str__(self):
        return f'{self.date.strftime("%d.%m.%Y %H:%M:%S")} {self.name}'
