from bs4 import BeautifulSoup

import time
import sys
import re
import json
import requests

wikipedia = "https://en.wikipedia.org"
mainWiki = "/wiki/Lists_of_astronomical_objects"

blacklist = [
    "Lists of astronauts",
    "List of astronomical objects",
    "List of government space agencies",
    "List of planetariums",
    "Lists of space scientists",
    "Lists of spacecraft"
]

nameList = json.load(open("data.json","r", encoding='utf8'))

def save_data():
    existing = json.load(open("data.json","r", encoding='utf8'))
    uniques = set(nameList) - set(existing)
    json.dump(list(set(existing)) + list(uniques),open("data.json","w", encoding='utf8'),indent=4, ensure_ascii=False)

def open_link(l):
    names = BeautifulSoup(requests.get(l).content, 'html.parser').find_all('td', recursive=True)

    print(f"Scrapping {l}...")
    for i in names:
        name = i.find("a")
        if (name and name.text):
            if (not re.match("[^a-zA-Z0-9 ]", name.text) and len(name.text) > 2):
                if not (name.text in nameList):
                    for string in BeautifulSoup(requests.get(f"{wikipedia}/wiki/{name.text.replace(' ','_')}").content, 'html.parser').strings:
                        if "astro" in string:
                            nameList.append(name.text)
                            break
    save_data()
    print(f"{l}\nNames scrapped: {(len(nameList))}")


def scrap():
    links = BeautifulSoup(requests.get(f"{wikipedia}{mainWiki}").content, 'html.parser').find_all('li', recursive=True)
    print(f"Estimated time: {(len(links) * 60)} seg\n")

    for i in links:
        link = i.find("a")
        if (link and link.text.lower().startswith("list") and not(link.text in blacklist)):
            open_link(f"{wikipedia}{link['href']}")

scrap()
print(f"Total: {len(nameList)}")