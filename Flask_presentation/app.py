# Import libraries
from flask import Flask, render_template, redirect, url_for
import numpy as np
import pandas as pd
from flask import Flask, json, jsonify
from flask import Flask, render_template, request
from urllib.parse import unquote

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



@app.route("/listStateCounties", methods = ['GET', 'POST'])
def stateCounties():
    counties = returnStateCountyOptions()
    return (counties)

@app.route("/makePrediction", methods = ['GET', 'POST'])
def makePrediction():
    if request.json:

        race_white = request.json.get('race_white')
        race_black = request.json.get('race_black')
        race_asian = request.json.get('race_asian')
        race_others = request.json.get('race_others')
        race_two_or_more = request.json.get('race_two_or_more')

        # use pickle to load our .sav model
        # assign model to variable
        # call model.predict(features_predict
        # set prediction to prediction_value
        prediction_value = (int(race_white) + int(race_black) + int(race_asian) + int(race_others) + int(race_two_or_more)) / 5
        return jsonify({"prediction": prediction_value})


@app.route("/predict", methods = ['GET', 'POST'])
def predict():
    # Start collecting post data and put into array for prediction
    #form_values = [x for x in request.form.values()]
    #features_predict = [int(x) for x in form_values]
    request_type = request.form.get("request_type")
    selected_state = request.form.get("requested_state")
    selected_county = request.form.get("requested_county")
    value1 = request.form.get("value1")
    value2 = request.form.get("value2")
    value3 = request.form.get("value3")
    value1_entered = ""
    value2_entered = ""
    value3_entered = ""
    prediction_value = ""
    state_counties = []

    if request_type == "listCounties":
        state_counties = returnStateCountyOptions()


    #if value1 and value2 and value3:
    if request_type == "makePrediction":
        value1_entered = value1
        value2_entered = value2
        value3_entered = value3

        # use pickle to load our .sav model
        # assign model to variable
        # call model.predict(features_predict
        # set prediction to prediction_value
        prediction_value = (int(value1) + int(value2) + int(value3)) / 3

    return render_template('predict.html', 
        states_options = returnStateOptions(),
        state_counties_options = state_counties,
        value1_val = value1,
        value2_val = value2,
        value3_val = value3,
        value1_entered_val = value1_entered,
        value2_entered_val = value2_entered,
        value3_entered_val = value3_entered,
        prediction_value_val = prediction_value,
        selected_state_val = selected_state,
        selected_county_val = selected_county,
        request_type_val = request_type)

if __name__ == '__main__':
    app.run()