# import modules
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz
import warnings
warnings.filterwarnings('ignore')

# main variables
stock_name = 'META'
start_date = '2010-01-01'
end_date = '2020-10-31'
pred_end_date = '2020-12-31'
scen_size = 10000

def simulate_stock_prices(stock_name, start_date, end_date, pred_end_date, scen_size):
    try:
        # Convert dates to timezone-aware datetime objects
        utc = pytz.UTC
        end_date_dt = pd.to_datetime(end_date).tz_localize(utc)
        pred_end_date_dt = pd.to_datetime(pred_end_date).tz_localize(utc)
        
        # Verify dates are in correct order
        if end_date_dt >= pred_end_date_dt:
            raise ValueError("Prediction end date must be after training end date")
        
        # download and prepare data
        prices = yf.download(tickers=stock_name, start=start_date, end=pred_end_date)['Adj Close']
        if prices.empty:
            raise ValueError("No data downloaded for the specified stock and date range")
        
        # Split into train and test sets using indexer
        train_mask = prices.index <= end_date_dt
        test_mask = prices.index > end_date_dt
        
        train_set = prices[train_mask]
        test_set = prices[test_mask]
        
        if len(train_set) < 2:
            raise ValueError("Not enough training data")
            
        # Calculate daily returns, dropping NA values
        daily_returns = ((train_set / train_set.shift(1)) - 1).dropna()
        
        # Parameter Assignments
        So = float(train_set.iloc[-1])  # Last known price
        dt = 1  # day
        
        print(f"Initial stock price (So): {So:.2f}")
        
        # Calculate number of business days for prediction
        business_days = pd.bdate_range(start=end_date_dt, 
                                     end=pred_end_date_dt,
                                     inclusive='right')  # Exclude start date as it's the last known price
        n_of_wkdays = len(business_days)
        
        print(f"Number of business days for prediction: {n_of_wkdays}")
        print(f"Test set size: {len(test_set)}")
        
        if n_of_wkdays <= 0:
            raise ValueError(f"No business days between {end_date} and {pred_end_date}")
            
        T = n_of_wkdays
        N = T / dt
        t = np.arange(1, int(N) + 1)
        
        # Calculate mu and sigma from daily returns
        mu = float(np.mean(daily_returns))
        sigma = float(np.std(daily_returns, ddof=1))
        
        print(f"Calculated parameters: mu={mu:.4f}, sigma={sigma:.4f}")
        
        # Generate random walks
        np.random.seed(42)  # For reproducibility
        b = {str(scen): np.random.normal(0, 1, int(N)) for scen in range(1, scen_size + 1)}
        W = {str(scen): b[str(scen)].cumsum() for scen in range(1, scen_size + 1)}
        
        # Calculating drift and diffusion components
        drift = (mu - 0.5 * sigma ** 2) * t
        diffusion = {str(scen): sigma * W[str(scen)] for scen in range(1, scen_size + 1)}
        
        # Making the predictions
        S = np.array([So * np.exp(drift + diffusion[str(scen)]) for scen in range(1, scen_size + 1)])
        
        # Calculate prediction as mean of simulations
        S_pred = np.mean(S, axis=0)
        
        # Create final dataframe
        final_df = pd.DataFrame(index=business_days)
        final_df['real'] = test_set
        final_df['pred'] = S_pred
        
        # Calculate MSE only for overlapping dates
        valid_mask = pd.notna(final_df['real'])
        mse = np.mean((final_df.loc[valid_mask, 'pred'] - final_df.loc[valid_mask, 'real']) ** 2)
        
        print(f"Simulation completed successfully. MSE: {mse:.2f}")
        print("\nFirst few predictions:")
        print(final_df.head())
        
        return final_df, S, mse, business_days
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return None, None, None, None

def plot_simulations(final_df, S, mse, business_days, stock_name, scen_size):
    try:
        # Set style parameters
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = [12, 10]
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1)
        
        # Plot simulations
        ax1.set_title(f'Monte-Carlo Simulation: {scen_size} simulations\nAsset: {stock_name}', 
                     fontsize=12, pad=10)
        ax1.set_ylabel('USD Price')
        ax1.set_xlabel('Date')
        
        # Plot only a subset of simulations for better visualization
        plot_scenarios = min(100, scen_size)
        
        # Plot simulations with alpha for transparency
        for i in range(plot_scenarios):
            ax1.plot(business_days, S[i], 'b-', alpha=0.1, linewidth=0.5)
            
        # Plot real prices on top
        mask = pd.notna(final_df['real'])
        ax1.plot(final_df[mask].index, final_df[mask]['real'], 'r-', linewidth=2, label='Real Price')
        ax1.legend()
        
        # Plot predictions vs real prices
        ax2.set_title(f'Predicted Price vs Real Price\nMean Squared Error (MSE): {mse:.2f}', 
                     fontsize=12, pad=10)
        ax2.set_ylabel('USD Price')
        ax2.set_xlabel('Date')
        
        # Plot with different colors and styles
        ax2.plot(final_df[mask].index, final_df[mask]['real'], 'r-', linewidth=2, label='Real Price')
        ax2.plot(final_df.index, final_df['pred'], 'b--', linewidth=2, label='Predicted Price')
        ax2.legend()
        
        # Adjust layout to prevent overlap
        plt.tight_layout()
        
        # Rotate x-axis labels for better readability
        for ax in [ax1, ax2]:
            ax.tick_params(axis='x', rotation=45)
            
        return fig
    
    except Exception as e:
        print(f"Error in plotting: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# Run simulation
print("Starting simulation...")
print(f"Stock: {stock_name}")
print(f"Training period: {start_date} to {end_date}")
print(f"Prediction period: {end_date} to {pred_end_date}")
print(f"Number of scenarios: {scen_size}")

final_df, S, mse, business_days = simulate_stock_prices(
    stock_name, start_date, end_date, pred_end_date, scen_size
)

if final_df is not None:
    print("Creating plots...")
    fig = plot_simulations(final_df, S, mse, business_days, stock_name, scen_size)
    if fig is not None:
        plt.show()
    else:
        print("Failed to create plots")
else:
    print("Simulation failed")