from django.shortcuts import render,HttpResponse
import yfinance as yf
from django.utils.dateparse import parse_date
from .models import StockData, DividendData
from django.db import IntegrityError


def home(request):
    indexStockPriceData(request.GET.get('stock'))
    # fetch_and_save_dividend_data(request.GET.get('stock'))
    return HttpResponse("Data indexed successfully")
def indexStockPriceData(stock_ticker):
    # stock_ticker = request.GET.get('stock')
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
        return HttpResponse("Unique constraint violated. Data not indexed")
    except Exception as e:
        print(e)
        return HttpResponse("Data not indexed")
    return HttpResponse("Data indexed successfully")


def fetch_and_save_dividend_data(ticker):
    start_date="1999-01-31"
    end_date="2024-05-02"
    print(ticker)
    # Download dividend data using yfinance
    data = yf.Ticker(ticker).dividends
    print(type(data))

    # Iterate over the dividend data and save it to the database
    for index, dividend in data.items():
        # Convert the index (date) to the correct format
        date = parse_date(index.strftime('%Y-%m-%d'))
        # Save the dividend data to the database
        dividend_data = DividendData(
            ticker=ticker,
            date=date,
            dividend=dividend
        )
        dividend_data.save()

