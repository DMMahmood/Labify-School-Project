import unittest
from main import *

class TestMain(unittest.TestCase):
    def setUp(self):
        # Set up the test database
        self.connection = sql.connect(':memory:')
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Users (UserID TEXT, Password TEXT, DateOfSetup TEXT, Admin TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Experiments (ExperimentID TEXT, Equipment TEXT, Date TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS SignIO (Date TEXT, UserID TEXT, SignInTime TEXT, SignOutTime TEXT, TotalTime TEXT)")

    def tearDown(self):
        # Close the test database connection
        self.connection.close()

    def test_userIDGen(self):
        # Test the userIDGen function
        user_id = userIDGen()
        self.assertEqual(len(user_id), 7)  # User ID should be 7 characters long

    def test_experimentIDGen(self):
        # Test the experimentIDGen function
        experiment_id = experimentIDGen()
        self.assertEqual(len(experiment_id), 10)  # Experiment ID should be 10 characters long

    def test_createUser(self):
        # Test the createUser function
        username = createUser("password123", 1)
        self.assertIsNotNone(username)  # User should be created successfully

    def test_createExperiment(self):
        # Test the createExperiment function
        createExperiment("Equipment 1")
        rows = self.cursor.execute("SELECT * FROM Experiments").fetchall()
        self.assertEqual(len(rows), 1)  # One experiment should be created

    def test_showAllUsers(self):
        # Test the showAllUsers function
        rows = showAllUsers()
        self.assertEqual(len(rows), 0)  # No users should be in the database initially

    def test_searchUserID(self):
        # Test the searchUserID function
        row = searchUserID("1234abcd")
        self.assertIsNone(row)  # No user should be found initially

    def test_searchExperimentID(self):
        # Test the searchExperimentID function
        row = searchExperimentID("abcdefghij")
        self.assertIsNone(row)  # No experiment should be found initially

    def test_searchUserAdmin(self):
        # Test the searchUserAdmin function
        row = searchUserAdmin(1)
        self.assertIsNone(row)  # No admin user should be found initially

    def test_searchExperimentDate(self):
        # Test the searchExperimentDate function
        row = searchExperimentDate("2022-01-01")
        self.assertIsNone(row)  # No experiment should be found initially

    def test_deleteUser(self):
        # Test the deleteUser function
        deleteUser(1, "1234abcd")
        rows = self.cursor.execute("SELECT * FROM Users").fetchall()
        self.assertEqual(len(rows), 0)  # No users should be in the database after deletion

    def test_deleteExperiment(self):
        # Test the deleteExperiment function
        deleteExperiment(1, "abcdefghij")
        rows = self.cursor.execute("SELECT * FROM Experiments").fetchall()
        self.assertEqual(len(rows), 0)  # No experiments should be in the database after deletion

if __name__ == '__main__':
    unittest.main()