from mongoengine import Document, StringField, BooleanField

import connect as connect


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sending_mail = BooleanField(default=False)
