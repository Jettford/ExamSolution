import unittest

from database import db

class DatabaseWrapperTestCase(unittest.TestCase):
    def setUp(self):
        db.reset_database()
        db.push_test_data()

    def test_user_grabbing(self):
        self.assertTrue(len(db.get_all_users()) > 0)

    def test_grabbing_test_user(self):
        self.assertEqual(db.get_user_by_id(1).name, "John")

    def test_article_grabbing(self):
        self.assertTrue(len(db.get_all_articles()) > 0)

    def test_grabbing_test_article(self):
        self.assertEqual(db.get_article_by_id(1).title, "Head to the Zoo")

    def test_booking_grabbing(self):
        self.assertTrue(len(db.get_all_bookings()) > 0)

    def test_grabbing_test_booking(self):
        self.assertEqual(db.get_booking_by_id(1).user_id, 1)

    def test_booking_price_grabbing(self):
        self.assertTrue(len(db.get_all_booking_prices()) > 0)

    def test_grabbing_test_booking_price(self):
        self.assertEqual(db.get_booking_price_by_id(1).price, 100)

    def test_article_visit_grabbing(self):
        self.assertTrue(len(db.get_all_article_visits()) > 0)

    def test_grabbing_test_article_visit(self):
        self.assertEqual(db.get_article_visit_by_id(1).article_id, 1)
