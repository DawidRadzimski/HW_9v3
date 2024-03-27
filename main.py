import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from connect import connect_to_mongodb
from models import Author, Quote, Tag

def scrape_quotes(url):
    quotes = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quote_cards = soup.find_all(class_='quote')
    for card in quote_cards:
        quote_info = {}
        quote_info['quote'] = card.find(class_='text').get_text(strip=True)
        quote_info['author'] = card.find(class_='author').get_text(strip=True)
        tags = card.find_all(class_='tag')
        quote_info['tags'] = [tag.get_text(strip=True) for tag in tags]
        quotes.append(quote_info)
    return quotes

def scrape_author_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    fullname = soup.find(class_='author-title').get_text(strip=True)
    born_info = soup.find(class_='author-born-date').get_text(strip=True)
    born_location = soup.find(class_='author-born-location').get_text(strip=True)
    description = soup.find(class_='author-description').get_text(strip=True)
    author_info = {
        'fullname': fullname,
        'born_date': born_info,
        'born_location': born_location,
        'description': description
    }
    return author_info

def scrape_authors(url):
    authors = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quote_cards = soup.find_all(class_='quote')
    for card in quote_cards:
        author_link = card.find('a', href=True)['href']
        author_info = scrape_author_info(f"http://quotes.toscrape.com{author_link}")
        authors.append(author_info)
    return authors

def save_quotes_to_json(data, filename):
    os.makedirs('data', exist_ok=True)
    with open(os.path.join('data', filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_authors_to_json(data, filename):
    os.makedirs('data', exist_ok=True)
    with open(os.path.join('data', filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_data_to_mongodb(authors, quotes):
    for author in authors:
        author_obj = Author()
        author_obj.fullname = author["fullname"]
        author_obj.born_date = datetime.strptime(author["born_date"], "%B %d, %Y").strftime("%Y-%m-%d")
        author_obj.born_location = author["born_location"]
        author_obj.description = author["description"]
        author_obj.save()

    for quote in quotes:
        author_obj = Author.objects(fullname=quote["author"]).first()
        tags = []
        for tag in quote["tags"]:
            tags.append(Tag(name=tag))
        Quote(
            tags=tags,
            author=author_obj,
            quote=quote["quote"]
        ).save()

quotes_url = 'http://quotes.toscrape.com'

quotes_data = scrape_quotes(quotes_url)

authors_data = scrape_authors(quotes_url)

save_quotes_to_json(quotes_data, 'quotes.json')

save_authors_to_json(authors_data, 'authors.json')

connect_to_mongodb()
save_data_to_mongodb(authors_data, quotes_data)