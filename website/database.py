import re
import mariadb

from typing import List, Optional

from config import config
from structures import *

class Database:
    def __init__(self):
        self.db = mariadb.connect(
            host = config.get("DATABASE_URI"),
            user = config.get("DATABASE_USER"),
            password = config.get("DATABASE_PASSWORD"),
            database = config.get("DATABASE_NAME")
        )

    def cursor(self) -> mariadb.Cursor:
        """
        Generates a cursor for the database connection

        Returns:
            mariadb.Cursor: Cursor object for the database connection
        """
        
        return self.db.cursor(
            buffered = True, 
            dictionary = True,
        )
    
    def commit(self) -> None:
        """
        Commits the current transaction to the database
        """
        
        self.db.commit()
    
    def get_user_by_id(self, id: int) -> Optional[User]:
        """
        Gets a user by their ID

        Args:
            id (int): The ID of the user to get

        Returns:
            Optional[User]: The user object if found, None otherwise
        """
        
        cur = self.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?;", (id,))
        
        res = cur.fetchone()
        
        if not res:
            return None

        return User(**res)
    
    def get_all_users(self) -> Optional[List[User]]:
        """
        Gets all users from the database

        Returns:
            Optional[List[User]]: A list of all users in the database
        """
        
        cur = self.cursor()
        cur.execute("SELECT * FROM users;")

        return [User(**user) for user in cur.fetchall()]
    
    def get_user_by_name(self, name: str) -> Optional[User]:
        """
        Gets a user by their name

        Args:
            name (str): The name of the user to get

        Returns:
            Optional[User]: The user object if found, None otherwise
        """
        
        cur = self.cursor()
        cur.execute("SELECT * FROM users WHERE name = ?;", (name,))

        res = cur.fetchone()
        
        if not res:
            return None

        return User(**res)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Gets a user by their email

        Args:
            email (str): The email of the user to get

        Returns:
            Optional[User]: The user object if found, None otherwise
        """
        
        cur = self.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?;", (email,))

        res = cur.fetchone()
        
        if not res:
            return None

        return User(**res)
    
    def create_user(self, user: User):
        """
        Creates a user in the database, and sets the ID of the passed in user object

        Args:
            user (User): The user object to create
        """
        
        cur = self.cursor()
        cur.execute("INSERT INTO users (name, password, email) VALUES (?, ?, ?);", (user.name, user.password, user.email))

        self.commit()

        user.id = cur.lastrowid

    def get_article_by_id(self, id: int) -> Optional[Article]:
        """
        Gets an article by its ID

        Args:
            id (int): The ID of the article to get

        Returns:
            Optional[Article]: The article object if found, None otherwise
        """
        
        cur = self.cursor()
        cur.execute("SELECT * FROM articles WHERE id = ?;", (id,))

        res = cur.fetchone()
        
        if not res:
            return None

        return Article(**res)
    
    def get_all_articles(self) -> Optional[List[Article]]:
        """
        Gets all articles from the database

        Returns:
            Optional[List[Article]]: A list of all articles in the database
        """
        
        cur = self.cursor()
        cur.execute("SELECT * FROM articles;")

        return [Article(**article) for article in cur.fetchall()]

    def delete_article(self, id: int) -> None:
        """
        Deletes an article from the database

        Args:
            id (int): The ID of the article to delete
        """
        
        cur = self.cursor()
        cur.execute("DELETE FROM articles WHERE id = ?;", (id,))

        self.commit()

    def update_article(self, article: Article) -> None:
        """
        Updates an article in the database

        Args:
            article (Article): The article object to update
        """
        
        cur = self.cursor()
        cur.execute("UPDATE articles SET title = ?, body = ?, tags = ? WHERE id = ?;", (article.title, article.body, article.tags, article.id))

        self.commit()

    def create_article(self, article: Article) -> None:
        """
        Creates an article in the database, and sets the ID of the passed in article object

        Args:
            article (Article): The article object to create
        """
        
        cur = self.cursor()
        cur.execute("INSERT INTO articles (title, body, tags) VALUES (?, ?, ?);", (article.title, article.body, article.tags))

        self.commit()

        article.id = cur.lastrowid

    def get_booking_by_id(self, id: int) -> Optional[Booking]:
        """
        Gets a booking by its ID

        Args:
            id (int): The ID of the booking to get

        Returns:
            Optional[Booking]: The booking object if found, None otherwise
        """
        
        cur = self.cursor()
        cur.execute("SELECT * FROM bookings WHERE id = ?;", (id,))

        res = cur.fetchone()
        
        if not res:
            return None

        return Booking(**res)
    
    def get_booking_by_user(self, user_id: int) -> Optional[List[Booking]]:
        """
        Gets all bookings by a user

        Args:
            user_id (int): The ID of the user to get bookings for

        Returns:
            Optional[List[Booking]]: A list of all bookings for the user
        """
        
        cur = self.cursor()
        cur.execute("SELECT * FROM bookings WHERE user_id = ?;", (user_id,))

        return [Booking(**booking) for booking in cur.fetchall()]
    
    def get_all_bookings(self) -> Optional[List[Booking]]:
        """
        Gets all bookings from the database

        Returns:
            Optional[List[Booking]]: A list of all bookings in the database
        """
        
        cur = self.cursor()
        cur.execute("SELECT * FROM bookings;")

        return [Booking(**booking) for booking in cur.fetchall()]
    
    def get_all_bookings_on_date(self, date: datetime.datetime) -> Optional[List[Booking]]:
        """
        Gets all bookings on a given date

        Args:
            date (datetime): The date you want the bookings for

        Returns:
            Optional[List[Booking]]: A list of all the bookings present in the database for that date. 
        """
            
        cur = self.cursor()
        cur.execute("SELECT * FROM bookings WHERE time = ?;", (date.strftime("%Y-%m-%d"),))

        return [Booking(**booking) for booking in cur.fetchall()]
    
    def get_booking_price_by_id(self, id: int) -> Optional[BookingPrice]:
        """
        Gets a booking price by its ID

        Args:
            id (int): The ID of the booking price to get

        Returns:
            Optional[BookingPrice]: The booking price object if found, None otherwise
        """
        
        cur = self.cursor()
        cur.execute("SELECT * FROM booking_prices WHERE id = ?;", (id,))

        res = cur.fetchone()
        
        if not res:
            return None

        return BookingPrice(**res)
    
    def create_booking(self, booking: Booking) -> None:
        """
        Creates a booking in the database, and sets the ID of the passed in booking object

        Args:
            booking (Booking): The booking object to create
        """
        
        cur = self.cursor()
        cur.execute("INSERT INTO bookings (price_id, time, user_id) VALUES (?, ?, ?);", (booking.price_id, booking.time, booking.user_id))

        self.commit()

        booking.id = cur.lastrowid
    
    def delete_booking(self, booking: Booking) -> None:
        """
        Deletes a booking from the database

        Args:
            booking (Booking): The booking object to delete
        """
        
        cur = self.cursor()
        cur.execute("DELETE FROM bookings WHERE id = ?;", (booking.id,))

        self.commit()

    def get_all_booking_prices(self) -> Optional[List[BookingPrice]]:
        """
        Gets all booking prices from the database

        Returns:
            Optional[List[BookingPrice]]: A list of all booking prices in the database
        """
        
        cur = self.cursor()
        cur.execute("SELECT * FROM booking_prices;")

        return [BookingPrice(**booking_price) for booking_price in cur.fetchall()]
    
    def get_booking_prices_available(self, date: str) -> Optional[List[BookingPrice]]:
        """
        Gets all booking prices available for a given date

        Args:
            date (str): The date to get booking prices for, in the format YYYY-MM-DD

        Returns:
            Optional[List[BookingPrice]]: A list of all booking prices available for the date
        """
        
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date): # yeah, i know this doesn't quite actually check the date but it's good enough 
            return None
        
        dateObject = datetime.datetime.strptime(date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        
        if dateObject < datetime.datetime.now():
            return None

        prices = self.get_all_booking_prices()
        bookings = self.get_all_bookings()
        
        def get_count_of_booking_on_day(price_id: int) -> int:
            result = 0 
            for booking in bookings:
                # compare days
                if booking.time.strftime("%Y-%m-%d") == date and booking.price_id == price_id:
                    result += 1
        
            return result
        
        prices = [price for price in prices if get_count_of_booking_on_day(price.id) < price.max_per_day]

        for price in prices:
            price.max_per_day -= get_count_of_booking_on_day(price.id)
        
        return prices
    
    def get_article_visit_by_id(self, id: int) -> Optional[ArticleVisit]:
        """
        Gets an article visit by its ID

        Args:
            id (int): The ID of the article visit to get

        Returns:
            Optional[ArticleVisit]: The article visit object if found, None otherwise
        """
        
        cur = self.cursor()
        cur.execute("SELECT * FROM article_visits WHERE id = ?;", (id,))

        res = cur.fetchone()
        
        if not res:
            return None

        return ArticleVisit(**res)
    
    def get_all_article_visits(self) -> Optional[List[ArticleVisit]]:
        """
        Gets all article visits from the database

        Returns:
            Optional[List[ArticleVisit]]: A list of all article visits in the database
        """
        
        cur = self.cursor()
        cur.execute("SELECT * FROM article_visits;")

        return [ArticleVisit(**article_visit) for article_visit in cur.fetchall()]
    
    def get_all_article_visits_on_article(self, article_id: int) -> Optional[List[ArticleVisit]]:
        """
        Gets all article visits on an article

        Args:
            article_id (int): The ID of the article to get visits for

        Returns:
            Optional[List[ArticleVisit]]: A list of all article visits for the article
        """
        
        cur = self.cursor()
        cur.execute("SELECT * FROM article_visits WHERE article_id = ?;", (article_id,))
        
        return [ArticleVisit(**article_visit) for article_visit in cur.fetchall()]
    
    def log_article_visit(self, article_visit: ArticleVisit) -> None:
        """
        Logs an article visit in the database

        Args:
            article_visit (ArticleVisit): The article visit object to log
        """
        
        cur = self.cursor()
        cur.execute("INSERT INTO article_visits (user_id, article_id) VALUES (?, ?);", (article_visit.user_id, article_visit.article_id))

        self.commit()

        article_visit.id = cur.lastrowid

    def reset_database(self) -> None:
        """
        Resets the database to its base state
        """
        
        cur = db.cursor()

        cur.execute("DROP TABLE IF EXISTS article_visits;")
        cur.execute("DROP TABLE IF EXISTS bookings;")

        cur.execute("DROP TABLE IF EXISTS users;")
        cur.execute("DROP TABLE IF EXISTS articles;")
        cur.execute("DROP TABLE IF EXISTS booking_prices;")

        db.commit()

        with open(config.data_path + "/migrations/01_initial.sql") as f:
            for statement in f.read().split(";"):
                try:
                    cur.execute(statement)
                except:
                    pass

        db.commit()

    def push_test_data(self) -> None:
        """
        Pushes test data to the database
        """
        cur = db.cursor()

        with open(config.data_path + "/migrations/test.sql") as f:
            for statement in f.read().split(";"):
                try:
                    cur.execute(statement)
                except:
                    pass

        db.commit()

db = Database()