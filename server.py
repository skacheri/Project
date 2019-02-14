from flask import Flask, render_template, redirect, session, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Meal, Foodgroup, Meal_Foodgroup, db, connect_to_db
import datetime
from jinja2 import StrictUndefined

app = Flask(__name__)

app.secret_key = "1234"

#################################################################
#####Update this dict before start of server.py????HHOW##########
#################################################################

foodgroup_dictionary = {
                        "Carbohydrates": 1,
                        "Proteins": 2,
                        "Vegetables": 3,
                        "Fruits": 4,
                        "Water": 5,
                        "Juice": 6,
                        "Dairy": 7,
                        "Soda": 8,
                        "Tea_no_sugar": 9,
                        "Coffee_no_sugar": 10,
                        "Tea_with_sugar": 11,
                        "Coffee_with_sugar": 12,
                        "Unsaturated_fat": 13,
                        "Saturated_fat": 14,
                        "Trans_fat": 15
                        }

#-----------------------------------------------------

@app.route('/')
def homepage():
    """Homepage"""

    return render_template('homepage.html')

#-------------------------------------------------------

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
        flash('Try logging in again or register if first time user!') 
        #####################################################################
        ###Will need to work as if user is not registered then gives this error
        ####################################################################
        return redirect('/')

#--------------------------------------------------------


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

    return render_template('log_meal.html')

"""---------------------------------------------------------"""

@app.route('/log_meal', methods=['POST'])
def logged_meal():
    """User loged meal will enter database"""

    # fetching data from form for each meal component

    meal_time_html = request.form.get("meal_time")
    if meal_time_html:
        meal_time = datetime.datetime.strptime(meal_time_html, '%Y-%m-%dT%H:%M')
    else:
        meal_time = datetime.datetime.utcnow()


    meal_name = request.form.get("meal_name")

    meal_component_40 = request.form.get("meal_component_40")
    meal_component_10 = request.form.get("meal_component_10")
    meal_component_25 = request.form.get("meal_component_25")
    meal_component_2_25 = request.form.get("meal_component_2_25")
    meal_component_drink = request.form.get("meal_component_drink")
    meal_component_oil = request.form.get("meal_component_oil")
    
    # getting user_id out from session and assigning it to user_id variable
    user_id = session.get('user_id')

    # adding user_id and meal_name to the meal table in database
    meal = Meal(user_id=user_id, meal_time=meal_time, meal_name=meal_name)
    db.session.add(meal)
    db.session.commit()

    # fetching the meal_id of currently entered meal and storing it in variable
    meal_id = meal.meal_id 

    ########################################################
    ####Think of a for loop, or a dictionary!!!!!!!#########
    ########################################################

    # adding the foodgroups, meal, user, percentage to meal_foodgroups table
    meal_foodgroup40 = Meal_Foodgroup(meal_id=meal_id,
                                    foodgroup_id=foodgroup_dictionary[meal_component_40],
                                    percentage_meal=40)
    meal_foodgroup10 = Meal_Foodgroup(meal_id=meal_id,
                                    foodgroup_id=foodgroup_dictionary[meal_component_10],
                                    percentage_meal=10)
    meal_foodgroup25 = Meal_Foodgroup(meal_id=meal_id,
                                    foodgroup_id=foodgroup_dictionary[meal_component_25],
                                    percentage_meal=25)
    meal_foodgroup225 = Meal_Foodgroup(meal_id=meal_id,
                                    foodgroup_id=foodgroup_dictionary[meal_component_2_25],
                                    percentage_meal=25)
    meal_foodgroupdrink = Meal_Foodgroup(meal_id=meal_id,
                                    foodgroup_id=foodgroup_dictionary[meal_component_drink])    
    meal_foodgroupoil = Meal_Foodgroup(meal_id=meal_id,
                                    foodgroup_id=foodgroup_dictionary[meal_component_oil])


    db.session.add_all([meal_foodgroup40, meal_foodgroup10, meal_foodgroup25,
                        meal_foodgroup225, meal_foodgroupdrink, meal_foodgroupoil])
    db.session.commit()


    return redirect('/calendar')

"""---------------------------------------------------------"""

@app.route("/calendar")
def render_calendar():
    """Render data stored by user for each meal"""

    # NEED TO WORK ON THIS
    # JS chart plugin
    return render_template("calendar.html")



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