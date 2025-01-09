Crypto Trading Bot

This is a Python-based cryptocurrency trading bot that uses the Simple Moving Average (SMA) Crossover Strategy to make buy/sell decisions. It also includes a Flask web server to monitor the bot and view logs.

Requirements

- Python 3.9+
- A Kraken account with API credentials.

Clone the Repository

```
git clone https://github.com/joegery/trading-bot.git
cd trading-bot
```

Set Up a Virtual Environment

```python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

Install Dependencies

pip install -r requirements.txt

Configure Kraken API

Log in to your Kraken account.

Create API credentials with the following permissions:

- Funds: Query
- Orders and Trades: Query open orders & trades, Create & modify orders, Cancel & close orders
Store your API key and secret securely.

Set Environment Variables

Set your Kraken API credentials as environment variables:

```export KRAKEN_API_KEY=your_api_key
export KRAKEN_API_SECRET=your_api_secret
```

On Windows:

```set KRAKEN_API_KEY=your_api_key
set KRAKEN_API_SECRET=your_api_secret
```

Run the Bot Locally

Start the bot and web server:

```
python test_data_fetching.py
```

Access the Flask web interface:

Home: http://localhost:5000
Logs: http://localhost:5000/logs


Deploying the Bot

Deploy to Heroku
Install the Heroku CLI:

https://devcenter.heroku.com/articles/heroku-cli

Create a Heroku app:

```
heroku create your-app-name
```

Add and commit all changes to Git

Push the app to Heroku:

```
git push heroku master
```

Scale the dyno:

```
heroku ps:scale web=1
```

Access the app:
https://your-app-name.herokuapp.com

Access live logs:
https://your-app-name.herokuapp.com/logs
