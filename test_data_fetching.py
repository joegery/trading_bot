from flask import Flask
from threading import Thread
import time
import logging

# Import your bot logic
from app.data_fetcher import DataFetcher
from app.strategies import sma_crossover_strategy
from app.trade_executor import TradeExecutor

# Set up logging
logging.basicConfig(
    filename='logs/trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
    trade_amount = 0.00001  # Example: Trade 0.00001 BTC

    while True:
        try:
            # Fetch account balances
            balance = executor.exchange.fetch_balance()
            usdt_balance = balance['total'].get('USDT', 0)
            btc_balance = balance['total'].get('BTC', 0)

            logging.info(f"Available USDT balance: {usdt_balance}")
            logging.info(f"Available BTC balance: {btc_balance}")

            # Fetch historical data
            since = int(time.time() * 1000) - (60 * 60 * 1000)  # 1-hour ago
            data = fetcher.fetch_historical_data(symbol, timeframe, since)

            if data is not None:
                # Apply SMA Crossover Strategy
                strategy_result = sma_crossover_strategy(data)

                # Get the most recent signal
                latest_signal = strategy_result['signal'].iloc[-1]

                if latest_signal == 1:  # Buy signal
                    if usdt_balance >= trade_amount * 100:  # Ensure enough USDT for trade
                        logging.info("Placing a BUY order...")
                        executor.execute_trade(symbol, "buy", trade_amount)
                    else:
                        logging.warning("Insufficient USDT balance to place a BUY order.")
                
                elif latest_signal == -1:  # Sell signal
                    if btc_balance >= trade_amount:  # Ensure enough BTC for trade
                        logging.info("Placing a SELL order...")
                        executor.execute_trade(symbol, "sell", trade_amount)
                    else:
                        logging.warning("Insufficient BTC balance to place a SELL order.")
                
                else:
                    logging.info("No trade signal. Holding position.")
            
            # Sleep before the next iteration
            time.sleep(300)  # Wait 5 minutes before the next cycle

        except Exception as e:
            logging.error(f"Error occurred: {e}")
            time.sleep(60)  # Wait and retry after a minute

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=5000)).start()
    run_bot()
