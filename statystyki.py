import sqlite3
import matplotlib.pyplot as plt
import re
from collections import Counter
import numpy as np
import statistics

def powierzchnia_liczba(cursor,axes):

    cursor.execute("SELECT area FROM offers;")

    wyniki = cursor.fetchall()

    wyniki_ocz = []
    for i in wyniki:
        pow = int(re.search(r'\d+', i[0]).group())
        wyniki_ocz.insert(len(wyniki_ocz),pow)
    #print(wyniki_ocz)

    wystepowanie = Counter(wyniki_ocz)
    #print(wystepowanie)
    max_key=0
    for i in wystepowanie:
        if i>max_key:
            max_key=i

    #print(max_key)
    y_axis = []
    for i in range(max_key+1):
        if wystepowanie[i] == 0:
            y_axis.insert(len(y_axis), None)
        else:
            y_axis.insert(len(y_axis),wystepowanie[i])

    axes[0,0].plot(range(max_key+1),y_axis, "ko", markersize=2)
    axes[0,0].set_xlabel('Powierzchnia [m^2]')
    axes[0,0].set_ylabel('Liczba ogloszen')
    axes[0,0].set_title('Liczba ogloszen o danej powierzchni')
    axes[0,0].grid()
    #plt.show()

def powierzchnia_od_pokoju(cursor,axes):
    cursor.execute("SELECT area,rooms FROM offers;")

    wyniki = cursor.fetchall()

    wyniki_ocz = []
    #print(wyniki)
    for i in wyniki:
        pow = int(re.search(r'\d+', i[0]).group())
        liczba = i[1].split(' ', 1)[0]
        try:
            wyniki_ocz.insert(len(wyniki_ocz), [pow,int(liczba)])
        except:
            pass


    #print(wyniki_ocz)
    box_1_pok=[]
    box_2_pok=[]
    box_3_pok=[]
    box_4_pok=[]
    box_5_pok=[]
    for wynik in wyniki_ocz:
        if wynik[1] == 1:
            box_1_pok.insert(len(box_1_pok),wynik[0])
        if wynik[1] == 2:
            box_2_pok.insert(len(box_2_pok),wynik[0])
        if wynik[1] == 3:
            box_3_pok.insert(len(box_3_pok),wynik[0])
        if wynik[1] == 4:
            box_4_pok.insert(len(box_4_pok),wynik[0])
        if wynik[1] == 5:
            box_5_pok.insert(len(box_5_pok),wynik[0])

    flierprops = dict(marker='o', markerfacecolor='black', markersize=3,
                      markeredgecolor='none')
    axes[0,1].boxplot([box_1_pok,box_2_pok,box_3_pok,box_4_pok,box_5_pok],notch=1,flierprops=flierprops)
    axes[0,1].set_xlabel('Liczba pokoi')
    axes[0,1].set_ylabel('Powierzchnia [m^2]')
    axes[0,1].set_title('Powierzchnia w zaleznosci od liczby pokoi')
    axes[0,1].grid()
    #plt.show()


def dzielnica_kolowy(cursor,axes):
    cursor.execute("SELECT district FROM offers;")

    wyniki = cursor.fetchall()

    wyniki_ocz = []
    for i in wyniki:
        dzielnica = i[0].split('Wrocław, ',1)[1]
        dzielnica = dzielnica.split(',',1)[0]
        wyniki_ocz.insert(len(wyniki_ocz), dzielnica)
    #print(wyniki_ocz)

    wystepowanie = Counter(wyniki_ocz)

    #print(wystepowanie)
    #print(len(wyniki_ocz))
    procenty = {}
    for key in wystepowanie:
        procenty[key]=round(wystepowanie[key]/len(wyniki_ocz),2)

    #print(procenty)
    labels = []
    sizes = []
    for key in procenty:
        labels.insert(len(labels),key)
        sizes.insert(len(sizes),procenty[key])

    axes[1,1].pie(sizes,labels=labels,autopct='%1.1f%%',startangle=90)
    axes[1,1].axis('equal')
    axes[1,1].set_title("Dzielnice")
    #axes[1,1].show()

