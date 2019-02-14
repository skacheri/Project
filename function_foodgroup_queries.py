    # unsure why i need this block anymore
    # quering the foodgroup table for foodgroup id 
    # make a fucntion to make the six queries, so you can call function to update foodgroup
    query40 = Foodgroup.query.filter(Foodgroup.foodgroup_name==meal_component_40).first()
    query10 = Foodgroup.query.filter(Foodgroup.foodgroup_name==meal_component_10).first()
    query25 = Foodgroup.query.filter(Foodgroup.foodgroup_name==meal_component_25).first()
    query225 = Foodgroup.query.filter(Foodgroup.foodgroup_name==meal_component_2_25).first()
    querydrink = Foodgroup.query.filter(Foodgroup.foodgroup_name==meal_component_drink).first()
    queryoil = Foodgroup.query.filter(Foodgroup.foodgroup_name==meal_component_oil).first()