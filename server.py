from flask import Flask, render_template, redirect, session, request, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Meal, Foodgroup, Meal_Foodgroup, db, connect_to_db
import datetime
import pytz
import tzlocal
import bcrypt
from jinja2 import StrictUndefined
import json

app = Flask(__name__)
foodgroup_dictionary = {}
app.secret_key = "1234"


@app.route('/')
def homepage():
    """Homepage"""
    if 'user_id' in session:
        return redirect('/log_meal')
    return render_template('homepage.html')

################################################################################

@app.route('/login', methods=['POST'])
def check_login():
    """Check user log in information before rendering log_meal page and storing info in session"""

    email = request.form.get("email")
    password = request.form.get("password")

    #Email and password query check if mateches
    query = User.query.filter(User.email == email).first()
    if query:
        if bcrypt.checkpw(password.encode('utf-8'), query.password.encode('utf-8')):
            session['user_id'] = query.user_id
            flash('You are successfully logged in')
            return redirect('/log_meal')
        else:
            flash('Hello valued user please try loggin in again')
            return redirect('/')
    else:
        flash('Please register')
        return redirect('/')


################################################################################

@app.route('/info')
def how_to_use():
    """Displays textual information on how to use meal tracker"""

    return render_template('info.html')


################################################################################


@app.route('/register')
def register_user():
    """Registration for user"""

    return render_template('register.html')

################################################################################

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
        hashed = str(bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt()), 'utf-8')

        #inserting data obtained from form into the database
        user = User(f_name=f_name, l_name=l_name, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()

        flash('Thank you for registering for your Meal Plate Tracker')
        session['user_id'] = user.user_id

        flash('You will be logged in')
        return redirect('/log_meal')

################################################################################

@app.route('/log_meal')
def log_meal():
    """Logging a meal for user"""

    if not session:
        flash('You need to login prior to accessing this page')
        # del session
        return redirect('/')
    return render_template('log_meal.html')

################################################################################

@app.route('/log_meal', methods=['POST'])
def logged_meal():
    """User loged meal will enter database"""

    # fetching data from form for each meal component

    meal_time_html = request.form.get("meal_time")
    if meal_time_html:
        local_zone = pytz.timezone("US/Pacific")
        meal_time_local = datetime.datetime.strptime(meal_time_html, '%Y-%m-%dT%H:%M')
        datetime_with_tz = local_zone.localize(meal_time_local, is_dst=None) # No daylight saving
        meal_time = datetime_with_tz.astimezone(pytz.utc)
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
    # meal.users.user_id.append(meal) instead of the user_id=user_id above
    db.session.add(meal)
    db.session.commit()

    # fetching the meal_id of currently entered meal and storing it in variable
    meal_id = meal.meal_id 


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
                                    foodgroup_id=foodgroup_dictionary[meal_component_drink],
                                    percentage_meal=1)    
    meal_foodgroupoil = Meal_Foodgroup(meal_id=meal_id,
                                    foodgroup_id=foodgroup_dictionary[meal_component_oil],
                                    percentage_meal=2)


    db.session.add_all([meal_foodgroup40, meal_foodgroup10, meal_foodgroup25,
                        meal_foodgroup225, meal_foodgroupdrink, meal_foodgroupoil])
    db.session.commit()


    return redirect('/calendar')

################################################################################

@app.route("/calendar/get_data")
def calendar_get_data():
    """Render data stored by user for each meal"""

    # get user_id from session
    user_id = session.get('user_id')
    # get meals for user_id
    meals_for_user = Meal.query.filter(Meal.user_id==user_id).order_by(
                    Meal.meal_time).options(db.joinedload("meal_foodgroups")).all()

        
    events = []
    #loop through the meals to obtain each meal
    for meal in meals_for_user:
        #initialize an empty event object to store each meal data
        event = {}
        event['title']=meal.meal_name
        event['meal_id']=meal.meal_id
        event['start_utc']=meal.meal_time
        #initialize an empty meal foodgroup list for each meal food info
        event['meal_foodgroups']=[]

        #loop through each of the mral_foodgroups in each meal
        for m in meal.meal_foodgroups:
            #add to the empty meal_foodgroups list each component in a particular format as defined in model.py
            event['meal_foodgroups'].append(m.serialize())

        event['allDay']=False
        #add to the events list each event
        events.append(event)
    return jsonify(events)

################################################################################

@app.route("/calendar")
def render_calendar():
    """Render data stored by user for each meal"""

    if not session:
        flash('You need to login prior to accessing this page')
        return redirect('/')

    # get user_id from session
    user_id = session.get('user_id')
    # get meals for user_id
    meals_for_user = Meal.query.filter(Meal.user_id==user_id).order_by(
                    Meal.meal_time).options(db.joinedload("meal_foodgroups")).all()


    return render_template("calendar.html", 
                           meals_for_user=meals_for_user,
                           )

################################################################################

@app.route("/log_out")
def logged_out():  


    del session['user_id']
    flash("You are logged out")
    

    return redirect('/')

################################################################################
################################################################################

def init_foodgroups():
    """Making the foodgroups dictionary from table on running server.py"""
    all_foodgroups = Foodgroup.query.all()
    for foodgroup in all_foodgroups:
        foodgroup_dictionary[foodgroup.foodgroup_name] = foodgroup.foodgroup_id

if __name__ == "__main__":

    # app.debug = True
    connect_to_db(app)
    init_foodgroups()
    # DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')