from mongoengine import (
    CASCADE,
    Document,
    ListField,
    ReferenceField,
    StringField,
)

import connect as connect


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=60)
    born_location = StringField(max_length=150)
    discription = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField(StringField(max_length=20))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {"collection": "quotes"}
