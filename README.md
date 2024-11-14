# QuantTrading
Quantitative Trading Bot and Monte Carlo Simulations
The main program automates trades using Python and QuantConnect


# Strategy
The main trading strategy is based on identifying key historic trading levels (market highs)
If a breakout occurs, we buy (can adjust how much relative to local market high)
A trailing stop loss is created in order to mitigate losses (adjustable) with an initial stop risk and trailing stop risk percentage

A dynamic lookback timeframe helps to determine what qualifies as a breakout — greater market volatility results in a longer necessary lookback timeframe

# Backtesting
Primary backtesting was performed on SPY over a 

# Monte Carlo Simulation
