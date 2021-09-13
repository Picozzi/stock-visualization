import datetime
import praw
from dotenv import load_dotenv
import os
import pandas as pd
import string
import flair
import yfinance
import requests
import re

load_dotenv('.env')

reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
reddit_secret = os.getenv('REDDIT_SECRET')
reddit_user_agent = os.getenv('REDDIT_USER_AGENT')
twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
endpoint = 'https://api.twitter.com/2/tweets/search/recent'
headers = {'authorization': f'Bearer {twitter_bearer_token}'}

# --- CONSTANTS ---

current_time = datetime.datetime.now()
cut_off = current_time - datetime.timedelta(days=7)
epoch_cut_off = cut_off.timestamp()
sentiment_model = flair.models.TextClassifier.load('en-sentiment')
ticker_df = pd.read_csv('list_of_all_stocks.csv')
blacklist = {'I', 'ARE',  'ON', 'GO', 'NOW', 'CAN', 'UK', 'SO', 'OR', 'OUT', 'SEE', 'ONE', 'LOVE', 'U', 'STAY', 'HAS', 'BY', 'BIG', 'GOOD', 'RIDE', 'EOD', 'ELON', 'WSB', 'THE', 'A', 'ROPE', 'YOLO', 'TOS', 'CEO', 'DD', 'IT', 'OPEN', 'ATH', 'PM', 'IRS', 'FOR', 'DEC', 'BE', 'IMO', 'ALL', 'RH', 'EV', 'TOS', 'CFO', 'CTO', 'DD', 'BTFD', 'WSB', 'OK', 'PDT', 'RH', 'KYS', 'FD', 'TYS', 'US', 'USA', 'IT', 'ATH', 'RIP', 'BMW', 'GDP', 'OTM',
             'ATM', 'ITM', 'IMO', 'LOL', 'AM', 'BE', 'PR', 'PRAY', 'PT', 'FBI', 'SEC', 'GOD', 'NOT', 'POS', 'FOMO', 'TL;DR', 'EDIT', 'STILL', 'WTF', 'RAW', 'PM', 'LMAO', 'LMFAO', 'ROFL', 'EZ', 'RED', 'BEZOS', 'TICK', 'IS', 'PM', 'LPT', 'GOAT', 'FL', 'CA', 'IL', 'MACD', 'HQ', 'OP', 'PS', 'AH', 'TL', 'JAN', 'FEB', 'JUL', 'AUG', 'SEP', 'SEPT', 'OCT', 'NOV', 'FDA', 'IV', 'ER', 'IPO', 'MILF', 'BUT', 'SSN', 'FIFA', 'USD', 'CPU', 'AT', 'GG', 'Mar'}

pd.set_option('max_columns', None)
pd.set_option('max_rows', None)

# ------


def reddit_aggregation():

    def find_symbols(text):
        text = text.translate(str.maketrans('', '', string.punctuation))
        text.replace('$', '')
        tokenized_text = text.split()
        symbols = []
        for word in tokenized_text:
            if word.isupper() and len(word) <= 5 and word not in blacklist and word in ticker_df.Symbol.values:
                symbols.append(word)
        return symbols

    reddit = praw.Reddit(client_id=reddit_client_id,
                         client_secret=reddit_secret, user_agent=reddit_user_agent)

    new_posts = reddit.subreddit('wallstreetbets').new(limit=1000)

    l_symbol = []

    cannot_find = 0
    can_find = 0
    for post in new_posts:
        if post.created_utc > epoch_cut_off:

            value = find_symbols(post.title)

            if len(value) == 0:
                cannot_find += 1

            else:

                sentence = flair.data.Sentence(post.title)
                sentiment_model.predict(sentence)

                for symbol in value:

                    l_symbol.append(
                        [symbol, sentence.labels[0].value, sentence.labels[0].score, post.created])
                can_find += 1
        else:
            break

    df_stocks = pd.DataFrame(
        l_symbol, columns=['symbol', 'sentiment', 'probability', 'date_created'])

    sentiment_frame = df_stocks.groupby(
        ['symbol', 'sentiment']).size().unstack(fill_value=0)

    probability_frame = df_stocks.groupby(
        'symbol').agg({'probability': 'mean'})
    stock_resultant = pd.merge(sentiment_frame, probability_frame, on="symbol")

    stock_resultant['count'] = stock_resultant['POSITIVE'] + \
        stock_resultant['NEGATIVE']

    stock_resultant.rename(columns={'symbol': 'Symbol', 'NEGATIVE': 'negative_frequency',
                                    'POSITIVE': 'positive_frequency', 'count': 'total_frequency'}, inplace=True)

    stock_resultant = stock_resultant.sort_values(
        by='total_frequency', ascending=False)
    stock_resultant_limit = stock_resultant.head(10)

    json = stock_resultant_limit.to_json(orient='index')

    return json


