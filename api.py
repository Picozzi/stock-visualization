import datetime
import os
from flask import Flask
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
import pymongo
from bson import json_util
from dotenv import load_dotenv

load_dotenv('.env')

# configurations of Flask API and database client access
pymongo_configuration = os.getenv('PYMONGO_ADDRESS')

app = Flask(__name__, static_folder="visualization/build", static_url_path="")
CORS(app)

mongo = pymongo.MongoClient(pymongo_configuration,
                            maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo, 'stock_analysis')
social_media_collection = pymongo.collection.Collection(
    db, 'daily_social_media_aggregation')


@app.errorhandler(404)
def not_found(e):
    print(e)
    return app.send_static_file('index.html')


# API route for front-end to gather aggregate data
@app.route('/aggregation', methods=['GET'])
@cross_origin()
def recommendations():

    date_id = datetime.datetime.now().date().strftime("%m/%d/%Y")

    new_filter = {
        "date_id": date_id
    }
    # Retrieve the top 10 stocks from the database for the current day and order by rank
    top_10_stocks_of_the_day = social_media_collection.find(
        filter=new_filter).sort("rank")
    top_10_stocks_of_the_day = json_util.dumps(top_10_stocks_of_the_day)
    return top_10_stocks_of_the_day


@ app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run()
