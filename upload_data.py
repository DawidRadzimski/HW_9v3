import json
from connect import connect_to_mongodb
from models import Author, Quote, Tag
from datetime import datetime

def read_json_data(file_path):
    with open(file_path, "r", encoding="UTF-8") as fh:
        readable_data = json.load(fh)
    return readable_data

def save_data_to_mongodb(authors, quotes):
    for author in authors:
        author_obj = Author()
        author_obj.fullname = author["fullname"]
        author_obj.born_date = datetime.strptime(author["born_date"], "%B %d, %Y").strftime("%Y-%m-%d")
        author_obj.born_location = author["born_location"]
        author_obj.description = author["description"]
        author_obj.save()

        for quote in quotes:
            if quote["author"] == author["fullname"]:
                tags = []
                for tag in quote["tags"]:
                    tags.append(Tag(name=tag))
                Quote(
                    tags=tags,
                    author=author_obj,
                    quote=quote["quote"]
                ).save()

def seed_mongo_db():
    connect_to_mongodb()
    authors_file_path = "./data/authors.json"
    quotes_file_path = "./data/quotes.json"
    save_data_to_mongodb(read_json_data(authors_file_path), read_json_data(quotes_file_path))

if __name__ == '__main__':
    seed_mongo_db()
