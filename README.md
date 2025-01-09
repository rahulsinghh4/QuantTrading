# QuantTrading
Quantitative Trading Bot and Monte Carlo Simulations
The main program automates trades using Python and QuantConnect


# Strategy
The main trading strategy is based on identifying key historic trading levels (market highs).
If a breakout occurs, we buy (can adjust how much relative to local market high).
A trailing stop loss is created in order to mitigate losses (adjustable) with an initial stop risk and trailing stop risk percentage.

A dynamic lookback timeframe helps to determine what qualifies as a breakout — greater market volatility results in a longer necessary lookback timeframe.

# Backtesting
Primary backtesting was performed on SPY over a period of 5 years.

# Target
The goal of this program was to optimize the probabilistic Sharpe ratio (PSR), which defines the likelihood of a given method beating the expected market outcome. A secondary goal was to either match or outperform the market in terms of overall return over any large-scale backtesting period. 

# Monte Carlo Simulation
The program simulates 10,000 possible outcomes based on a random walk with drift and cross-correlations by calculating drift and diffusion coefficients based on historical price data. 
The average of these simulations is then compared with the actual price trajectory (if available).
The Monte Carlo Simulation is based off of Geometric Brownian Motion with Drift.
