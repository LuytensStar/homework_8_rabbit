from mongoengine import Document, StringField,BooleanField

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)
    phone_number = StringField()
    preferred_way = StringField(choices=['email', 'sms'])
