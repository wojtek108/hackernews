import json
import requests
from bs4 import BeautifulSoup
import os

url = 'https://us1.campaign-archive.com/home/?u=faa8eb4ef3a111cef92c4f3d4&id=e505c88a2e'

response = requests.get(url)
html = response.text

links = set()

soup = BeautifulSoup(response.content, 'html.parser')
for link in soup.find_all('a'):
    try:
        if link.string and '#' in link.string:
            links.add(link.get('href'))
    except TypeError:
        pass

# Read existing data from the JSON file
if os.path.exists("database.json"):
    with open("database.json", "r", encoding="UTF-8") as infile:
        database = json.load(infile)
else:
    database = {}

# Process new links and update the database
for link in links:
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        issue = soup.find(id='issue')
        
        if issue and len(issue.contents) > 2:
            date_of_issue = issue.contents[2].strip()
        
            for link2 in soup.find_all('a'):
                try:
                    if link2.get('title') and 'Votes' in link2.get('title'):
                        category = link2.parent.find_previous_sibling('h2').get_text(strip=True)
                        element_link = link2.get('href')
                        element_name = link2.string.strip()

                        if database.get(category) is None:
                            database[category] = []
                        database[category].append([element_name, element_link, date_of_issue])
                except Exception as e:
                    print(f"Error processing inner link: {e}")
    except requests.RequestException as e:
        print(f"Error fetching link {link}: {e}")

# Write the updated database back to the JSON file
with open("database.json", "w", encoding="UTF-8") as outfile:
    json.dump(database, outfile, indent=4, ensure_ascii=False)
