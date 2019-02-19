"""Models and database functions for Meal Plate Tracker project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User of Meal Plate Tracker website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provied helpful representation of class User when printed"""

        return ('User user_id={} email={}'.format(self.user_id, self.email))


class Meal(db.Model):
    """Meal information for plate"""

    __tablename__ = "meals"

    meal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    meal_time = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    meal_name = db.Column(db.String(50)) #either breakfast, lunch or dinner from user dropdown
    #2.0 features for calorie count:
    # meal_description = db.Column(db.String(50), nullable=True) #nullable for now
    # calories = db.Column(db.Numeric(8, 2), nullable=True) #nullable for now

    users = db.relationship("User", backref="meals")
    foodgroups = db.relationship("Foodgroup", secondary="meal_foodgroups", backref="meals")
    meal_foodgroups = db.relationship("Meal_Foodgroup", backref="meals")

    def __repr__(self):
        """Provide helpful representation of class Meal when printed"""

        return ('Meal: id={} mealtime={}'.format(self.meal_id, self.meal_time))


class Foodgroup(db.Model):
    """Food group information for plate"""

    __tablename__ = "foodgroups"

    foodgroup_id = db.Column(db.Integer, primary_key=True)
    foodgroup_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation of class Meal when printed"""

        return ('Foodgroup: id={} name={}'.format(self.foodgroup_id, self.foodgroup_name))


class Meal_Foodgroup(db.Model):
    """Associatiion table between foodgroup and meal"""

    __tablename__ = "meal_foodgroups"

    meal_foodgroup_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.meal_id'))
    foodgroup_id = db.Column(db.Integer, db.ForeignKey('foodgroups.foodgroup_id'))
    percentage_meal = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation of class Meal_Foodgroup(association table)"""

        return ('meal-foodgroup-id: {}, meal-id: {}, foodgroup_id: {}, percentage_meal: {}'
                .format(self.meal_foodgroup_id, self.meal_id,
                        self.foodgroup_id, self.percentage_meal))

    def serialize(self):
        return {
            "meal_id": self.meal_id,
            "foodgroup_id": self.foodgroup_id,
            "percentage_meal": self.percentage_meal
            }

""""""
""""""

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mealtracker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
    db.create_all()