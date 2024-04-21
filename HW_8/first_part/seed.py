import json

from mongoengine.errors import NotUniqueError

from models import Author, Quote


def create_an_authors():
    with open("authors.json", encoding="utf8") as af:
        data = json.load(af)
        for el in data:
            try:
                author = Author(
                    fullname=el.get("fullname"),
                    born_date=el.get("born_date"),
                    born_location=el.get("born_location"),
                    discription=el.get("discription"),
                )
                author.save()
            except NotUniqueError:
                pass


def create_quotes():
    with open("quotes.json", encoding="utf8") as qf:
        data = json.load(qf)
        for el in data:
            author, *_ = Author.objects(fullname=el.get("author"))
            quote = Quote(tags=el.get("tags"), author=author, quote=el.get("quote"))
            quote.save()


if __name__ == "__main__":
    create_an_authors()
    create_quotes()
