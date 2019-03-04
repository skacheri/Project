from model import connect_to_db, db
from server import app
from sqlalchemy import func
from model import Foodgroup

def load_foodgroups():
    """Load foodgroups into the foodgroups table"""

    # to avoid duplicating information when running this file over and over
    Foodgroup.query.delete()

    # Read u.user file and insert data
    file_handler = open("seed_data/foodgroups.data")
    for row in file_handler:
        row = row.rstrip()
        foodgroup_id, foodgroup_name = row.split("|")

        foodgroup = Foodgroup(foodgroup_id=foodgroup_id,
                    foodgroup_name=foodgroup_name)

        # We need to add to the session each foodgroup
        db.session.add(foodgroup)
    file_handler.close()
    # commit
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import foodgroups data
    load_foodgroups()