# Interview pre-screening homework

## Task Definition 
An Investor has two brokerage accounts -- Schwab and Fidelity 
  
In his Schwab account, he owns stock of Apple Computer (AAPL), 100 shares, that he purchased at the closing piece on 12/31/2023.
In his Fidelity account, he has two positions:  Microsoft (MSFT), 100 shares, that he purchased at closing price on 12/31/23, and 100 shares of Vanguard Total Stock Market Index ETF (VTI) 
   
## Technical Requirements
Using Django 5, please develop 
- an api to pull the daily closes and dividends data from Yahoo Finance into a database (only one endpoint and no authentication needed)
- and a webpage to display the information as follows based on stock data end of day 3/31/24.: 

For the display, use the following libraries:
https://github.com/ColorlibHQ/AdminLTE/releases
That will include all the necessary CSS and JS files.
Layout should be similar to the https://adminlte.io/themes/v3/ dashboard.

For accessing Yahoo Finance there is a Python library called yfinance that you can use. It's added to requirements and there is a simple example of how to use it in the ytest.py file.
Package home page: https://pypi.org/project/yfinance/

## Data Requirements
  For Schwab and Fidelity Account: 
  Investment Value ($) by Ticker Symbol 
  Change in value by $ and Percent for 1 day and 3 months 
  Beta for each security
  
  Investment value by ticker symbol 
  combined investment value line graph for 3 months (closing day price) 
  Pie chart with total value by security ($ and 😖

## How to finish the task
- Clone this repository
- Create a new branch with your name
- when all the requirements are met, push the branch to github

