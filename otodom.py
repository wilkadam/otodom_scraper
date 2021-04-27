from bs4 import BeautifulSoup
from requests import get
import re
import sqlite3
from sys import argv

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Create tables in DB
if len(argv) > 1 and argv[1] == 'create':
    cursor.execute('''CREATE TABLE offers (price REAL, rooms REAL, area TEXT, district TEXT, rent REAL, floor REAL, bail REAL)''')
    quit()

# Iterafe through number of pages
for page in (1,115):

    url = 'https://www.otodom.pl/wynajem/mieszkanie/wroclaw/?search%5Bregion_id%5D=1&search%5Bsubregion_id%5D=381&search%5Bcity_id%5D=39&page=' + str(page)

    page = get(url)
    bs = BeautifulSoup(page.content, 'html.parser')

    for offer in bs.find_all('div', class_='offer-item-details'):
        price = offer.find('li', class_='offer-item-price').get_text().replace(' ', '').replace('zł/mc', '').strip()
        rooms = offer.find('li', class_='offer-item-rooms hidden-xs').get_text()
        area = offer.find('li', class_='hidden-xs offer-item-area').get_text()
        district = offer.find('p', class_='text-nowrap').get_text().replace('Mieszkanie na wynajem: ', '')

        link = offer.find('a')['href']

        get_details = get(link)
        page_details = BeautifulSoup(get_details.content, 'html.parser')
        
        info = str(page_details.find('div', class_='css-1d9dws4 egzohkh2').get_text()).replace(' ','')

        try:
            rent = re.search('(?<=Czynsz-dodatkowo:)(\d{3,4})', info).group()
            floor = re.search('(?<=Piętro:)(\d{1,2})', info).group()
            bail = re.search('(?<=Kaucja:)(\d+)', info).group()
        except:
            pass

        print(price, rooms, area, district)
        # try:
        #     print("Kaucja: " + bail + " Piętro: " + floor + " Czynsz: " + rent)
        # except:
        #     pass

        cursor.execute('INSERT INTO offers VALUES (?,?,?,?,?,?,?)', (price, rooms, area, district, rent, floor, bail))
        conn.commit()

conn.close()