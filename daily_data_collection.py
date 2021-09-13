import os
import json
import social_media_aggregator
import pymongo
import datetime
from dotenv import load_dotenv


class Stock:
    def __init__(self, date_id, rank, symbol, negative_frequency, positive_frequency, probability, total_frequency, chart_data):
        self.date_id = date_id
        self.rank = rank
        self.symbol = symbol
        self.negative_frequency = negative_frequency
        self.positive_frequency = positive_frequency
        self.probability = probability
        self.total_frequency = total_frequency
        self.chart_data = chart_data


load_dotenv('.env')

# Initate database client
pymongo_configuration = os.getenv('PYMONGO_ADDRESS')


mongo = pymongo.MongoClient(pymongo_configuration,
                            maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo, 'stock_analysis')
social_media_collection = pymongo.collection.Collection(
    db, 'daily_social_media_aggregation')

top_10_list = []

# Retrieve top 10 most mentioned stocks on Reddit
reddit_json = social_media_aggregator.reddit_aggregation()

reddit_dict = json.loads(reddit_json)

# Initate rank
count = 1
for stock in reddit_dict:

    # temporary dictionary to save us from typing "reddit_dict[stock]['...'] each time"
    temp_dict = reddit_dict[stock]

    # temporary variable to hold Twitter data for each top 10 stock
    temp_chart_data = json.loads(
        social_media_aggregator.twitter_aggregation(stock))

    # Create a date id to identify the top 10 stocks for said day (used in database)
    temp_date_id = datetime.datetime.now().date().strftime("%m/%d/%Y")

    # Create the stock object
    stock_object = Stock(temp_date_id, count, stock, temp_dict['negative_frequency'],
                         temp_dict['positive_frequency'], temp_dict['probability'],
                         temp_dict['total_frequency'], temp_chart_data)

    top_10_list.append(stock_object)

    # Iterate rank
    count += 1


top_10_json = json.loads(json.dumps([ob.__dict__ for ob in top_10_list]))

# Insert into the database
social_media_collection.insert_many(top_10_json)
