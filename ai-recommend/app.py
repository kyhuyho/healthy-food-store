import os
from flask import Flask, request, Response
from flask_restful import Resource, Api
from flask_cors import CORS

from json import dumps
from flask import jsonify
from werkzeug.utils import secure_filename
import random
import requests
import pandas as pd
import numpy as np
from model import *
import requests
import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from pulp import *
import numpy as np
UPLOAD_FOLDER = 'image'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
CORS(app)

data_api = "http://localhost:5001/api/ingredient/getingredientwithoutpagination"
global_data = None

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def fetch_data():
    global global_data
    try:
        response = requests.get(data_api)
        response.raise_for_status()

        data_json = response.json()

        # Extract only the 'data' field from the JSON response
        api_data = data_json.get("ingredientData")  # Assuming 'data' is the key for the data array

        global_data = pd.DataFrame(api_data)  # Create DataFrame from extracted data
        global_data = global_data.replace('na', pd.NA)  # Replace 'na' with NA
        global_data = global_data.fillna(0)  # Fill missing values with 0

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {str(e)}")
        global_data = pd.DataFrame()
class fetching(Resource):
    def get(self):
        fetch_data()
        result = global_data
        finalresult =  jsonify(result.to_dict(orient='records'))
        finalresult.headers.add('Access-Control-Allow-Origin', '*')
        return finalresult
class dietoptimize(Resource):
    def post(self):
        if request.method == 'POST':
            if global_data is None:
                fetch_data()
            data = request.get_json()
            calories = data.get('calories')
            ingredient = data.get('ingredient')
            noIngredient = data.get('noIngredient')
            unhealthyfat = data.get('unhealthyfat')
            cholesterol = data.get('cholesterol')
            sugar = data.get('sugar')
            sodium = data.get('sodium')
            calcium = data.get('calcium')
            iron = data.get('iron')
            zinc = data.get('zinc')
            gramon = data.get('gramon')
            data_ingredient = pd.DataFrame((ingredient))
            data_noingredient = pd.DataFrame((noIngredient))
            print("calories",calories)
            print("okeokeoke",unhealthyfat,cholesterol,sugar,sodium, calcium , iron, zinc)
            print("okeokeoke2",gramon)
            # print("okeokeoke",data_noingredient["name"].tolist())
            result = DietModel(global_data,int(calories),data_ingredient, data_noingredient,unhealthyfat,cholesterol,sugar,sodium, calcium , iron, zinc, gramon,'male' )
            finalresult =  jsonify(result.to_dict(orient='records'))
            finalresult.headers.add('Access-Control-Allow-Origin', '*')
            return finalresult

api.add_resource(fetching, '/fetching')
api.add_resource(dietoptimize, '/diet-list')
if __name__ == '__main__':
     fetch_data()
     app.run()