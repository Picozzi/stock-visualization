# Stock Analysis and Algorithmic Trading

A web application that aggregates the top 10 mentioned stocks on the Reddit coommunity 'wallstreetbets' and performs sentiment analysis to determine whether overall sentiment of the stock is bullish or bearish.

# Motivation

The motivation behind this application was to create a way to integrate social media data into algorithmic trading. The current implementation simply aggregates and analyzes the most mentioned stocks. Future implementations will implement analysis into a moment strategy algorithm.

## How to Use

Due to size constraints, this project only runs locally. Please clone the repository and run flask and yarn.

###### Steps

1. cd into visualization
2. run yarn start
3. in a new tab, in the base directory run source venv/bin/activate
4. run the following command: flask run (it should open on port:5001)
5. for data to appear, the daily_data_collection.py must be run for the day

## Contributing

Feel free to contribute to this project and make changes that better fit your needs, a contributing guideline will be released soon.

## Pull Requests

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Built With

- Python
- React
- Flask
- MongoDB
- yfinance
- flair

## License

Apache 2.0

Apache © Picozzi