def pokoj_kolowy(cursor,axes):
    cursor.execute("SELECT rooms FROM offers;")

    wyniki = cursor.fetchall()

    #print(wyniki)
    wyniki_ocz = []
    for i in wyniki:
        liczba = i[0].split(' ', 1)[0]
        try:
            wyniki_ocz.insert(len(wyniki_ocz), int(liczba))
        except:
            pass

    #print(wyniki_ocz)

    wystepowanie = Counter(wyniki_ocz)

    #print(wystepowanie)
    #print(len(wyniki_ocz))
    procenty = {}
    for key in wystepowanie:
        procenty[key] = round(wystepowanie[key] / len(wyniki_ocz), 2)

    #print(procenty)
    labels = []
    sizes = []
    for key in procenty:
        labels.insert(len(labels), key)
        sizes.insert(len(sizes), procenty[key])

    axes[1,1].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    axes[1,1].axis('equal')
    axes[1,1].set_title("Liczba pokoi")
    #axes[1,0].show()

def cena_za_metr_kw(cursor,axes):
    cursor.execute("SELECT price,area FROM offers;")

    wyniki = cursor.fetchall()
    #print(wyniki)
    wyniki_ocz=[]
    for wynik in wyniki:
        if isinstance(wynik[0], str):
            prc = wynik[0].replace(',', '.')
            prc = float(prc)
            pow = int(re.search(r'\d+', wynik[1]).group())
            try:
                wyniki_ocz.insert(len(wyniki_ocz), [prc, pow])
            except:
                pass
        else:
            pow = int(re.search(r'\d+', wynik[1]).group())
            try:
                wyniki_ocz.insert(len(wyniki_ocz), [wynik[0], pow])
            except:
                pass

    #print(wyniki_ocz)

    axes[0,0].plot([i[1] for i in wyniki_ocz],[i[0] for i in wyniki_ocz], "ko", markersize=2)
    axes[0,0].set_xlabel('Powierzchnia [m^2]')
    axes[0,0].set_ylabel('Cena [zł]')
    axes[0,0].set_title('Cena w zaleznosci od powierzchni')
    axes[0,0].grid()
    z = np.polyfit([i[1] for i in wyniki_ocz],[i[0] for i in wyniki_ocz], 1)
    p = np.poly1d(z)
    axes[0,0].plot([i[1] for i in wyniki_ocz], p([i[1] for i in wyniki_ocz]), "r--")
    #plt.show()

