import fire
import unittest

from database import db

from config import config

class DatabaseCli:
    def setup(self, pushTestData=False):
        """
        Sets up the database and optionally pushes test data.

        Args:
            pushTestData (bool, optional): Whether to fill the database with test information. Defaults to False.
        """

        print("Setting up database...")

        db.reset_database()

        if pushTestData:
            db.push_test_data()

        print("Database setup complete.")
        
    def run(self):
        """
        Runs the flask app in a development server
        """

        from app import app

        app.run("localhost", 5000, debug=config.get("DEBUG"))
        
    def test(self):
        """
        Runs the tests
        """
        
        testLoader = unittest.TestLoader()

        discovered = testLoader.discover("./website/tests/", "*_tests.py")

        testSuite = unittest.TestSuite(discovered)
        unittest.TextTestRunner(verbosity=2).run(testSuite)

if __name__ == "__main__":
    fire.Fire(DatabaseCli)