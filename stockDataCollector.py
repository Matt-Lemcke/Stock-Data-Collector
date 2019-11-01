# Import Libraries
from bs4 import BeautifulSoup
import requests
import numpy as np
import matplotlib.pyplot as plt

# List of the user's holdings in portfolio [stock name,[shares,price bought at]]
MY_STOCKS = [["fire", [588, 1.70], [526, 1.90]], [
    "vsp", [22, 43.50]], ["wm:us", [8, 94.72], [8, 118.64]]]

# Return current exchange rate for specified currency


def getExchangeRate(currency):
    # Get webpage for exchange rate
    exRatePage = requests.get(
        "https://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/")

    # Parse webpage
    s1 = BeautifulSoup(exRatePage.content, 'html.parser')

    # Read exchange rates table
    ratesTable = s1.find(id="table_daily_1")
    currencies = list(ratesTable.find_all(class_="bocss-table__tr"))

    # Find exchange rate
    for ct in currencies:
        currencyTypes = ct.find(
            class_="bocss-table_th--indent-0 bocss-table__th bocss-table__th--row").getText()
        if currencyTypes == currency:
            currencyRates = (ct.find_all(
                class_="bocss-table__td bocss-table__td--data"))
            return float(currencyRates[-1].getText())
    return 0.0

# Display a pie chart of the portfolio holding's


def showPortfolioPie(stValues, currValues):

    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    stocks = [x[0] for x in MY_STOCKS]
    for y in stValues:
        stocks[stValues.index(
            y)] += "  " + str(round(((currValues[stValues.index(y)] - y)/y * 100), 2)) + "%"
    wedges, texts, autotexts = ax.pie(currValues, autopct=lambda pct: func(
        pct, currValues), textprops=dict(color='w'))
    ax.legend(wedges, stocks, title="Stocks",
              loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title("Portfolio Holdings")

    plt.show()


def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n(${:d})".format(pct, absolute)


# Find the current exchange rate from US dollars to CAN dollars
currentRate = getExchangeRate("US dollar")
print(currentRate)

# Find information for each stock in portfolio
priceList = []
for st in MY_STOCKS:
    # Get webpage for stock
    stockPage = requests.get(
        "https://web.tmxmoney.com/quote.php?qm_symbol="+st[0])

    # Parse webpage
    s2 = BeautifulSoup(stockPage.content, 'html.parser')

    # Get stock price
    stockInfo = s2.find(class_="quote-company-symbol")
    stockPrice = list(stockInfo.find(class_="price"))
    priceList.append(float(stockPrice[1].getText()))
print(priceList)

# Find the starting value and current value of all investements
startingValues = []
currentValues = []
for st in MY_STOCKS:
    stValue = 0
    currValue = 0
    if st[0].split(":")[-1] == "us":
        for i in range(len(st)-1):
            stValue += st[i+1][0] * st[i+1][1] * currentRate
            currValue += st[i+1][0] * \
                priceList[MY_STOCKS.index(st)] * currentRate
    else:
        for i in range(len(st)-1):
            stValue += st[i+1][0] * st[i+1][1]
            currValue += st[i+1][0] * priceList[MY_STOCKS.index(st)]
    startingValues.append(stValue)
    currentValues.append(currValue)
print(startingValues)
print(currentValues)

# Create pie chart
showPortfolioPie(startingValues, currentValues)
