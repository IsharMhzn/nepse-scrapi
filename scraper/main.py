from bs4 import BeautifulSoup
import requests
import datetime
import json


def scrape(souplist, categories, count, max=None):
    container = []
    counter = 0
    row = {}
    for t in souplist:
        if max and max == count:
            break
        if not counter:
            row[categories[counter]] = count
        else:
            row[categories[counter]] = t.text.strip()
        counter += 1
        if not counter < len(categories):
            container.append(row)
            counter = 0
            count += 1
            row = {}
    
    return container, count

def todaysprice():
    index = 1
    URL = f"http://www.nepalstock.com/main/todays_price/index/{index}/"
    categories = ('S.N.', 'Traded Company', 'No. of trans', 'MaxPrice', 'MinPrice',
                    'ClosePrice', 'TradeShares', 'Amount', 'PrevClose', 'Diff')

    container = []

    count = 1
    while index <= 10:
        response = requests.get(URL).text
        soup = BeautifulSoup(response, features="html.parser")
        td = soup.find_all("td")[11:]

        con, count = scrape(td, categories, count)
        container.extend(con)
        index += 1
    
    return container


def liveprice():
    URL = "http://www.nepalstock.com/stocklive"
    categories = ('S.N.', 'Symbol', 'LTP', 'LTV', 'PointChange', 'PercChange', 'Open', 'High', 'Low', 'Volume', 'PrevClosing')


    response = requests.get(URL).text
    soup = BeautifulSoup(response, features="html.parser")
    td = soup.find_all("td")
    
    container, count = scrape(td[11:], categories, 1)
    print(container)



def main():
    # latest_day = datetime.date.today()
    # print(latest_day)
    # latest_time = datetime.datetime.now()
    # while True:
    #     day = datetime.date.today()
    #     time = datetime.datetime.now()
    #     if time.min > latest_time.min:
    #         print("StockPrice updated")

    stock = todaysprice()
    # json_data = json.loads(stock)
    # print(json_data)
    with open("../json/todaysprice.json", 'w') as f:
        json.dump(stock, f)



if __name__ == "__main__":
    main()