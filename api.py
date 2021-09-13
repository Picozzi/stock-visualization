import datetime
import os
from flask import Flask
from flask import request
import json
from bson import ObjectId
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
import pymongo
from bson import json_util
from dotenv import load_dotenv

load_dotenv('.env')
pymongo_configuration = os.getenv('PYMONGO_ADDRESS')

app = Flask(__name__, static_folder="visualization/build", static_url_path="")
CORS(app)

mongo = pymongo.MongoClient(pymongo_configuration,
                            maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo, 'stock_analysis')
social_media_collection = pymongo.collection.Collection(
    db, 'daily_social_media_aggregation')


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@app.route('/aggregation', methods=['GET'])
@cross_origin()
def recommendations():

    date_id = datetime.datetime.now().date().strftime("%m/%d/%Y")

    new_filter = {
        "date_id": date_id
    }
    top_10_stocks_of_the_day = social_media_collection.find(
        filter=new_filter).sort("rank")
    top_10_stocks_of_the_day = json_util.dumps(top_10_stocks_of_the_day)
    print(top_10_stocks_of_the_day)
    return top_10_stocks_of_the_day


@ app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run()
