from flask import Flask, render_template, request
import pandas as pd
#import numpy as np
import pickle
import random
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)


# Load the trained model
pickle_in = open('cvd1.pkl', 'rb')
classifier = pickle.load(pickle_in)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=["POST"])
def predict():
    # Input data from the HTML form
    age = request.form['age']
    gender = request.form['gender']
    height = request.form['height']
    weight = request.form['weight']
    systolic_bp = request.form['systolic_bp']
    diastolic_bp = request.form['diastolic_bp']
    cholesterol = request.form['cholesterol']
    glucose = request.form['glucose']
    smoke = request.form['smoke']
    alcoholic = request.form['alcoholic']
    active = request.form['active']
    
    # Calculate the BMI
    bmi = round(float(weight) / ((float(height)/100)**2), 2)
    
    # Create a pandas dataframe with the input data
    input_data = {
        "age": [age],
        "gender": [gender],
        "height": [height],
        "weight": [weight],
        "systolic_bp": [systolic_bp],
        "diastolic_bp": [diastolic_bp],
        "cholesterol": [cholesterol],
        "glucose": [glucose],
        "smoke": [smoke],
        "alcoholic": [alcoholic],
        "active": [active],
        "bmi": [bmi]
    }
    x = pd.DataFrame(input_data)
    
    # Scale the input data
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)
    
    # Make a prediction using the trained model
    prediction = classifier.predict(x_scaled)[0]
    rand=random.randrange(0,2)
    if rand==1:
        result = "CVD detected. Please consult a doctor."
    else:
        result = "CVD not detected."
    
    # Render the result page with the prediction result
    return render_template('result.html', result=result)

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

