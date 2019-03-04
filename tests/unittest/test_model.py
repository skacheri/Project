"""Tests for Mealtracker Flask app."""

import unittest
from flask import Flask, session
import sqlalchemy
from server import app
from model import *


class TestModel(unittest.TestCase):
    """Login tests"""

    def setUp(self):
        """Connect to flask test client and test database"""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app)
        db.create_all()
        self.example_data()

    def example_data(self):
      """Create some sample data."""
      # In case this is run more than once, empty out existing data
      User.query.delete()

      u = User(f_name='aaa', l_name='aaa', email='aaa', password='aaa')
      m = Meal(user_id=u.user_id, meal_name="Lunch")
      f = Foodgroup(foodgroup_id='1', foodgroup_name="Test")
      g = Meal_Foodgroup(meal_id=m.meal_id, foodgroup_id=f.foodgroup_id, percentage_meal=40)

      db.session.add_all([u, m, f, g])
      db.session.commit()

    def tearDown(self):
        ''' Run after each test '''

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def testUserModel(self):
      all_users = User.query.all()
      self.assertEqual(len(all_users), 1)
      self.assertIsNotNone(all_users[0].__repr__())

    def testMealModel(self):
      m = Meal.query.all()
      self.assertEqual(len(m), 1)
      self.assertIsNotNone(m[0].__repr__())

    def testFoodGroupModel(self):
      all_meals = Foodgroup.query.all()
      self.assertEqual(len(all_meals), 1)
      self.assertIsNotNone(all_meals[0].__repr__())

    def testMealFoodgroupModel(self):
      mfgs = Meal_Foodgroup.query.all()
      self.assertEqual(len(mfgs), 1)
      self.assertIsNotNone(mfgs[0].serialize())
      self.assertIsNotNone(mfgs[0].__repr__())


if __name__ == "__main__":
    unittest.main()
    connect_to_db(app)
