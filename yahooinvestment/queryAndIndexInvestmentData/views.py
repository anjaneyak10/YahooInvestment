from django.shortcuts import render,HttpResponse
import yfinance as yf
from django.utils.dateparse import parse_date
from .models import StockData, DividendData
from django.db import IntegrityError


def home(request):
    if indexStockPriceData(request.GET.get('stock')) and fetch_and_save_dividend_data(request.GET.get('stock')):
        return HttpResponse("Data indexed successfully")
    return HttpResponse("Error indexing data")

def indexStockPriceData(stock_ticker):
    try:
        data = yf.download(stock_ticker, start="2022-12-31", end="2024-05-02")
        for index, row in data.iterrows():
            date_str = index.strftime('%Y-%m-%d')
            stock_data = StockData(
                ticker=stock_ticker,
                date=parse_date(date_str),
                open_price=row['Open'],
                high_price=row['High'],
                low_price=row['Low'],
                close_price=row['Close'],
                volume=row['Volume'],
                adj_close_price=row['Adj Close']
            )
            stock_data.save()
    except IntegrityError:
        return False
    except Exception as e:
        print(e)
        return False
    return True


def fetch_and_save_dividend_data(ticker):
    try:
        start_date="1999-01-31"
        end_date="2024-05-02"
        data = yf.Ticker(ticker).dividends
        for index, dividend in data.items():
            date = parse_date(index.strftime('%Y-%m-%d'))
            dividend_data = DividendData(
                ticker=ticker,
                date=date,
                dividend=dividend
            )
            dividend_data.save()
    except Exception as e:
        print(e)
        return False
    return True
