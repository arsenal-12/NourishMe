from flask import Flask, render_template, request
app = Flask(__name__)
import pandas as pd 

df=pd.read_csv('static\loose_wt.csv')
def recommend_foods(calories, carbs, fats, protein):
    # Convert the provided nutritional ranges to integers
    calories = int(calories)
    carbs = int(carbs)
    fats = int(fats)
    protein = int(protein)

    # Filter foods based on the given criteria
    filtered_foods = df[(df['Energ_Kcal'] >= calories) &
                        (df['Carbohydrt_(g)'] <= carbs) &  # Update the condition to use less than or equal to
                        (df['Lipid_Tot_(g)'] <= fats) &
                        (df['Protein_(g)'] <= protein)]  # Update the condition to use less than or equal to

    # Print the filtered DataFrame

    # Convert the DataFrame to a list of dictionaries
    recommended_foods = filtered_foods.to_dict(orient='records')

    return recommended_foods




CALORIES_PER_KG = 30  # Adjust based on activity level
CARBS_PERCENTAGE = 50
FATS_PERCENTAGE = 30
PROTEIN_PERCENTAGE = 20

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/nutrition_planning')
def nutrition_planning():
    return render_template('nutrition_planning.html')

@app.route('/mental_wellness')
def mental_wellness():
    return render_template('mental_wellness.html')
@app.route('/calculate_intake', methods=['POST'])
def calculate_intake():
    # Retrieve user input from the form
    age = int(request.form.get('age'))
    height = float(request.form.get('height'))
    weight = float(request.form.get('weight'))
    gender = request.form.get('gender')
    body_fat = request.form.get('body_fat')
    activity_level = request.form.get('activity_level')
    weight_goal = request.form.get('weight_goal')

    # Calculate BMI
    bmi = calculate_bmi(height, weight)

    # Calculate Total Daily Energy Expenditure (TDEE)
    tdee = calculate_tdee(age, height, weight, gender, activity_level)

    # Calculate Calories, Carbs, Fats, and Protein based on weight goal
# Update the function call to the modified function
    calories, carbs, fats, protein = calculate_nutritional_values(tdee, weight_goal)

    recommended_foods_list = recommend_foods(calories, carbs, fats, protein)

    return render_template('result.html', bmi=bmi, calories=calories, carbs=carbs, fats=fats, protein=protein, recommended_foods_df=recommended_foods_list)
def calculate_bmi(height, weight):
    height_meters = height / 100
    bmi = weight / (height_meters ** 2)
    return round(bmi, 2)

def calculate_tdee(age, height, weight, gender, activity_level):
    # Use Harris-Benedict Equation to calculate Basal Metabolic Rate (BMR)
    if gender == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    # Adjust BMR based on activity level to get TDEE
    if activity_level == 'sedentary':
        tdee = bmr * 1.2
        # Adjust constants for sedentary activity level
        CALORIES_PER_KG = 25
        CARBS_PERCENTAGE = 45
        FATS_PERCENTAGE = 25
        PROTEIN_PERCENTAGE = 30
    elif activity_level == 'moderate':
        tdee = bmr * 1.55
        # Adjust constants for moderate activity level
        CALORIES_PER_KG = 30
        CARBS_PERCENTAGE = 50
        FATS_PERCENTAGE = 30
        PROTEIN_PERCENTAGE = 20
    elif activity_level == 'active':
        tdee = bmr * 1.9
        # Adjust constants for active activity level
        CALORIES_PER_KG = 35
        CARBS_PERCENTAGE = 55
        FATS_PERCENTAGE = 25
        PROTEIN_PERCENTAGE = 20

    return round(tdee)
def calculate_nutritional_values(tdee, weight_goal):
    # Calculate Calories based on weight goal
    if weight_goal == 'lose_weight':
        calories = int(tdee * 0.8)//4
    elif weight_goal == 'maintain':
        calories = int(tdee)//4
    elif weight_goal == 'build_muscle':
        calories = int(tdee * 1.2)//4

    # Define macronutrient percentages
    carbs_percentage = 50  # Adjust as needed
    fats_percentage = 30   # Adjust as needed
    protein_percentage = 20  # Adjust as needed

    # Calculate macronutrient values based on total calories
    carbs = (int(calories * carbs_percentage / 100))//4
    fats = (int(calories * fats_percentage / 100))//4
    protein = (int(calories * protein_percentage / 100))//4

    return calories, carbs, fats, protein


if __name__ == '__main__':
    app.run(debug=True)
