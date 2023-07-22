import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = 'https://us1.campaign-archive.com/home/?u=faa8eb4ef3a111cef92c4f3d4&id=e505c88a2e'

response = requests.get(url)

print(response)

html = response.text

links =set()

soup = BeautifulSoup(response.content, 'html.parser')
for link in soup.find_all('a'):
    try:
        if '#' in link.string:
            print("Link:", "Text:", link.string)
            links.add(link.get('href'))
    except TypeError:
        pass

print(links)

database = dict()

for link in links:
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link2 in soup.find_all('a'):
        try:
            if 'Votes' in link2.get('title'):
                category = link2.parent.find_previous_sibling('h2').get_text()
                element_link = link2.get('href')
                element_name = link2.string

                if database.get(category) == None:
                    database[category] = []
                    database[category].append([element_name, element_link])
                else:
                    database[category].append([element_name, element_link])
        except:
            pass
pprint(database)
