import yfinance as yf
data = yf.download("SPY AAPL", period="1mo")
data = yf.Ticker("AAPL").dividends
print(type(data))
