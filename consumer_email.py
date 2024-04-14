from models import Contact
from connection import connect
import json
import pika

credentials = pika.PlainCredentials('guest', 'guest')
connected = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))

channel = connected.channel()

channel.queue_declare('email_queue')

def email_send(email):
    print(f"email sent to {email}")
    return True

def callback(ch, method, properties, body):
    contact = Contact.objects(id = body.decode()).first()
    if contact and not contact.message_sent:
        if email_send(contact.email):
            contact.message_sent=True
            contact.save()

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print("waiting for message(email)")
channel.start_consuming()