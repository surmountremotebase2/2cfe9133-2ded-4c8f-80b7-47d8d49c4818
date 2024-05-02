from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    """
    This trading strategy buys when the asset's price is above its EMA (indicating an uptrend)
    and the RSI is not oversold (above 30), suggesting potential continuation of the upward movement.
    Conversely, it sells (or doesn't buy, in our case, just avoids holding) when the asset's price
    is below its EMA or RSI is overbought (above 70), indicating a potential reversal or correction.
    The strategy focuses on a single asset, for example, 'AAPL'.
    """

    def __init__(self):
        self.asset = "AAPL"  # Focused asset for the strategy.

    @property
    def interval(self):
        return "1day"  # Daily timeframe for the analysis.

    @property
    def assets(self):
        return [self.asset]

    @property
    def data(self):
        return []  # No additional data required outside of default price data.

    def run(self, data):
        """
        Executes the strategy logic to determine the target allocation.

        :param data: Contains historical OHLCV data and other relevant information.
        :return: TargetAllocation object to specify the desired portfolio allocation.
        """
        ohlcv = data["ohlcv"]
        if len(ohlcv) < 15:  # Ensuring there's enough data for our indicators.
            return TargetAllocation({})

        # Calculating EMA and RSI.
        ema_values = EMA(self.asset, ohlcv, length=14)  # 14 periods EMA.
        rsi_values = RSI(self.asset, ohlcv, length=14)  # 14 periods RSI.

        current_price = ohlcv[-1][self.asset]["close"]
        allocation_ratio = 0  # Default no allocation.

        # Determine if the conditions for buying or selling are met.
        if ema_values and rsi_values:  # Ensure indicators calculated correctly.
            latest_ema = ema_values[-1]
            latest_rsi = rsi_values[-1]

            if current_price > latest_ema and latest_rsi > 30:
                allocation_ratio = 1  # Full allocation if trend is up and not oversold.
            elif current_price < latest_ema or latest_rsi > 70:
                allocation_ratio = 0  # No allocation if trend is down or overbought.

        # Log decisions (useful for analysis and debugging).
        log(f"Current Price: {current_price}, EMA: {latest_ema}, RSI: {latest_rsi}, Allocation: {allocation_ratio}")

        return TargetAllocation({self.asset: allocation_ratio})