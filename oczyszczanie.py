import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM offers;")

wyniki = cursor.fetchall()

ile_usunac=int(wyniki[0][0]*0.01)

print(ile_usunac)

#cursor.execute(".load /usr/lib/sqlite3/pcre.so")

#oczyszczanie ceny
zapytanie="DELETE FROM offers WHERE price NOT REGEXP '^\d{1,5}[.]\d';"

cursor.execute(zapytanie)

zapytanie="DELETE FROM offers ORDER BY price DESC LIMIT %s;".format(ile_usunac)

cursor.execute(zapytanie)

zapytanie="DELETE FROM offers ORDER BY price ASC LIMIT %s;".format(ile_usunac)

cursor.execute(zapytanie)

#oczyszczanie pokoi
zapytanie="DELETE FROM offers WHERE rooms NOT REGEXP '^\d{1,2}\spo';"

cursor.execute(zapytanie)

#oczyszczanie metrazu
zapytanie="DELETE FROM offers ORDER BY cast(area as float) DESC LIMIT %s;".format(ile_usunac)

cursor.execute(zapytanie)

zapytanie="DELETE FROM offers ORDER BY cast(area as float) ASC LIMIT %s;".format(ile_usunac)

cursor.execute(zapytanie)

#oczyszczanie dzielnicy
#zapytanie="DELETE FROM offers WHERE district NOT REGEXP '\b(Krzyki|Stare Miasto|Nadodrze|Psie Pole|Fabryczna|Rynek|dolnośląskie|Śródmieście)\b';"

#oczyszczanie czynszu
zapytanie="DELETE FROM offers ORDER BY rent DESC LIMIT %s;".format(int(ile_usunac/2))

cursor.execute(zapytanie)

zapytanie="DELETE FROM offers ORDER BY rent ASC LIMIT %s;".format(int(ile_usunac/2))

cursor.execute(zapytanie)

#oczyszczanie pietra
zapytanie="DELETE FROM offers WHERE floor NOT REGEXP '^\d{1,2}[.]\d';"

cursor.execute(zapytanie)

#oczyszczanie kaucji
zapytanie="DELETE FROM offers ORDER BY bail DESC LIMIT %s;".format(int(ile_usunac/2))

cursor.execute(zapytanie)

zapytanie="DELETE FROM offers ORDER BY bail ASC LIMIT %s;".format(int(ile_usunac/2))

cursor.execute(zapytanie)

zapytanie="DELETE FROM offers WHERE bail NOT REGEXP '^\d{1,5}[.]\d';"

cursor.execute(zapytanie)