def twitter_aggregation(target_stock):

    def clean(text):
        whitespace = re.compile(r"\s+")
        web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")
        tick = re.compile(r"(?i)@" + target_stock + "(?=\b)")
        user = re.compile(r"(?i)@[a-z0-9_]+")

        text = whitespace.sub(' ', text)
        text = web_address.sub('', text)
        text = tick.sub(target_stock, text)
        text = user.sub('', text)

        return text

    def get_data(tweets):
        data = {
            'id': tweets['id'],
            'created_at': tweets['created_at'],
            'text': tweets['text']
        }
        return data

    query = '(' + target_stock + ') (lang:en)'
    params = {
        'query': query,
        'max_results': '100',
        'tweet.fields': 'created_at,lang',
    }

    dtformat = '%Y-%m-%dT%H:%M:%SZ'

    twitter_df = pd.DataFrame()

    twitter_current_time = current_time
    twitter_cutoff = cut_off + datetime.timedelta(days=1)

    while twitter_current_time >= twitter_cutoff:
        pastday = twitter_current_time - datetime.timedelta(hours=24)

        if pastday == twitter_cutoff:
            pastday = pastday + datetime.timedelta(hours=5)

        params['start_time'] = pastday.strftime(dtformat)
        params['end_time'] = twitter_current_time.strftime(dtformat)

        response = requests.get(endpoint,
                                params=params,
                                headers=headers)
        twitter_current_time = pastday

        for tweet in response.json()['data']:
            row = get_data(tweet)
            twitter_df = twitter_df.append(row, ignore_index=True)

    probs = []
    sentiments = []

    twitter_df['text'] = twitter_df['text'].apply(clean)

    for tweet in twitter_df['text'].to_list():
        sentence = flair.data.Sentence(tweet)
        sentiment_model.predict(sentence)
        probs.append(sentence.labels[0].score)
        sentiments.append(sentence.labels[0].value)

    twitter_df['probability'] = probs
    twitter_df['sentiment'] = sentiments

    twitter_df['normalized_date'] = pd.to_datetime(
        twitter_df['created_at']).dt.date

    twitter_df = twitter_df.replace('POSITIVE', 1)
    twitter_df = twitter_df.replace('NEGATIVE', 0)

    average_twitter_frame = twitter_df.groupby(
        'normalized_date').agg({'sentiment': 'mean'}).reset_index()

    stock_current_time = current_time + datetime.timedelta(days=1)

    symbol = yfinance.Ticker(target_stock)
    stock = symbol.history(
        start=cut_off.strftime('%Y-%m-%d'),
        end=stock_current_time.strftime('%Y-%m-%d'),
        interval='1d'
    ).reset_index()

    stock = stock.drop(['Open', 'High', 'Low', 'Volume',
                        'Dividends', 'Stock Splits'], axis=1)
    stock.rename(columns={'Date': 'normalized_date',
                          'Close': 'closing price'}, inplace=True)

    stock['normalized_date'] = pd.to_datetime(stock['normalized_date']).dt.date

    combined = average_twitter_frame.merge(
        stock, on='normalized_date', how='left')

    combined_results = combined.to_json(orient='records')

    return combined_results
