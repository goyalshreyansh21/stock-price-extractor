import requests
import csv
from bs4 import BeautifulSoup
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np

url = "https://coinmarketcap.com/"

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')

stocks=[]
name=[]
price=[]
mktcap=[]
volume=[]

heading = soup.find('tr')
for row in heading.find_all_next('tr',limit = 10):
    stock={}
    stock['name'] = row.find('p',attrs={'class':'sc-e225a64a-0 ePTNty'}).text
    stock['abbr'] = row.find('p',attrs={'class':'sc-e225a64a-0 dfeAJi coin-item-symbol'}).text
    name += [stock['abbr']]
    stock['price'] = row.find('div',attrs={'class':'sc-4bc2743f-0 fhCjTa'}).text
    price += [int(round(float(stock['price'].strip('$ ').replace(",",""))))/10**3]
    stock['mktcap'] = row.find('span',attrs={'class':'sc-edc9a476-1 gqomIJ'}).text
    mktcap += [int(round(float(stock['mktcap'].strip('$ ').replace(",",""))))/10**9]
    stock['volume'] = row.find('p',attrs={'class':'sc-e225a64a-0 gLNGkf font_weight_500'}).text
    volume += [int(round(float(stock['volume'].strip('$ ').replace(",",""))))/10**9]
    stocks.append(stock)

filename = 'stockmarketscraper.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['name','abbr','price','mktcap','volume'])
    w.writeheader()
    for stock in stocks:
        w.writerow(stock)

barWidth = 0.5
r1 = np.arange(len(price))
r2 = np.arange(len(mktcap))
r3 = np.arange(len(volume))

plt.subplot(1, 3, 1)
plt.bar(r1, price, color='#7f6d5f', width=barWidth)
plt.title('Price (in thousand $)', fontsize = 15, fontname = 'Helvetica')
plt.xticks([r for r in range(len(price))], name, rotation = 30)

plt.subplot(1, 3, 2)
plt.bar(r2, mktcap, color='#557f2d', width=barWidth)
plt.title('Market Cap (in billion $)', fontsize = 15, fontname = 'Helvetica')
plt.xticks([r for r in range(len(mktcap))], name, rotation = 30)

plt.subplot(1, 3, 3)
plt.bar(r3, volume, color='#2d7f5e', width=barWidth)
plt.title('Volume (in billion $)', fontsize = 15, fontname = 'Helvetica')
plt.xticks([r for r in range(len(volume))], name, rotation = 30)
 

plt.suptitle("Cryptocurrencies", fontsize = 20)
plt.show()
