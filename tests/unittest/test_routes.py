"""Tests for Mealtracker Flask app."""
import unittest
from flask import Flask, session
from server import app, init_foodgroups
from model import *
from foodgroups_seed import load_foodgroups
import sqlalchemy
import bcrypt

class TestRoutes(unittest.TestCase):
    """Login tests"""

    def setUp(self):
      """Connect to flask test client and test database"""

      self.client = app.test_client()
      app.config['TESTING'] = True
      connect_to_db(app)
      db.drop_all()
      db.session.commit()
      db.create_all()
      load_foodgroups()
      init_foodgroups()
      self.example_data()


    def example_data(self):
      """Create some sample data."""
      # In case this is run more than once, empty out existing data
      User.query.delete()

      hashed_pwd = str(bcrypt.hashpw(bytes('temp_password', 'utf-8'), bcrypt.gensalt()), 'utf-8')
      u = User(f_name='aaa', l_name='aaa', email='aaa@example.com', password=hashed_pwd)
      m = Meal(user_id=u.user_id, meal_name="Lunch")
      f = Foodgroup(foodgroup_id='100', foodgroup_name="Test")
      g = Meal_Foodgroup(meal_id=m.meal_id, foodgroup_id=f.foodgroup_id, percentage_meal=40)

      db.session.add_all([u, m, f, g])
      db.session.commit()

    def tearDown(self):
        ''' Run after each test '''
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_home_page(self):
      """Some non-database test..."""
      result = self.client.get("/")
      self.assertEqual(result.status_code, 200)
      self.assertIn('First time users please register here', str(result.data))

    def test_log_meal(self):
      """Some non-database test..."""
      result = self.client.get("/log_meal")
      self.assertEqual(result.status_code, 200)

    def test_login_failed(self):
      result = self.client.post('/login',
        data={'email':'aaa@example.com', 'password':'bar'})
      self.assertEqual(result.status_code, 302)
      self.assertTrue((str(result.location)).endswith('/'))

    def test_login_success(self):
      result = self.client.post('/login',
        data={'email':'aaa@example.com', 'password':'temp_password'})
      self.assertEqual(result.status_code, 302)
      self.assertIn('/log_meal', str(result.location))

    def test_login_bad_user_name(self):
      result = self.client.post('/login',
        data={'email':'xyz@example.com', 'password':'asd'})
      self.assertEqual(result.status_code, 302)
      self.assertTrue((str(result.location)).endswith('/'))

    def test_register(self):
      result = self.client.post('/register',
        data={
          'email':'test@example.com', 
          'password':'asd',
          'f_name': 'Test',
          'l_name': 'User'})
      self.assertEqual(result.status_code, 302)
      self.assertIn('/log_meal', str(result.location))

    def test_log_meal_post(self):
      result = self.client.post('/log_meal',
        data={
          'meal_name':'Test meal', 
          'meal_component_40':'Vegetables',
          'meal_component_10': 'Vegetables',
          'meal_component_25':'Vegetables',
          'meal_component_2_25': 'Vegetables',
          'meal_component_oil': 'Unsaturated_fat',
          'meal_component_drink': 'Water'})
      self.assertEqual(result.status_code, 302)
      self.assertIn('/calendar', str(result.location))