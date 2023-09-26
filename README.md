# Script analyzing cryptocurrency 

---
## Project Description
This code represents a script for analyzing cryptocurrency market data (specifically, the BTC/USDT pair) and executing trading operations based on predefined strategies. The code analyzes historical Bitcoin price data, simulating the buying and selling of assets based on various criteria. Below is a description of the key components and functions in this code.

## Input Data
folder_path: Path to the folder containing historical Bitcoin price data files in .csv format.

## Settings and Parameters
* initial_balance: Initial account balance for simulating trading.


## Data Processing
* Reading and combining historical data from .csv files into a single DataFrame (combined_data).
* Determining the list of buy orders (buy_orders).
* Processing data in blocks and executing the trading strategy in the process_data_block() function.
* Tracking profitable trades, total profit, and displaying statistics for each data block.

## Simulation of Trading Strategy
* The strategy is based on changes in the asset's price relative to the purchase price.
* Under specific conditions, the code creates buy orders and executes asset trades.
* Trades, their profits, and other information are saved in the trades_df DataFrame.

## Data Visualization
* Creating a plot with points representing buy and sell prices of assets.
* Each point is labeled with a unique trade identifier.
* The plot allows for visual tracking of trades on a time axis.

## Data Saving
* Saving trade data to the trades.csv file in CSV format.
* Memory is released after the code execution is completed.

# Notes
* This code is an example of simulating a trading strategy and is not intended for real trading.