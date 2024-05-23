from datetime import date,datetime,timedelta
from django.shortcuts import render
from django.views import generic
from django.shortcuts import render
from django.conf import settings

from .models import StockData
import matplotlib.pyplot as plt
import mpld3

# This is the function that will be called when /investments is called
def investments_view(request):
    investment = settings.STATIC_INVESTMENTS
    investment_data=get_total_investment_data(investment)
    return render(request, 'investmentDashboard/investments.html', {'static_investments': investment_data[0], 'plot_htmls': investment_data[1], 'investment_data': investment_data[2],'pie_chart_html': investment_data[3]})

# This is the function that will be called when /fidelity is called
def fidelity_view(request):
    fidelity_investments = [investment for investment in settings.STATIC_INVESTMENTS if investment['broker'] == 'Fidelity']
    investment_data=get_investment_data(fidelity_investments)
    return render(request, 'investmentDashboard/fidelity.html', {'static_investments': investment_data[0], 'plot_htmls': investment_data[1], 'investment_data': investment_data[2],'pie_chart_html': investment_data[3]})
# This is the function that will be called when /schwab is called
def schwab_view(request):
    schwab_investments = [investment for investment in settings.STATIC_INVESTMENTS if investment['broker'] == 'Schwab']
    investment_data=get_investment_data(schwab_investments)
    return render(request, 'investmentDashboard/schwab.html', {'static_investments': investment_data[0], 'plot_htmls': investment_data[1], 'investment_data': investment_data[2],'pie_chart_html': investment_data[3]})

#This function converts a matplotlib figure to an HTML string
def get_html_from_plot(fig):
    html_string = mpld3.fig_to_html(fig)
    return html_string


#This function is used to get the investments and then plot the combined value for all investments and the distribution of the investments
def get_total_investment_data(investments):
    plot_htmls = []
    investment_data = dict()
    plt.figure()
    close_prices = None
    for investment in investments:
        start_date = date(2023, 12,31)
        end_date = date(2024, 3, 28)
        investment_data[investment['ticker']] = get_investment_data_from_ticker(investment)
        ticker = investment['ticker']
        stock_data = StockData.objects.filter(ticker=ticker, date__range=(start_date, end_date))
        dates = [data.date for data in stock_data]
        if close_prices:
            for i in range(len(stock_data)):
                close_prices[i]+=stock_data[i].close_price*investment['quantity']
        else:
            close_prices = [data.close_price* investment['quantity'] for data in stock_data]
    plt.plot(dates, close_prices, label="Total Investment")
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Stock Close Prices')
    plt.legend()
    plot_html = get_html_from_plot(plt.gcf())
    plot_htmls.append(plot_html)
    pie_chart_html = ''
    labels= []
    sizes=[]
    for key in investment_data.keys():
        labels.append(key)
        sizes.append(investment_data[key][3])
    plt.figure()
    plt.pie(sizes, labels=labels, autopct=lambda x: '{:,.2f}'.format(x),startangle=140)
    plt.axis('equal')
    plt.title('Current Investment Value Distribution')
    pie_chart_html = get_html_from_plot(plt.gcf())
    return [investments, plot_htmls, investment_data,pie_chart_html]

#This function is used to get the investments and then plot the data for each investment and the distribution of the investments
def get_investment_data(investments):
    plot_htmls = []
    investment_data = dict()
    plt.figure()
    for investment in investments:
        start_date = date(2023, 12,31)
        end_date = date(2024, 3, 28)
        investment_data[investment['ticker']] = get_investment_data_from_ticker(investment)
        ticker = investment['ticker']
        stock_data = StockData.objects.filter(ticker=ticker, date__range=(start_date, end_date))
        dates = [data.date for data in stock_data]
        close_prices = [data.close_price for data in stock_data]
        plt.plot(dates, close_prices, label=ticker)
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Stock Close Prices')
    plt.legend()
    plot_html = get_html_from_plot(plt.gcf())  # Assuming you have a function to convert Matplotlib figures to HTML strings
    plot_htmls.append(plot_html)
    pie_chart_html = ''
    labels= []
    sizes=[]
    for key in investment_data.keys():
        labels.append(key)
        print(key,investment_data)
        sizes.append(investment_data[key][3])
    plt.figure()
    plt.pie(sizes, labels=labels, autopct=lambda x: '{:,.2f}'.format(x),startangle=140)
    plt.axis('equal')
    plt.title('Current Investment Value Distribution')
    pie_chart_html = get_html_from_plot(plt.gcf())
    return [investments, plot_htmls, investment_data,pie_chart_html]

#This function is used to get the investment data for a particular investment
def get_investment_data_from_ticker(investment):
    investment_data = list()
    curr_date = date(2024, 3, 28)
    ticker = investment['ticker']
    investment_data.append(investment['quantity'])
    investment_data.append(datetime.strptime(investment['purchase_date'], '%Y-%m-%d').date())
    investment_data.append(StockData.objects.filter(ticker=ticker, date=datetime.strptime(investment['purchase_date'], '%Y-%m-%d').date())[0].close_price)
    investment_data.append(investment_data[-1]* investment['quantity'])
    current_price = StockData.objects.filter(ticker=ticker, date=curr_date).first()
    investment_data.append(current_price.close_price)
    investment_data.append(current_price.close_price*investment['quantity'])
    one_day_ago = curr_date - timedelta(days=1)
    one_day_ago_data = StockData.objects.filter(ticker=ticker, date=one_day_ago).first()
    one_day_ago_percentage= ((current_price.close_price - one_day_ago_data.close_price)/one_day_ago_data.close_price)*100
    investment_data.append(-one_day_ago_data.close_price+current_price.close_price)
    investment_data.append(one_day_ago_percentage)
    three_months_ago = curr_date - timedelta(days=92)
    three_months_ago_data = StockData.objects.filter(ticker=ticker, date=three_months_ago).first()
    three_months_ago_percentage= ((current_price.close_price - three_months_ago_data.close_price)/current_price.close_price)*100
    investment_data.append(-three_months_ago_data.close_price+ current_price.close_price)
    investment_data.append(three_months_ago_percentage)
    return investment_data
