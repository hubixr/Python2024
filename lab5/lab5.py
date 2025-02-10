import requests
from bs4 import BeautifulSoup
import json

url = "https://pl.wikipedia.org/wiki/Mistrzostwa_Polski_w_szachach"
res = requests.get(url)


soup = BeautifulSoup(res.text, 'html.parser')
mistrzowie = []

for row in soup.select('table tbody tr'):  # wskaznie miejsca gdzie są interesujące nas dane
  columns = row.find_all(['td'])  
  if len(columns) == 6:  #6 kolumn bo tyle ma tabela z której biorę dane
    rok = columns[1].get_text(strip=True)
    lokalizacja = columns[2].get_text(strip=True)
    zwyciezca = columns[3].get_text(strip=True) 
    drugie = columns[4].get_text(strip=True)
    trzecie = columns[5].get_text(strip=True)
    mistrzowie.append({"Rok": rok, "Lokalizacja": lokalizacja, "1 Miejsce": zwyciezca, "2 Miejsce": drugie, "3 Miejsce": trzecie})
 


#print(mistrzowie)
output_file = "mistrzowie_polski_szachy.json"
with open(output_file, 'w', encoding='utf-8') as file:
  json.dump(mistrzowie, file, ensure_ascii=False, indent=4)
