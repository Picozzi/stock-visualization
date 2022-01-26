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

# Gather all environment variables from .env
load_dotenv('.env')
reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
reddit_secret = os.getenv('REDDIT_SECRET')
reddit_user_agent = os.getenv('REDDIT_USER_AGENT')
twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
endpoint = 'https://api.twitter.com/2/tweets/search/recent'
headers = {'authorization': f'Bearer {twitter_bearer_token}'}

# --- CONSTANTS ---

# Retrieving current time and calculating 7 days prior
current_time = datetime.datetime.now()
cut_off = current_time - datetime.timedelta(days=7)
epoch_cut_off = cut_off.timestamp()

# Retrieving the Flair text clasification AI model
sentiment_model = flair.models.TextClassifier.load('en-sentiment')

# Gathering all stock tickers on the AMEX, NYSE, and NASDAQ
ticker_df = pd.read_csv('list_of_all_stocks.csv')

# Dictionary of common stock tickers that are also commonly said words
blacklist = {'I', 'ARE',  'ON', 'GO', 'NOW', 'CAN', 'UK', 'SO', 'OR', 'OUT', 'SEE', 'ONE', 'LOVE', 'U', 'STAY', 'HAS', 'BY', 'BIG', 'GOOD', 'RIDE', 'EOD', 'ELON', 'WSB', 'THE', 'A', 'ROPE', 'YOLO', 'TOS', 'CEO', 'DD', 'IT', 'OPEN', 'ATH', 'PM', 'IRS', 'FOR', 'DEC', 'BE', 'IMO', 'ALL', 'RH', 'EV', 'TOS', 'CFO', 'CTO', 'DD', 'BTFD', 'WSB', 'OK', 'PDT', 'RH', 'KYS', 'FD', 'TYS', 'US', 'USA', 'IT', 'ATH', 'RIP', 'BMW', 'GDP', 'OTM',
             'ATM', 'ITM', 'IMO', 'LOL', 'AM', 'BE', 'PR', 'PRAY', 'PT', 'FBI', 'SEC', 'GOD', 'NOT', 'POS', 'FOMO', 'TL;DR', 'EDIT', 'STILL', 'WTF', 'RAW', 'PM', 'LMAO', 'LMFAO', 'ROFL', 'EZ', 'RED', 'BEZOS', 'TICK', 'IS', 'PM', 'LPT', 'GOAT', 'FL', 'CA', 'IL', 'MACD', 'HQ', 'OP', 'PS', 'AH', 'TL', 'JAN', 'FEB', 'JUL', 'AUG', 'SEP', 'SEPT', 'OCT', 'NOV', 'FDA', 'IV', 'ER', 'IPO', 'MILF', 'BUT', 'SSN', 'FIFA', 'USD', 'CPU', 'AT', 'GG', 'Mar'}

pd.set_option('max_columns', None)
pd.set_option('max_rows', None)

# ------


def reddit_aggregation():  # Method to retrieve the top 10 mentioned stocks on r/wallstreetbets

    def find_symbols(text):
        text = text.translate(str.maketrans(
            '', '', string.punctuation))  # Remove punctation
        text.replace('$', '')
        tokenized_text = text.split()  # tokenize
        symbols = []
        for word in tokenized_text:
            if word.isupper() and len(word) <= 5 and word not in blacklist and word in ticker_df.Symbol.values:
                symbols.append(word)
        return symbols

    # Retrieve a reddit client
    reddit = praw.Reddit(client_id=reddit_client_id,
                         client_secret=reddit_secret, user_agent=reddit_user_agent)

    # Gather the 1000 most recent posts on r/wallstreetbets
    new_posts = reddit.subreddit('wallstreetbets').new(limit=1000)

    l_symbol = []

    # Variables for logging purposes
    cannot_find = 0
    can_find = 0

    # Looping through to find posts from the past 7 days
    for post in new_posts:
        if post.created_utc > epoch_cut_off:

            value = find_symbols(post.title)

            if len(value) == 0:
                cannot_find += 1

            else:
                # Applying Flair model to Reddit posts
                sentence = flair.data.Sentence(post.title)
                sentiment_model.predict(sentence)

                for symbol in value:

                    l_symbol.append(
                        [symbol, sentence.labels[0].value, sentence.labels[0].score, post.created])
                can_find += 1
        else:
            break

    # Adding all data into a dataframe

    df_stocks = pd.DataFrame(
        l_symbol, columns=['symbol', 'sentiment', 'probability', 'date_created'])

    # Grouping stocks by symbol and gathering number of positive and negative mentions
    sentiment_frame = df_stocks.groupby(
        ['symbol', 'sentiment']).size().unstack(fill_value=0)

    # Calculating mean certainty for each symbol
    probability_frame = df_stocks.groupby(
        'symbol').agg({'probability': 'mean'})
    stock_resultant = pd.merge(sentiment_frame, probability_frame, on="symbol")

    # Calculating total mentions
    stock_resultant['count'] = stock_resultant['POSITIVE'] + \
        stock_resultant['NEGATIVE']

    stock_resultant.rename(columns={'symbol': 'Symbol', 'NEGATIVE': 'negative_frequency',
                                    'POSITIVE': 'positive_frequency', 'count': 'total_frequency'}, inplace=True)

    # Sort values by number of mentions
    stock_resultant = stock_resultant.sort_values(
        by='total_frequency', ascending=False)
    stock_resultant_limit = stock_resultant.head(10)

    json = stock_resultant_limit.to_json(orient='index')

    return json


