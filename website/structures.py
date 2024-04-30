import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class Article:
    id: int
    title: str
    body: str
    tags: str

@dataclass 
class ArticleVisit:
    id: int 
    user_id: int
    article_id: int

@dataclass
class BookingPrice:
    id: int
    type: str
    price: int
    max_per_day: int

@dataclass
class Booking:
    id: int
    price_id: int
    time: datetime.date
    user_id: int

@dataclass
class User:
    id: int
    name: str
    password: str
    email: str
    admin: bool