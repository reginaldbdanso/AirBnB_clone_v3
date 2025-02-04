#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pycodestyle as pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}
# models.storage_t = "db"
os.putenv("HBNB_TYPE_STORAGE", "db")
os.putenv("HBNB_MYSQL_USER", "hbnb_test")
os.putenv("HBNB_MYSQL_PWD", "hbnb_test_pwd")
os.putenv("HBNB_MYSQL_HOST", "localhost")
os.putenv("HBNB_MYSQL_DB", "hbnb_test_db")


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        # Create some test data
        obj1 = BaseModel()
        obj2 = BaseModel()
        obj3 = BaseModel()

        # Save the test data to the database
        storage = DBStorage()
        storage.new(obj1)
        storage.new(obj2)
        storage.new(obj3)
        storage.save()

        # Call the all method with no class argument
        results = storage.all()

        # Check that the results contain all the test data
        self.assertIn(obj1, results.values())
        self.assertIn(obj2, results.values())
        self.assertIn(obj3, results.values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        new_state = State(name="California")
        new_state.save()
        self.assertIn(new_state, models.storage.all().values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to the database"""
        # Create some test data
        obj1 = BaseModel()
        obj2 = BaseModel()
        obj3 = BaseModel()

        # Save the test data to the database
        storage = DBStorage()
        # storage.reload()
        storage.new(obj1)
        storage.new(obj2)
        storage.new(obj3)
        storage.save()

        # Check that the objects were saved to the database
        self.assertIn(obj1, models.storage.all().values())
        self.assertIn(obj2, models.storage.all().values())
        self.assertIn(obj3, models.storage.all().values())


class TestDBStorageMethods(unittest.TestCase):
    """Test the methods of the DBStorage class"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test the get method"""
        # Create some test data
        obj1 = State(name="California")
        obj1.save()

        # Get the object using the get method
        obj2 = models.storage.get(State, obj1.id)

        # Check that the object is the same as the original object
        self.assertEqual(obj1, obj2)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test the count method"""
        # Create some test data
        obj1 = State(name="California")
        obj2 = State(name="Nevada")
        obj3 = City(name="San Francisco", state_id=obj1.id)
        obj4 = City(name="Las Vegas", state_id=obj2.id)
        obj5 = Review(text="Great place", place_id="1234", user_id="5678")
        obj6 = Review(text="Terrible place", place_id="4321", user_id="8765")
        obj1.save()
        obj2.save()
        obj3.save()
        obj4.save()
        obj5.save()
        obj6.save()

        # Check that the count method returns the correct number of objects
        self.assertEqual(models.storage.count(), 6)
        self.assertEqual(models.storage.count(State), 2)
        self.assertEqual(models.storage.count(City), 2)
        self.assertEqual(models.storage.count(Review), 2)
        self.assertEqual(models.storage.count(User), 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete(self):
        """Test the delete method"""
        # Create some test data
        obj1 = State(name="California")
        obj1.save()

        # Delete the object using the delete method
        models.storage.delete(obj1)
        models.storage.save()

        # Check that the object was deleted from the database
        self.assertNotIn(obj1, models.storage.all().values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_reload(self):
        """Test the reload method"""
        # Create some test data
        obj1 = State(name="California")
        obj1.save()

        # Reload the database
        models.storage.reload()

        # Check that the object is no longer in the database
        self.assertNotIn(obj1, models.storage.all().values())
