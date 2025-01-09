# QuantTrading
Quantitative Trading Bot and Monte Carlo Simulations
The main program automates trades using Python and QuantConnect

## Overview
This QuantConnect algorithm implements a dynamic breakout trading strategy for the S&P 500 (SPY) with adaptive lookback periods and trailing stop losses. The strategy adjusts its lookback period based on market volatility and implements risk management through trailing stop orders.

## Strategy Details

### Core Components
1. **Dynamic Lookback Period**
   - Base lookback period: 10 days
   - Range: 10-360 days
   - Adjusts automatically based on volatility changes
   - Higher volatility → Longer lookback period
   - Lower volatility → Shorter lookback period

2. **Entry Conditions**
   - Monitors daily high prices within the lookback period
   - Enters position when current price exceeds the highest price in the lookback period
   - Takes full position size (100% of available capital)

3. **Risk Management**
   - Initial stop loss: 2% below breakout level
   - Trailing stop loss: 6% below current price
   - Stop loss automatically adjusts upward as price increases

## Implementation Details

### Parameters
- Initial Capital: $100,000
- Trading Resolution: Daily
- Market: SPY (S&P 500 ETF)
- Backtest Period: 2019-11-14 to 2024-11-14
- Trading Schedule: Daily, 30 minutes after market open

### Risk Parameters
```python
initialStopRisk = 0.98  # Initial 2% stop loss
trailingStopRisk = 0.94  # Trailing 6% stop loss
```

### Lookback Period Calculation
The strategy dynamically adjusts the lookback period using the following formula:
```python
deltaVolatility = (todayVolatility - yesterdayVolatility) / todayVolatility
lookback = currentLookback * (1 + deltaVolatility)
```

## Key Features

1. **Volatility Adaptation**
   - Automatically adjusts to market conditions
   - Provides flexibility in different market environments
   - Helps avoid false breakouts during high volatility periods

2. **Risk Control**
   - Two-tiered stop loss system
   - Initial stop loss for immediate risk control
   - Trailing stop loss to protect profits
   - Automatic stop price updates

3. **Position Management**
   - Full position sizing on breakout signals
   - Automated position exit through stop orders
   - No manual intervention required

## Usage

1. **Setup**
   ```python
   self.SetStartDate(2019, 11, 14)
   self.SetEndDate(2024, 11, 14)
   self.SetCash(100000)
   ```

2. **Market Data**
   - Uses daily resolution data
   - Requires minimum 360 days of historical data (maximum lookback period)
   - Processes market data 30 minutes after open

3. **Monitoring**
   - Plots current price
   - Plots stop loss levels
   - Tracks highest achieved price

## Performance Tracking
The algorithm includes built-in plotting functionality:
- Main price chart
- Stop loss levels
- Entry and exit points

## Dependencies
- QuantConnect API
- NumPy for statistical calculations
- Standard Python libraries

## Risk Considerations

1. **Market Conditions**
   - Strategy performs best in trending markets
   - May experience frequent stops in choppy markets
   - Volatility-based adjustments help mitigate false signals

2. **Position Sizing**
   - Uses full capital allocation on entry
   - Consider adjusting position sizing based on risk tolerance
   - Monitor account leverage and margin requirements

3. **Stop Loss Impact**
   - 2% initial risk per trade
   - Trailing stop may result in larger gains or losses
   - Consider adjusting stop percentages based on market conditions

## Customization Options

1. **Lookback Parameters**
   ```python
   self.ceiling = 360  # Maximum lookback period
   self.floor = 10    # Minimum lookback period
   ```

2. **Risk Parameters**
   ```python
   self.initialStopRisk = 0.98   # Initial stop loss percentage
   self.trailingStopRisk = 0.94  # Trailing stop loss percentage
   ```

3. **Trading Schedule**
   - Can be modified to trade at different times
   - Currently set to 30 minutes after market open
  

## Target
The goal of this program was to optimize the probabilistic Sharpe ratio (PSR), which defines the likelihood of a given method beating the expected market outcome. A secondary goal was to either match or outperform the market in terms of overall return over any large-scale backtesting period. 


## Limitations and Considerations

1. **Market Impact**
   - Strategy assumes sufficient liquidity
   - May need adjustments for less liquid securities
   - Consider transaction costs and slippage

2. **Data Requirements**
   - Requires consistent daily price data
   - Historical data needed for lookback calculation
   - May need adjustment for gaps or missing data

3. **Market Regimes**
   - Performance may vary in different market conditions
   - Consider adding market regime filters
   - May need adjustment during high volatility periods

## Future Improvements

1. **Position Sizing**
   - Implement dynamic position sizing based on volatility
   - Add risk-based position scaling
   - Consider portfolio-level risk management

2. **Entry Conditions**
   - Add volume confirmation
   - Implement additional technical indicators
   - Consider fundamental data integration

3. **Risk Management**
   - Add time-based exit rules
   - Implement profit taking levels
   - Add correlation-based risk adjustments


## Monte Carlo Simulation
The program simulates 10,000 possible outcomes based on a random walk with drift and cross-correlations by calculating drift and diffusion coefficients based on historical price data. 
The average of these simulations is then compared with the actual price trajectory (if available).
The Monte Carlo Simulation is based off of Geometric Brownian Motion with Drift.
