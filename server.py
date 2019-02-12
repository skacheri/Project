from flask import Flask, render_template, redirect, session, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Meal, Foodgroup, Meal_Foodgroup

app = Flask(__name__)

app.secret_key = "1234"

"""-----------------------------------------------------"""

@app.route('/')
def homepage():
    """Homepage"""

    return render_template('homepage.html')

"""-------------------------------------------------------"""

@app.route('/log_in_check', methods=['POST'])
def check_login():
    """Check user log in information before rendering log_meal page and storing info in session"""

    email = request.form.get("email")
    password = request.form.get("password")

    #Email and password query check if mateches
    query = User.query.filter(User.email == email , User.password == password).first()

    if query:
        session['user_id'] = query.user_id
        flash('You are successfully logged in')
        return redirect('/log_meal')
    else:
        flash('Try the combination of email and password again!')
        return redirect('/')

"""--------------------------------------------------------"""

@app.route('/register')
def register_user():
    """Registration for user"""

    return render_template('register.html')

"""--------------------------------------------------------"""

@app.route('/register', methods=['POST'])
def check_register_user():
    """Check Registration for user"""

    email = request.form.get("email")
    query = User.query.filter(User.email == email).first()

    if query:
        flash('The email entered is already in use, try logging in!')
        return redirect('/')
    else:
        return redirect('/thank_you')

"""--------------------------------------------------------"""

@app.route('/thank_you', methods=['POST'])
def thank_user():
    """Thank user for registering"""

    #fetching data from form
    f_name = request.form.get("f_name")
    l_name = request.form.get("l_name")
    email = request.form.get("email")
    password = request.form.get("password")

    #inserting data obtained from form into the database
    user = User(f_name=f_name, l_name=l_name, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    flash('Thank you for registering for your Meal Plate Tracker')
    return redirect('/log_meal')

"""--------------------------------------------------------"""

@app.route('/log_meal')
def log_meal():
    """Logging a meal for user"""

    return render_template('/log_meal.html')

"""---------------------------------------------------------"""

@app.route('/logged-meal')
def logged_meal():
    """User loged meal will enter database"""

    pass

"""-----------------------------------------------------------"""
"""-----------------------------------------------------------"""

if __name__ == "__main__":

    app.debug = True
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')