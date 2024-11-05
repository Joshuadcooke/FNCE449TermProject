import yfinance as yf
import os

# Define the stock tickers and the S&P 500
tickers = ["AAPL", "JPM", "TSLA", "XOM", "META", "^GSPC"]
# Define the periods
pre_covid_period = ("2016-01-01", "2018-01-01")
post_covid_period = ("2022-11-01", "2024-11-01")
# Define the output directory as the Downloads folder
output_dir = os.path.join(os.path.expanduser("~"), "Downloads")

# Function to download and save data
def download_and_save_data(ticker, period, period_name):
    start_date, end_date = period
    data = yf.download(ticker, start=start_date, end=end_date)
    filename = f"{ticker}_{period_name}.csv"
    filepath = os.path.join(output_dir, filename)
    data.to_csv(filepath)
    print(f"Saved {ticker} data for {period_name} period to {filepath}")

# Download data for each stock and period
for ticker in tickers:
    download_and_save_data(ticker, pre_covid_period, "Pre_Covid")
    download_and_save_data(ticker, post_covid_period, "Post_Covid")