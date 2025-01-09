from flask import Flask
from threading import Thread
import time
import logging
import os

from app.data_fetcher import DataFetcher
from app.strategies import sma_crossover_strategy
from app.trade_executor import TradeExecutor

# logging
logging.basicConfig(
    filename='logs/trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# go to https://jgery-bot-0e24270cbb69.herokuapp.com/ to see if app is running
# go to https://jgery-bot-0e24270cbb69.herokuapp.com/logs to see logs

# Flask app for monitoring
app = Flask(__name__)

@app.route("/")
def home():
    return "Trading bot is running."

@app.route("/logs")
def view_logs():
    try:
        with open("logs/trading_bot.log", "r") as log_file:
            return f"<pre>{log_file.read()}</pre>"
    except Exception as e:
        return f"Error reading logs: {e}"

def run_bot():
    fetcher = DataFetcher()
    executor = TradeExecutor(api_key="qRCV4WdBM/HAIqpxhgxLa37On9sI6dsToHyks26qNfWf1t0SAqpxmy6R", api_secret="KXLacJceW8ZyX+T9aFgzYQWwu1C6d3VKKmiMdtdiks5ZkbmAEkh+6hklfeseMgHEVwXD4ldfKg0Oqbrz5eBfVg==")

    symbol = "BTC/USDT"
    timeframe = "1h"
    trade_amount = 0.00001  

    while True:
        try:
            balance = executor.exchange.fetch_balance()
            usdt_balance = balance['total'].get('USDT', 0)
            btc_balance = balance['total'].get('BTC', 0)

            logging.info(f"Available USDT balance: {usdt_balance}")
            logging.info(f"Available BTC balance: {btc_balance}")

            # historical data
            since = int(time.time() * 1000) - (60 * 60 * 1000)  # 1-hour ago
            data = fetcher.fetch_historical_data(symbol, timeframe, since)

            if data is not None:
                strategy_result = sma_crossover_strategy(data)

                # Get the most recent signal
                latest_signal = strategy_result['signal'].iloc[-1]

                if latest_signal == 1:  # Buy
                    if usdt_balance >= trade_amount * 100: 
                        logging.info("Placing a BUY order...")
                        executor.execute_trade(symbol, "buy", trade_amount)
                    else:
                        logging.warning("Insufficient USDT balance to place a BUY order.")
                
                elif latest_signal == -1:  # Sell
                    if btc_balance >= trade_amount: 
                        logging.info("Placing a SELL order...")
                        executor.execute_trade(symbol, "sell", trade_amount)
                    else:
                        logging.warning("Insufficient BTC balance to place a SELL order.")
                
                else:
                    logging.info("No trade signal. Holding position.")
            
            time.sleep(300)  # Wait 5 minutes before the next cycle

        except Exception as e:
            logging.error(f"Error occurred: {e}")
            time.sleep(60)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    # Start Flask in a separate thread
    Thread(target=lambda: app.run(host="0.0.0.0", port=port)).start()
    # Start the bot
    run_bot()
