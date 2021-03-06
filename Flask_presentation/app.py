# Import libraries
from flask import Flask, render_template, redirect, url_for
import numpy as np
import pandas as pd
import os
from flask import Flask, json, jsonify
from flask import Flask, render_template, request
from urllib.parse import unquote
import pickle
import json

appPath =  (os.path.abspath(os.pardir))
# Catch heroku 
if (len(appPath)<10):
    appPath = "/app"

# Create Flask application
app = Flask(__name__)

# Define routes and route functions
@app.route("/")
def index():
    return render_template("home.html", 
    filepath =  (appPath)
    )

@app.route("/test1")
def test1():
    return "test1"

@app.route("/test2")
def test2():
    return {'a':1, 'b':2}


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


def returnStateOptions():
    states = ['Alabama',
    'Alaska',
    'Arizona',
    'Arkansas',
    'California',
    'Colorado',
    'Connecticut',
    'Delaware',
    'Florida',
    'Georgia',
    'Hawaii',
    'Idaho',
    'Illinois',
    'Indiana',
    'Iowa',
    'Kansas',
    'Kentucky',
    'Louisiana',
    'Maine',
    'Maryland',
    'Massachusetts',
    'Michigan',
    'Minnesota',
    'Mississippi',
    'Missouri',
    'Montana',
    'Nebraska',
    'Nevada',
    'New Hampshire',
    'New Jersey',
    'New Mexico',
    'New York',
    'North Carolina',
    'North Dakota',
    'Ohio',
    'Oklahoma',
    'Oregon',
    'Pennsylvania',
    'Rhode Island',
    'South Carolina',
    'South Dakota',
    'Tennessee',
    'Texas',
    'Utah',
    'Vermont',
    'Virginia',
    'Washington',
    'West Virginia',
    'Wisconsin',
    'Wyoming']

    return states

Employment_by_County = appPath + '/Flask_presentation/static/data_files/Employment_by_County.csv'
Employment_Education_by_County = appPath + '/Flask_presentation/static/data_files/Employment_by_County_with_education_info.csv'


def returnStateCountyOptions():
    df = pd.read_csv(Employment_by_County)
    search_state = request.args.get("state").replace("'","")
    #results = df[df['county'].str.split(',')[1].contains(search_state)]
    results = df[df['county'].str.contains(search_state)]   
    response = results['county']
    response = response.to_list()
    counties = {"counties":response}
    return jsonify(counties)

def returnCountyDemographics():
    df = pd.read_csv(Employment_by_County)
    search_county = request.args.get("county").replace("%20", " ")
    search_county = unquote(search_county)
    results_ = df[df['county'].str.contains(search_county)]
    results = results_.apply(lambda x: x.to_json(), axis=1)
    return (results.to_list()[0])

def returnCountyDemographicsEducation():
    df = pd.read_csv(Employment_Education_by_County)
    search_county = request.args.get("county").replace("%20", " ")
    search_county = unquote(search_county)
    results_ = df[df['county'].str.contains(search_county)]
    results = results_.apply(lambda x: x.to_json(), axis=1)
    return (results.to_list()[0])

@app.route("/getCountyDemogrographic", methods = ['GET', 'POST'])
def getCountyDemogrographic():
    demographic = returnCountyDemographics()
    return jsonify({"demographic":demographic})

@app.route("/getCountyDemogrographicEducation", methods = ['GET', 'POST'])
def getCountyDemogrographicEducation():
    demographic = returnCountyDemographicsEducation()
    return jsonify({"demographic":demographic})



@app.route("/listStateCounties", methods = ['GET'])
def stateCounties():
    counties = returnStateCountyOptions()
    return (counties)

@app.route("/predict", methods = ['GET', 'POST'])
def predict():
    return render_template('predict.html', 
        states_options = returnStateOptions())




@app.route("/predict-unemployed", methods = ['GET', 'POST'])
def predictUnemployed():
    return render_template('predict-unemployed.html', 
        states_options = returnStateOptions())


@app.route("/makeUnemployedPrediction", methods = ['POST'])
def makeUnemployedPrediction():
    feature_columns = ['race_white', 'race_black', 'race_asian','race_others','completed_college_county','not_completed_college_county']
    if request.json:

        # Extra json input
        race_white = request.json.get('race_white')
        race_black = request.json.get('race_black')
        race_asian = request.json.get('race_asian')
        race_others = request.json.get('race_others')
        completed_college_county = request.json.get('completed_college_county')
        not_completed_college_county = request.json.get('not_completed_college_county')

        # Labor force prediction
        filename_labor_force = appPath + '/Flask_presentation/static/model/finalized_model_variation_education.sav'
        model_unemployed = pickle.load(open(filename_labor_force, 'rb'))
        prediction_unemployed = model_unemployed.predict([[race_white,race_black,race_asian,race_others,completed_college_county, not_completed_college_county]])[0]
        prediction_unemployed_feature_importance_ = sorted(zip(model_unemployed.feature_importances_, feature_columns), reverse=True)
        prediction_unemployed_feature_importance = json.dumps(prediction_unemployed_feature_importance_)

        
        # Return data in json format
        prediction_unemployed = round(prediction_unemployed)

        return jsonify({
            "prediction_unemployed": prediction_unemployed, 
            "prediction_unemployed_feature_importance":prediction_unemployed_feature_importance
        })

if __name__ == '__main__':
    app.run()