def twitter_aggregation(target_stock):

    # Method to clean Tweet using regex
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

    # Method to format tweet data before entering the dataframe
    def get_data(tweets):
        data = {
            'id': tweets['id'],
            'created_at': tweets['created_at'],
            'text': tweets['text']
        }
        return data

    # Query and parameters for Twitter API
    query = '(' + target_stock + ') (lang:en)'
    params = {
        'query': query,
        'max_results': '100',
        'tweet.fields': 'created_at,lang',
    }

    # Specific datetime format Twitter uses
    dtformat = '%Y-%m-%dT%H:%M:%SZ'

    twitter_df = pd.DataFrame()

    twitter_current_time = current_time
    twitter_cutoff = cut_off
    flag = True

    # Gathering the top 100 tweets for each day in the past 7 days
    while flag:
        pastday = twitter_current_time - datetime.timedelta(hours=24)

        if pastday <= twitter_cutoff:
            pastday = twitter_cutoff + datetime.timedelta(hours=6)
            flag = False
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

    # Applying Flair model to Tweets
    for tweet in twitter_df['text'].to_list():
        sentence = flair.data.Sentence(tweet)
        sentiment_model.predict(sentence)
        probs.append(sentence.labels[0].score)
        sentiments.append(sentence.labels[0].value)

    # Adding to dataframe
    twitter_df['probability'] = probs
    twitter_df['sentiment'] = sentiments

    # Normalizing date to remove the time portion (we only care about which day they were created)
    twitter_df['normalized_date'] = pd.to_datetime(
        twitter_df['created_at']).dt.date

    # Replacing 'POSITIVE' and 'NEGATIVE' with their numerical equivalents
    twitter_df = twitter_df.replace('POSITIVE', 1)
    twitter_df = twitter_df.replace('NEGATIVE', 0)

    # Group average sentiment by day
    average_twitter_frame = twitter_df.groupby(
        'normalized_date').agg({'sentiment': 'mean'}).reset_index()

    stock_current_time = current_time + datetime.timedelta(days=1)

    # Calculate the stock price over the past 7 days using Yahoo! Finance
    symbol = yfinance.Ticker(target_stock)
    stock = symbol.history(
        start=cut_off.strftime('%Y-%m-%d'),
        end=stock_current_time.strftime('%Y-%m-%d'),
        interval='1d'
    ).reset_index()

    # Drop any columns that are not required
    stock = stock.drop(['Open', 'High', 'Low', 'Volume',
                        'Dividends', 'Stock Splits'], axis=1)
    stock.rename(columns={'Date': 'normalized_date',
                          'Close': 'closing price'}, inplace=True)

    # Normalize the date, the same as the Twitter data
    stock['normalized_date'] = pd.to_datetime(stock['normalized_date']).dt.date

    # Merge the two dataframes to compare daily Twitter sentiment with daily stock price
    combined = average_twitter_frame.merge(
        stock, on='normalized_date', how='left')

    combined_results = combined.to_json(orient='records')

    return combined_results