def cena_za_metr_kw_dzielnica(cursor):
    cursor.execute("SELECT price,area,district FROM offers;")
    wyniki = cursor.fetchall()
    wyniki_ocz = []
    for wynik in wyniki:
        if isinstance(wynik[0], str):
            prc = wynik[0].replace(',', '.')
            prc = float(prc)
            pow = int(re.search(r'\d+', wynik[1]).group())
            dzielnica = wynik[2].split('Wrocław, ', 1)[1]
            dzielnica = dzielnica.split(',', 1)[0]
            try:
                wyniki_ocz.insert(len(wyniki_ocz), [prc, pow, dzielnica])
            except:
                pass
        else:
            pow = int(re.search(r'\d+', wynik[1]).group())
            dzielnica = wynik[2].split('Wrocław, ', 1)[1]
            dzielnica = dzielnica.split(',', 1)[0]
            try:
                wyniki_ocz.insert(len(wyniki_ocz), [wynik[0], pow, dzielnica])
            except:
                pass

    #print(wyniki_ocz)

    stare_miasto_suma_ceny = 0
    krzyki_suma_ceny = 0
    srodmiescie_suma_ceny = 0
    psie_pole_suma_ceny = 0
    nadodrze_suma_ceny = 0
    fabryczna_suma_ceny = 0
    dolnoslaskie_suma_ceny = 0
    rynek_suma_ceny = 0
    stare_miasto_ceny = []
    krzyki_ceny = []
    srodmiescie_ceny = []
    psie_pole_ceny = []
    nadodrze_ceny = []
    fabryczna_ceny = []
    dolnoslaskie_ceny = []
    rynek_ceny = []
    for wynik in wyniki_ocz:
        if wynik[2] == "Stare Miasto":
            stare_miasto_suma_ceny=stare_miasto_suma_ceny+(wynik[0]/wynik[1])
            stare_miasto_ceny.insert(len(stare_miasto_ceny),wynik[0]/wynik[1])
        if wynik[2] == "Krzyki":
            krzyki_suma_ceny=krzyki_suma_ceny+(wynik[0]/wynik[1])
            krzyki_ceny.insert(len(krzyki_ceny), wynik[0] / wynik[1])
        if wynik[2] == "Śródmieście":
            srodmiescie_suma_ceny=srodmiescie_suma_ceny+(wynik[0]/wynik[1])
            srodmiescie_ceny.insert(len(srodmiescie_ceny), wynik[0] / wynik[1])
        if wynik[2] == "Psie Pole":
            psie_pole_suma_ceny=psie_pole_suma_ceny+(wynik[0]/wynik[1])
            psie_pole_ceny.insert(len(psie_pole_ceny), wynik[0] / wynik[1])
        if wynik[2] == "Nadodrze":
            nadodrze_suma_ceny=nadodrze_suma_ceny+(wynik[0]/wynik[1])
            nadodrze_ceny.insert(len(nadodrze_ceny), wynik[0] / wynik[1])
        if wynik[2] == "Fabryczna":
            fabryczna_suma_ceny=fabryczna_suma_ceny+(wynik[0]/wynik[1])
            fabryczna_ceny.insert(len(fabryczna_ceny), wynik[0] / wynik[1])
        if wynik[2] == "dolnośląskie":
            dolnoslaskie_suma_ceny=dolnoslaskie_suma_ceny+(wynik[0]/wynik[1])
            dolnoslaskie_ceny.insert(len(dolnoslaskie_ceny), wynik[0] / wynik[1])
        if wynik[2] == "Rynek":
            rynek_suma_ceny=rynek_suma_ceny+(wynik[0]/wynik[1])
            rynek_ceny.insert(len(rynek_ceny), wynik[0] / wynik[1])

    liczba_ogloszen_na_dzielnice = Counter([i[2] for i in wyniki_ocz])
    #print(liczba_ogloszen_na_dzielnice)
    #print(stare_miasto_suma_ceny/liczba_ogloszen_na_dzielnice["Stare Miasto"])
    labels = ["Stare Miasto","Krzyki","Śródmieście","Psie Pole","Nadodrze","Fabryczna","dolnośląskie","Rynek"]
    try:
        ceny = [stare_miasto_suma_ceny/liczba_ogloszen_na_dzielnice["Stare Miasto"],krzyki_suma_ceny/liczba_ogloszen_na_dzielnice["Krzyki"],
                srodmiescie_suma_ceny/liczba_ogloszen_na_dzielnice["Śródmieście"],psie_pole_suma_ceny/liczba_ogloszen_na_dzielnice["Psie Pole"],
                nadodrze_suma_ceny/liczba_ogloszen_na_dzielnice["Nadodrze"],fabryczna_suma_ceny/liczba_ogloszen_na_dzielnice["Fabryczna"],
                dolnoslaskie_suma_ceny/liczba_ogloszen_na_dzielnice["dolnośląskie"],rynek_suma_ceny/liczba_ogloszen_na_dzielnice["Rynek"]]
    except:
        return

    mediany = [statistics.median(stare_miasto_ceny),statistics.median(krzyki_ceny),statistics.median(srodmiescie_ceny),statistics.median(psie_pole_ceny),
               statistics.median(nadodrze_ceny),statistics.median(fabryczna_ceny),statistics.median(dolnoslaskie_ceny),statistics.median(rynek_ceny)]
    #print(mediany)

    plt.figure(figsize=(20, 10))
    plt.barh(labels,ceny)
    plt.axvline(x=mediany[0], ymin=0.05, ymax=0.135, color='r',label="Mediana")
    plt.axvline(x=mediany[1], ymin=0.165, ymax=0.25, color='r')
    plt.axvline(x=mediany[2], ymin=0.28, ymax=0.365, color='r')
    plt.axvline(x=mediany[3], ymin=0.40, ymax=0.485, color='r')
    plt.axvline(x=mediany[4], ymin=0.52, ymax=0.605, color='r')
    plt.axvline(x=mediany[5], ymin=0.635, ymax=0.72, color='r')
    plt.axvline(x=mediany[6], ymin=0.75, ymax=0.835, color='r')
    plt.axvline(x=mediany[7], ymin=0.865, ymax=0.95, color='r')
    plt.legend()
    plt.xlabel("Cena za metr kwadratowy [m^2]")
    plt.ylabel("Dzielnica")
    plt.title("Cena za metr kwadratowy w zaleznosci od dzielnicy")
    plt.grid()
    plt.show()


