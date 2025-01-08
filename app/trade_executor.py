import ccxt

class TradeExecutor:
    def __init__(self, api_key=None, api_secret=None):
        """
        Initializes the TradeExecutor with API credentials.
        """
        self.exchange = ccxt.kraken({
            'apiKey': api_key,
            'secret': api_secret,
        })

    def execute_trade(self, symbol: str, side: str, amount: float):
        """
        Executes a market order on the exchange.

        Args:
            symbol (str): Trading pair (e.g., "BTC/USD").
            side (str): "buy" or "sell".
            amount (float): Amount to trade.

        Returns:
            dict: Details of the executed order.
        """
        try:
            order = self.exchange.create_order(
                symbol=symbol,
                type='market',
                side=side,
                amount=amount
            )
            print(f"Trade executed: {order}")
            return order
        except Exception as e:
            print(f"Error executing trade: {e}")
            return None
