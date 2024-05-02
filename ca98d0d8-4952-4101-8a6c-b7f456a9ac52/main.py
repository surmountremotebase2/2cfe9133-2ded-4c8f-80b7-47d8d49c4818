from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize the asset of interest and specify SMA periods
        self.ticker = "AAPL"  # Asset of interest
        self.short_sma_period = 10  # Short-term SMA
        self.long_sma_period = 30  # Long-term SMA
        self.volume_period = 20  # For checking volume increase

    @property
    def assets(self):
        # Assets that the strategy will trade
        return [self.ticker]

    @property
    def interval(self):
        # Data sampling interval
        return "1day"

    @property
    def data(self):
        # Define the data needed for the strategy
        return []

    def run(self, data):
        # Get closing prices and volumes for the ticker
        close_prices = [d[self.ticker]["close"] for d in data["ohlcv"]]
        volumes = [d[self.ticker]["volume"] for d in data["ohlcv"]]

        # Calculate SMAs
        short_sma = SMA(self.ticker, data["ohlcv"], self.short_sma_period)
        long_sma = SMA(self.ticker, data["ohlcv"], self.long_sma_period)

        # Calculate average volume
        avg_volume = sum(volumes[-self.volume_period:]) / self.volume_period

        # Initialize allocation dictionary
        allocation_dict = {self.ticker: 0}

        # Check if there's enough data to make a decision
        if short_sma is not None and long_sma is not None and len(short_sma) > 1 and len(volumes) >= self.volume_period:
            current_volume = volumes[-1]

            # Entry: Short SMA crosses above Long SMA and volume increases significantly
            if short_sma[-1] > long_sma[-1] and short_sma[-2] <= long_sma[-2]:
                if current_volume > 1.5 * avg_volume:  # Check for significant volume increase
                    allocation_dict[self.ticker] = 1  # Buy
                    log("Buying signal: Short SMA crossed above Long SMA with increased volume.")

            # Exit: Short SMA crosses below Long SMA
            elif short_sma[-1] < long_sma[-1] and short_sma[-2] >= long_sma[-2]:
                allocation_dict[self.ticker] = 0  # Sell
                log("Selling signal: Short SMA crossed below Long SMA.")

        return TargetAllocation(allocation_dict)