def ilosc_mieszan_w_danych_cenach(cursor,axes):
    cursor.execute("SELECT price FROM offers;")

    wyniki = cursor.fetchall()
    prices = []

    for price in wyniki:

        if isinstance(price[0], str):
            prc = price[0].replace(',', '.')
            prc = float(prc)
            prices.append(prc)
        else:
            prices.append(price[0])

    prices_counter = Counter(prices)

    prices_list = []
    for i in prices_counter:
        prices_list.append(i)

    prices_list.sort()
    prices_count_list = []
    for k in prices_list:
        prices_count_list.append(prices_counter[k])

    axes[0,1].plot(prices_list, prices_count_list, "ko", markersize=3)
    axes[0,1].set_xlabel('Cena [zł]')
    axes[0,1].set_ylabel('Ilość mieszkań')
    #axes[0,1].xticks(range(0, 25000, 2000))
    #axes[0,1].yticks(range(0, 250, 25))
    axes[0,1].set_title('Ilość mieszkań w danej cenie')
    axes[0,1].grid()
    #plt.show()


def cena_w_zaleznosci_od_liczby_pokoi(cursor,axes):
    cursor.execute("SELECT price,rooms FROM offers;")

    wyniki = cursor.fetchall()
    prices = []

    for price in wyniki:

        if isinstance(price[0], str):
            prc = price[0].replace(',', '.')
            prc = float(prc)
            prices.append(prc)
        else:
            prices.append(price[0])

    cena_liczba_pokojow_w_mieszkaniu = []

    for i in wyniki:
        if isinstance(i[0], str):
            prc = i[0].replace(',', '.')
            prc = float(prc)
        else:
            prc = (i[0])
        liczba = i[1].split(' ', 1)[0]
        try:
            cena_liczba_pokojow_w_mieszkaniu.append([prc, int(liczba)])
        except:
            pass
    box_1_pok = []
    box_2_pok = []
    box_3_pok = []
    box_4_pok = []
    box_5_pok = []
    for wynik in cena_liczba_pokojow_w_mieszkaniu:
        if wynik[1] == 1:
            box_1_pok.insert(len(box_1_pok), wynik[0])
        if wynik[1] == 2:
            box_2_pok.insert(len(box_2_pok), wynik[0])
        if wynik[1] == 3:
            box_3_pok.insert(len(box_3_pok), wynik[0])
        if wynik[1] == 4:
            box_4_pok.insert(len(box_4_pok), wynik[0])
        if wynik[1] == 5:
            box_5_pok.insert(len(box_5_pok), wynik[0])

    flierprops = dict(marker='o', markerfacecolor='black', markersize=3,
                      markeredgecolor='none')
    axes[1,0].boxplot([box_1_pok, box_2_pok, box_3_pok, box_4_pok, box_5_pok], notch=1, flierprops=flierprops)

    axes[1,0].set_xlabel('Ilość pokoi w mieszkaniu')
    axes[1,0].set_ylabel('Cena [zł]')
    axes[1,0].set_title('Cena w zależności od liczby pokoi')
    axes[1,0].grid()
    #axes[1,0].yticks(range(0, 17500, 1000))
    #plt.show()


