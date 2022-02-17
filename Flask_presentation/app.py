# Import libraries
from flask import Flask, render_template, redirect, url_for
import numpy as np
import pandas as pd
from flask import Flask, json, jsonify
from flask import Flask, render_template, request
from urllib.parse import unquote
import pickle

# Create Flask application
app = Flask(__name__)

# Define routes and route functions
@app.route("/")
def index():
    return render_template("home.html")

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


def returnStateOptions():
    states = ['Alabama','Alaska','American Samoa','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Guam','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Palau','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']

    return states

# Todo: link up to CSV/DB
# Todo: SQL : SELECT DISTINCT county FROM db.table;
def returnStateCountyOptions():
    df = pd.read_csv('static/data_files/Employment_by_County.csv', dtype=str)
    search_state = request.args.get("state").replace("'","")
    results = df[df['county'].str.contains(search_state)]
    response = results['county']
    response = response.to_list()
    counties = {"counties":response}
    return counties

def returnCountyDemographics():
    df = pd.read_csv('static/data_files/Employment_by_County.csv', dtype=str)
    search_county = request.args.get("county").replace("%20", " ")
    search_county = unquote(search_county)
    results_ = df[df['county'].str.contains(search_county)]
    results = results_.apply(lambda x: x.to_json(), axis=1)
    return (results.to_list()[0])

@app.route("/getCountyDemogrographic", methods = ['GET', 'POST'])
def getCountyDemogrographic():
    demographic = returnCountyDemographics()
    return jsonify({"demographic":demographic})



@app.route("/listStateCounties", methods = ['GET'])
def stateCounties():
    counties = returnStateCountyOptions()
    return (counties)

@app.route("/makePrediction", methods = ['POST'])
def makePrediction():
    feature_columns = ['race_white', 'race_black', 'race_asian', 'race_two_or_more',   'race_others']
    if request.json:
        # Labor force prediction
        filename_labor_force = './static/model/finalized_model_labor_force.sav'
        model_labor_force = pickle.load(open(filename_labor_force, 'rb'))
        race_white = request.json.get('race_white')
        race_black = request.json.get('race_black')
        race_asian = request.json.get('race_asian')
        race_others = request.json.get('race_others')
        race_two_or_more = request.json.get('race_two_or_more')
        prediction_labor_force = model_labor_force.predict([[race_white,race_black,race_asian,race_others,race_two_or_more]])[0]
        prediction_labor_force_feature_importance_ = sorted(zip(model_labor_force.feature_importances_, feature_columns), reverse=True)
        prediction_labor_force_feature_importance = json.dumps(prediction_labor_force_feature_importance_)

        # Unemployment pct prediction
        filename_unemployment_pct= './static/model/finalized_model_unemployment_pct.sav'
        model_unemployment_pct = pickle.load(open(filename_unemployment_pct, 'rb'))
        race_white = request.json.get('race_white')
        race_black = request.json.get('race_black')
        race_asian = request.json.get('race_asian')
        race_others = request.json.get('race_others')
        race_two_or_more = request.json.get('race_two_or_more')
        prediction_unemployment_pct = model_unemployment_pct.predict([[race_white,race_black,race_asian,race_others,race_two_or_more]])[0]
        prediction_unemployment_pct_feature_importance_ = sorted(zip(model_unemployment_pct.feature_importances_, feature_columns), reverse=True)
        prediction_unemployment_pct_feature_importance = json.dumps(prediction_unemployment_pct_feature_importance_)
        
        # Return data in json format
        prediction_labor_force = round(prediction_labor_force)
        prediction_unemployment_pct = round(prediction_unemployment_pct, 1)
        return jsonify({
            "prediction_labor_force": prediction_labor_force, 
            "prediction_labor_force_feature_importance": prediction_labor_force_feature_importance, 
            "prediction_unemployment_pct": prediction_unemployment_pct, 
            "prediction_unemployment_pct_feature_importance":prediction_unemployment_pct_feature_importance
        })


@app.route("/predict", methods = ['GET', 'POST'])
def predict():
    return render_template('predict.html', 
        states_options = returnStateOptions())

if __name__ == '__main__':
    app.run()