from models import Contact
import pika
import json
from connection import connect

credentials = pika.PlainCredentials('guest', 'guest')
connected = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost', port=5672, credentials=credentials))

channel = connected.channel()

channel.queue_declare('sms_queue')

def send_sms(phone):
    print(f"SMS sent to {phone}")
    return True

def callback(ch, method, properties,body):
    contact = Contact.objects(id = body.decode()).first()
    if contact and not contact.message_sent:
        if send_sms(contact.phone_number):
            contact.message_sent = True
            contact.save()

channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

print("waiting for messages(sms)")
channel.start_consuming()