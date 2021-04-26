from bs4 import BeautifulSoup
from requests import get
import re

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

        
        info = str(page_details.find('div', class_='css-1d9dws4 egzohkh2').get_text())
        #rent = re.search('(?<=Czynsz - dodatkowo:)(\d{3})', info).group()
        try:
            rent = re.search('(?<=Czynsz - dodatkowo:)(\d{3})', info).group()
    #    floor = re.search('(?<=Piętro:)(\d)', info).group()
    #   bail = re.search('(?<=Kaucja:)(\d{1,5}$)', info).group()
        except:
            pass


        print(price, rooms, area, district, rent)