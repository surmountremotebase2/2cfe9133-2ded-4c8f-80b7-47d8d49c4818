from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["QQQ"]  # Define which ticker this strategy will apply to

    @property
    def interval(self):
        return "1day"  # Use daily data for this strategy
    
    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return []  # This strategy will only use price data, no additional data required

    def run(self, data):
        """
        Executes strategy logic and returns a TargetAllocation object representing
        the desired allocations based on the MACD indicator.

        :param data: Dictionary containing historical market data and other relevant information.
        :return: TargetAllocation object with allocation percentages for each asset. 
        """
        # Define the initial stake in QQQ as 0 (not holding)
        qqq_stake = 0

        # Retrieve the MACD indicator values for QQQ
        macd_data = MACD("QQQ", data["ohlcv"], fast=12, slow=26)
        if macd_data is None:
            # If there's no MACD data available, keep allocations as they are
            return TargetAllocation({"QQQ": qqq_stake})

        macd_line = macd_data["MACD"]
        signal_line = macd_data["signal"]

        # Check if there's enough data to examine the MACD line and the signal line
        if len(macd_line) > 1 and len(signal_line) > 1:
            # Check for MACD line crossing above the signal line (bullish signal)
            if macd_line[-1] > signal_line[-1] and macd_line[-2] < signal_line[-2]:
                log("MACD crossover bullish signal detected, buying QQQ")
                qqq_stake = 1  # Allocate 100% to QQQ
            # Check for MACD line crossing below the signal line (bearish signal)
            elif macd_line[-1] < signal_line[-1] and macd_line[-2] > signal_line[-2]:
                log("MACD crossover bearish signal detected, selling QQQ")
                qqq_stake = 0  # Allocate 0% to QQQ, essentially selling it
        
        # Return the target allocation based on the strategy's decision
        return TargetAllocation({"QQQ": qqq_stake})