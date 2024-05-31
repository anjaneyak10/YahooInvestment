from django.shortcuts import render
from django.conf import settings
from .models import StockData
import json
from datetime import datetime, timedelta, date
# This is the function that will be called when /investments is called
def investments_view(request):
    investment = settings.STATIC_INVESTMENTS
    investment_data = get_total_investment_data(investment)
    print(investment_data[1])
    # print(investment_data[2])
    # print(investment_data[3], "pie chart data")
    return render(request, 'investmentDashboard/investments.html', {
        'static_investments': investment_data[0],
        'plot_data': json.dumps(investment_data[1]),
        'investment_data': investment_data[2],
        'pie_chart_data': json.dumps(investment_data[3])
    })

# This is the function that will be called when /fidelity is called
def fidelity_view(request):
    fidelity_investments = [investment for investment in settings.STATIC_INVESTMENTS if investment['broker'] == 'Fidelity']
    investment_data = get_investment_data(fidelity_investments)
    print(investment_data[1])
    return render(request, 'investmentDashboard/fidelity.html', {
        'static_investments': investment_data[0],
        'plot_data': json.dumps(investment_data[1]),
        'investment_data': investment_data[2],
        'pie_chart_data': json.dumps(investment_data[3])
    })

# This is the function that will be called when /schwab is called
def schwab_view(request):
    schwab_investments = [investment for investment in settings.STATIC_INVESTMENTS if investment['broker'] == 'Schwab']
    investment_data = get_investment_data(schwab_investments)
    return render(request, 'investmentDashboard/schwab.html', {
        'static_investments': investment_data[0],
        'plot_data': json.dumps(investment_data[1]),
        'investment_data': investment_data[2],
        'pie_chart_data': json.dumps(investment_data[3])
    })

# This function is used to get the investments and then plot the combined value for all investments and the distribution of the investments
def get_total_investment_data(investments):
    plot_data = {}
    investment_data = {}
    close_prices = []
    dates = []

    for investment in investments:
        start_date = date(2023, 12, 31)
        end_date = date(2024, 3, 28)
        investment_data[investment['ticker']] = get_investment_data_from_ticker(investment)
        ticker = investment['ticker']
        stock_data = StockData.objects.filter(ticker=ticker, date__range=(start_date, end_date))
        dates = [data.date for data in stock_data]

        if close_prices:
            for i in range(len(stock_data)):
                close_prices[i] += stock_data[i].close_price * investment['quantity']
        else:
            close_prices = [data.close_price * investment['quantity'] for data in stock_data]

    plot_data['dates'] = [date.strftime('%Y-%m-%d') for date in dates]
    plot_data['close_prices'] = close_prices

    pie_data = {'labels': [], 'sizes': []}
    for key in investment_data.keys():
        pie_data['labels'].append(key)
        pie_data['sizes'].append(investment_data[key][5])  # Current Value

    return [investments, plot_data, investment_data, pie_data]

# This function is used to get the investments and then plot the data for each investment and the distribution of the investments
def get_investment_data(investments):
    plot_data = {'dates': [], 'close_prices': {}}
    investment_data = {}

    for investment in investments:
        start_date = date(2023, 12, 31)
        end_date = date(2024, 3, 28)
        investment_data[investment['ticker']] = get_investment_data_from_ticker(investment)
        ticker = investment['ticker']
        stock_data = StockData.objects.filter(ticker=ticker, date__range=(start_date, end_date))
        dates = [data.date for data in stock_data]
        close_prices = [data.close_price for data in stock_data]

        plot_data['dates'] = [date.strftime('%Y-%m-%d') for date in dates]
        plot_data['close_prices'][ticker] = close_prices

    pie_data = {'labels': [], 'sizes': []}
    for key in investment_data.keys():
        pie_data['labels'].append(key)
        pie_data['sizes'].append(investment_data[key][5])  # Current Value

    return [investments, plot_data, investment_data, pie_data]

# This function is used to get the investment data for a particular investment
def get_investment_data_from_ticker(investment):
    investment_data = []
    curr_date = date(2024, 3, 28)
    ticker = investment['ticker']
    investment_data.append(investment['quantity'])
    investment_data.append(datetime.strptime(investment['purchase_date'], '%Y-%m-%d').date())
    investment_data.append(StockData.objects.filter(ticker=ticker, date=datetime.strptime(investment['purchase_date'], '%Y-%m-%d').date())[0].close_price)
    investment_data.append(investment_data[-1] * investment['quantity'])
    current_price = StockData.objects.filter(ticker=ticker, date=curr_date).first()
    investment_data.append(current_price.close_price)
    investment_data.append(current_price.close_price * investment['quantity'])
    one_day_ago = curr_date - timedelta(days=1)
    one_day_ago_data = StockData.objects.filter(ticker=ticker, date=one_day_ago).first()
    one_day_ago_percentage = ((current_price.close_price - one_day_ago_data.close_price) / one_day_ago_data.close_price) * 100
    investment_data.append(-one_day_ago_data.close_price + current_price.close_price)
    investment_data.append(one_day_ago_percentage)
    three_months_ago = curr_date - timedelta(days=92)
    three_months_ago_data = StockData.objects.filter(ticker=ticker, date=three_months_ago).first()
    three_months_ago_percentage = ((current_price.close_price - three_months_ago_data.close_price) / current_price.close_price) * 100
    investment_data.append(-three_months_ago_data.close_price + current_price.close_price)
    investment_data.append(three_months_ago_percentage)
    return investment_data
