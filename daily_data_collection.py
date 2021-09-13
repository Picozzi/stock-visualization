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

pymongo_configuration = os.getenv('PYMONGO_ADDRESS')


mongo = pymongo.MongoClient(pymongo_configuration,
                            maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo, 'stock_analysis')
social_media_collection = pymongo.collection.Collection(
    db, 'daily_social_media_aggregation')


complete_list = []
reddit_json = social_media_aggregator.reddit_aggregation()

reddit_dict = json.loads(reddit_json)
count = 1
for top_10 in reddit_dict:

    temp = reddit_dict[top_10]
    temp_chart_data = json.loads(
        social_media_aggregator.twitter_aggregation(top_10))
    temp_date_id = datetime.datetime.now().date().strftime("%m/%d/%Y")
    stock_object = Stock(temp_date_id, count, top_10, temp['negative_frequency'],
                         temp['positive_frequency'], temp['probability'],
                         temp['total_frequency'], temp_chart_data)

    complete_list.append(stock_object)
    count += 1


print(complete_list)
t = json.dumps([ob.__dict__ for ob in complete_list])
b = json.loads(t)
social_media_collection.insert_many(b)
