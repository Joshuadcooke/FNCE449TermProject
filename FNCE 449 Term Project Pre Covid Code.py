import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter  # Import PercentFormatter for percentage display

# Define URLs for the CSV files stored on GitHub
urls = {
    "AAPL": "https://raw.githubusercontent.com/Joshuadcooke/TermProjectData/main/AAPL_Pre_Covid.csv",
    "JPM": "https://raw.githubusercontent.com/Joshuadcooke/TermProjectData/main/JPM_Pre_Covid.csv",
    "TSLA": "https://raw.githubusercontent.com/Joshuadcooke/TermProjectData/main/TSLA_Pre_Covid.csv",
    "XOM": "https://raw.githubusercontent.com/Joshuadcooke/TermProjectData/main/XOM_Pre_Covid.csv",
    "META": "https://raw.githubusercontent.com/Joshuadcooke/TermProjectData/main/META_Pre_Covid.csv",
    "S&P 500": "https://raw.githubusercontent.com/Joshuadcooke/TermProjectData/main/%5EGSPC_Pre_Covid.csv"
}

# Load data into a dictionary
stock_data = {}
for ticker, url in urls.items():
    stock_data[ticker] = pd.read_csv(url, parse_dates=['Date'], index_col='Date')

# Calculate daily returns for each stock
daily_returns = pd.DataFrame()
for ticker, df in stock_data.items():
    df['Daily Return'] = df['Close'].pct_change() * 100
    daily_returns[ticker] = df['Daily Return']

# Define tickers (excluding S&P 500) for sector rotation
tickers = ["AAPL", "JPM", "TSLA", "XOM", "META"]

# Create an empty DataFrame to track positions for each day and another for the trade log
positions = pd.DataFrame(index=daily_returns.index, columns=tickers)
trade_log = pd.DataFrame(index=daily_returns.resample('ME').mean().index, columns=tickers)  # Log of trades

# Loop through each month to set positions based on previous month's performance
for date in daily_returns.resample('ME').mean().index:  # Monthly frequency for selecting top stocks
    if date == daily_returns.resample('ME').mean().index[0]:  # Skip the first month since there's no prior month to base on
        continue
    
    # Get the previous month's end date
    previous_date = daily_returns.resample('ME').mean().index[daily_returns.resample('ME').mean().index.get_loc(date) - 1]
    
    # Calculate the previous month's returns for each stock
    month_returns = pd.DataFrame()
    for ticker in tickers:
        month_returns[ticker] = stock_data[ticker]['Close'].resample('ME').ffill().pct_change() * 100

    # Filter for stocks with positive returns only and select top performers
    positive_returns = month_returns.loc[previous_date, tickers][month_returns.loc[previous_date, tickers] > 0]
    top_stocks = positive_returns.sort_values(ascending=False).head(3).index  # Get up to 3 stocks with positive returns

    # Ensure end-of-month sell only happens within available dates
    end_of_month_date = date - pd.DateOffset(days=1)
    if end_of_month_date in positions.index:
        positions.loc[end_of_month_date, :] = 0  # Sell all positions on the last day of each month

    # Allocate for the new month within available dates
    month_start_date = date
    month_end_date = date + pd.DateOffset(months=1) - pd.DateOffset(days=1)
    valid_dates = positions.index.intersection(pd.date_range(month_start_date, month_end_date))
    
    for ticker in tickers:
        if ticker in top_stocks:
            positions.loc[valid_dates, ticker] = 1  # Buy/Hold top performer for the month
            trade_log.loc[date, ticker] = "+1"  # Log buy action
        else:
            positions.loc[valid_dates, ticker] = 0  # No position
            trade_log.loc[date, ticker] = "0"  # Log no trade

# Calculate average monthly returns for each stock in the pre-COVID period and convert to percentage
monthly_returns = daily_returns.resample('ME').apply(lambda x: (1 + x / 100).prod() - 1)
pre_covid_avg_returns = monthly_returns[tickers].mean() * 100  # Convert to percentage

print("Average Monthly Returns Pre-COVID (2016–2018):")
print(pre_covid_avg_returns.apply(lambda x: f"{x:.2f}%"))  # Display as percentage

# Calculate the cumulative portfolio return using daily returns
portfolio_daily_returns = (daily_returns[tickers] * positions.shift(1)).sum(axis=1) / 3  # Divide by 3 for equal allocation across top 3
cumulative_portfolio_return = (1 + portfolio_daily_returns / 100).cumprod() - 1

# Calculate the cumulative return for S&P 500 on a daily basis (consistent with the portfolio calculation)
sp500_daily_returns = daily_returns["S&P 500"]
cumulative_sp500_return = (1 + sp500_daily_returns / 100).cumprod() - 1

# Calculate the ending cumulative returns and the difference
portfolio_ending_cumulative_return = cumulative_portfolio_return.iloc[-1] * 100  # Convert to percentage
sp500_ending_cumulative_return = cumulative_sp500_return.iloc[-1] * 100  # Convert to percentage
return_difference = portfolio_ending_cumulative_return - sp500_ending_cumulative_return

# Print the ending cumulative returns and the difference
print(f"Ending Cumulative Return of Portfolio: {portfolio_ending_cumulative_return:.2f}%")
print(f"Ending Cumulative Return of S&P 500: {sp500_ending_cumulative_return:.2f}%")
print(f"Difference in Cumulative Return (Portfolio - S&P 500): {return_difference:.2f}%")

# Display the trade log in a table
trade_log = trade_log.fillna("0")  # Replace NaNs with "0"

# Figure 1: Trade Log Table with Enhanced Styling
fig1, ax1 = plt.subplots(figsize=(12, len(trade_log) * 0.5))  # Adjust height based on number of rows
ax1.axis('off')  # Hide the axes

# Create the table with formatting
table = ax1.table(cellText=trade_log.values,
                  colLabels=trade_log.columns,
                  rowLabels=trade_log.index.strftime('%Y-%m-%d'),
                  cellLoc='center',
                  loc='center')

# Style table
header_color = colors.to_rgba('darkblue', alpha=0.8)
header_text_color = 'white'
for (i, j), cell in table.get_celld().items():
    if i == 0:
        cell.set_fontsize(10)
        cell.set_text_props(weight='bold', color=header_text_color)
        cell.set_facecolor(header_color)  # Column header styling
    elif j == -1:
        cell.set_fontsize(10)
        cell.set_text_props(weight='bold', color=header_text_color)
        cell.set_facecolor(header_color)  # Row header styling
    elif i % 2 == 1:  # Banding: Apply alternating colors to rows
        cell.set_facecolor(colors.to_rgba('lightgray', alpha=0.3))
    else:
        cell.set_facecolor('white')

# Add title directly above the table using fig.text
fig1.text(0.5, 0.70, "Monthly Trade Log (+1 = Buy and 0 = No Position)", ha='center', fontsize=12, weight='bold')

# Figure 2: Portfolio vs S&P 500 Cumulative Returns
fig2, ax2 = plt.subplots(figsize=(10, 6))
cumulative_portfolio_return.plot(label='Portfolio Return - Sector Rotation Strategy (Daily)', color='b', ax=ax2)
cumulative_sp500_return.plot(label='S&P 500 Return (Daily)', color='r', ax=ax2)
ax2.set_xlabel('Date')
ax2.set_ylabel('Cumulative Return')
ax2.yaxis.set_major_formatter(PercentFormatter(xmax=1))  # Display y-axis as percentage
ax2.set_title('Cumulative Portfolio Return vs S&P 500')
ax2.legend()
ax2.grid()

# Show both figures
plt.show()