import pandas as pd

def sma_crossover_strategy(data: pd.DataFrame, short_window: int = 50, long_window: int = 200):
    """
    Simple Moving Average (SMA) Crossover Strategy.

    Args:
        data (pd.DataFrame): Historical price data with a 'close' column.
        short_window (int): Window size for the short SMA.
        long_window (int): Window size for the long SMA.

    Returns:
        pd.DataFrame: The input DataFrame with 'SMA_short', 'SMA_long', and 'signal' columns.
    """
    # Calculate short-term and long-term SMAs
    data['SMA_short'] = data['close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['close'].rolling(window=long_window).mean()

    # Generate signals: 1 for Buy, -1 for Sell, 0 for Hold
    data['signal'] = 0
    data.loc[data['SMA_short'] > data['SMA_long'], 'signal'] = 1  # Buy signal
    data.loc[data['SMA_short'] <= data['SMA_long'], 'signal'] = -1  # Sell signal

    return data
