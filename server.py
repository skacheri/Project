from flask import Flask, render_template, redirect, session, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Meal, Foodgroup, Meal_Foodgroup, db, connect_to_db
import datetime

app = Flask(__name__)

app.secret_key = "1234"

"""-----------------------------------------------------"""

@app.route('/')
def homepage():
    """Homepage"""

    return render_template('homepage.html')

"""-------------------------------------------------------"""

@app.route('/login', methods=['POST'])
def check_login():
    """Check user log in information before rendering log_meal page and storing info in session"""

    email = request.form.get("email")
    password = request.form.get("password")

    #Email and password query check if mateches
    query = User.query.filter(User.email == email, User.password == password).first()

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
    query = User.query.filter(User.email==email).first()

    if query:
        flash('The email entered is already in use, try logging in!')
        return redirect('/')
    else:
        f_name = request.form.get("f_name") #fetching data from form
        l_name = request.form.get("l_name")
        email = request.form.get("email")
        password = request.form.get("password")

        #inserting data obtained from form into the database
        user = User(f_name=f_name, l_name=l_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        flash('Thank you for registering for your Meal Plate Tracker')
        session['user_id'] = user.user_id

        flash('You will be logged in')
        return redirect('/log_meal')

"""--------------------------------------------------------"""

@app.route('/log_meal')
def log_meal():
    """Logging a meal for user"""

    return render_template('/log_meal.html')

"""---------------------------------------------------------"""

@app.route('/log_meal', methods=['POST'])
def logged_meal():
    """User loged meal will enter database"""

    # fetching data from form for each meal component
    meal_name = request.form.get("meal_name")
    meal_component_40 = request.form.get("meal_component_40")
    meal_component_10 = request.form.get("meal_component_10")
    meal_component_25 = request.form.get("meal_component_25")
    meal_component_2_25 = request.form.get("meal_component_2_25")
    meal_component_drink = request.form.get("meal_component_drink")
    meal_component_oil = request.form.get("meal_component_oil")

    ######################################################################
    # now = datetime.datetime.now() 
    #was thinking instead of this to have a calender for user to pick day which 
    #should default to that day, so if they forget to enter meal on a day its cool
    ######################################################################

    # getting user_id out from session and assigning it to user_id variable
    user_id = session.get('user_id')

    # adding user_id and meal_name to the meal table in database
    meal = Meal(user_id=user_id, meal_name=meal_name)
    db.session.add(meal)
    db.session.commit()

    # fetching the meal_id of currently entered meal and storing it in variable
    meal_id = meal.meal_id 

    ########################################################################
    # unsure why i need this block anymore
    # quering the foodgroup table for foodgroup id 
    query40 = Foodgroup.query.filter(Foodgroup.foodgroup_name==meal_component_40).first()
    query10 = Foodgroup.query.filter(Foodgroup.foodgroup_name==meal_component_10).first()
    query25 = Foodgroup.query.filter(Foodgroup.foodgroup_name==meal_component_25).first()
    query225 = Foodgroup.query.filter(Foodgroup.foodgroup_name==meal_component_2_25).first()
    querydrink = Foodgroup.query.filter(Foodgroup.foodgroup_name==meal_component_drink).first()
    queryoil = Foodgroup.query.filter(Foodgroup.foodgroup_name==meal_component_oil).first()
    ########################################################################

    # adding the foodgroups, meal, user, percentage to meal_foodgroups table
    meal_foodgroup40 = Meal_Foodgroup(meal_id=meal_id,
                                    foodgroup_id=query40.foodgroup_id, percentage_meal=40)
    meal_foodgroup10 = Meal_Foodgroup(meal_id=meal_id,
                                    foodgroup_id=query10.foodgroup_id, percentage_meal=10)
    meal_foodgroup25 = Meal_Foodgroup(meal_id=meal_id,
                                    foodgroup_id=query25.foodgroup_id, percentage_meal=25)
    meal_foodgroup225 = Meal_Foodgroup(meal_id=meal_id,
                                    foodgroup_id=query225.foodgroup_id, percentage_meal=25)
    meal_foodgroupdrink = Meal_Foodgroup(meal_id=meal_id,
                                    foodgroup_id=querydrink.foodgroup_id)    
    meal_foodgroupoil = Meal_Foodgroup(meal_id=meal_id,
                                    foodgroup_id=queryoil.foodgroup_id)

    db.session.add(meal_foodgroup40)
    db.session.add(meal_foodgroup10)
    db.session.add(meal_foodgroup25)
    db.session.add(meal_foodgroup225)
    db.session.add(meal_foodgroupdrink)
    db.session.add(meal_foodgroupoil)
    db.session.commit()


    return redirect('/')

"""---------------------------------------------------------"""

@app.route("/log_out")
def logged_out():

    session.pop('user_id', None)
    flash("You are logged out")

    return redirect('/')

"""-----------------------------------------------------------"""
"""-----------------------------------------------------------"""

if __name__ == "__main__":

    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')