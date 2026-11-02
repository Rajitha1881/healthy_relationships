# ==============================================================================
# Unit Test Suite for Relationship Messages
# ==============================================================================

# 'unittest' is Python's built-in testing framework inspired by JUnit.
# It allows us to define test cases, run assertions, and detect regressions automatically.
import unittest

# Import the functions and data dictionary we want to test from relationship_messages.py
from relationship_messages import get_relationship_message, get_categories, MESSAGES


# ==============================================================================
# Test Case Class
# ==============================================================================
# A test class inherits from 'unittest.TestCase'.
# Any method inside this class whose name starts with 'test_' is executed as a test.
class TestRelationshipMessages(unittest.TestCase):

    def test_get_random_message(self):
        """
        Verify that calling get_relationship_message() with no arguments
        returns a non-empty string.
        """
        # Call the function without arguments
        message = get_relationship_message()

        # Check 1: Ensure the return type is a string
        self.assertIsInstance(message, str)

        # Check 2: Ensure the returned string is not empty (length > 0)
        self.assertGreater(len(message), 0)

    def test_get_categorized_message(self):
        """
        Verify that requesting a message for every valid category
        returns a message that belongs to that exact category list.
        """
        # Loop through each valid category key ('communication', 'growth', etc.)
        for category in MESSAGES.keys():
            # Get a message for that category
            message = get_relationship_message(category)

            # Ensure the returned message is present in that category's list
            self.assertIn(message, MESSAGES[category])

    def test_case_insensitive_category(self):
        """
        Verify that category matching works regardless of uppercase/lowercase input.
        """
        # Pass uppercase "COMMUNICATION"
        message = get_relationship_message("COMMUNICATION")

        # The result should still match the lowercase 'communication' category list
        self.assertIn(message, MESSAGES["communication"])

    def test_invalid_category_raises_error(self):
        """
        Verify that passing a non-existent category raises a ValueError.
        """
        # 'assertRaises(ValueError)' asserts that the code inside this context block
        # will trigger a ValueError exception. If it does not, the test fails.
        with self.assertRaises(ValueError):
            get_relationship_message("invalid_category_name")

    def test_get_categories(self):
        """
        Verify that get_categories() returns all available category keys as a list.
        """
        # Retrieve the category list
        categories = get_categories()

        # Ensure the returned list matches the keys of the MESSAGES dictionary
        self.assertEqual(categories, list(MESSAGES.keys()))


# ==============================================================================
# Test Runner Entry Point
# ==============================================================================
# If this file is run directly (python3 test_relationship_messages.py),
# unittest.main() discovers and executes all 'test_*' methods in this module.
if __name__ == "__main__":
    unittest.main()