def procent_ofert_w_zaleznosci_od_powierzchni(cursor,axes):
    cursor.execute("SELECT area FROM offers;")

    wyniki = cursor.fetchall()
    powierzchnie = []

    for i in wyniki:
        pow = int(re.search(r'\d+', i[0]).group())
        try:
            powierzchnie.append(pow)
        except:
            pass
    powierzchnie.sort()

    przedzial_0_25 = 0
    przedzial_25_50 = 0
    przedzial_50_75 = 0
    przedzial_75_100 = 0
    przedzial_100_125 = 0
    przedzial_125_150 = 0
    przedzial_150_175 = 0
    przedzial_175_200 = 0

    for powierzchnia in powierzchnie:
        if powierzchnia > 0 and powierzchnia <= 25:
            przedzial_0_25 += 1
        elif powierzchnia > 25 and powierzchnia <= 50:
            przedzial_25_50 += 1
        elif powierzchnia > 50 and powierzchnia <= 75:
            przedzial_50_75 += 1
        elif powierzchnia > 75 and powierzchnia <= 100:
            przedzial_75_100 += 1
        elif powierzchnia > 100 and powierzchnia <= 125:
            przedzial_100_125 += 1
        elif powierzchnia > 125 and powierzchnia <= 150:
            przedzial_125_150 += 1
        elif powierzchnia > 150 and powierzchnia <= 175:
            przedzial_150_175 += 1
        elif powierzchnia > 175 and powierzchnia <= 200:
            przedzial_175_200 += 1

    przedzialy = ['(0,25]', '(25,50]', '(50,75]', '(75,100]', '(100,125]', '(125,150]', '(150,175]', '(175,200]']
    suma_wszystkich = przedzial_0_25 + przedzial_25_50 + przedzial_50_75 + przedzial_75_100 + przedzial_100_125 + przedzial_125_150 + przedzial_150_175 + przedzial_175_200
    wartosci = [round(przedzial_0_25 / suma_wszystkich * 100, 1), round(przedzial_25_50 / suma_wszystkich * 100, 1),
                round(przedzial_50_75 / suma_wszystkich * 100, 1), round(przedzial_75_100 / suma_wszystkich * 100, 1),
                round(przedzial_100_125 / suma_wszystkich * 100, 1),
                round(przedzial_125_150 / suma_wszystkich * 100, 1),
                round(przedzial_150_175 / suma_wszystkich * 100, 1),
                round(przedzial_175_200 / suma_wszystkich * 100, 1)]

    axes[1,0].barh(przedzialy, wartosci)
    for index, value in enumerate(wartosci):
        axes[1,0].text((value), index, str(value) + "%")
    axes[1,0].set_xlabel('Procent ofert [%]')
    axes[1,0].set_ylabel('Powierzchnia [m^2]')
    axes[1,0].set_title('Udział procentowy w zależności od powierzchni')
    axes[1,0].grid()
    #plt.show()

if __name__ == "__main__":
    # Connect to DB
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    fig_1, axes = plt.subplots(2,2,figsize=(20,10))
    fig_1.subplots_adjust(left=0.125,bottom=0.1,right=0.9,top=0.9,wspace=0.3,hspace=0.3)
    powierzchnia_liczba(cursor,axes)
    dzielnica_kolowy(cursor,axes)
    ilosc_mieszan_w_danych_cenach(cursor,axes)
    cena_w_zaleznosci_od_liczby_pokoi(cursor,axes)
    plt.show()

    fig_2, axes =plt.subplots(2,2,figsize=(20,10))
    fig_2.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.3)
    powierzchnia_od_pokoju(cursor,axes)
    cena_za_metr_kw(cursor,axes)
    pokoj_kolowy(cursor, axes)
    procent_ofert_w_zaleznosci_od_powierzchni(cursor,axes)
    plt.show()

    cena_za_metr_kw_dzielnica(cursor)
