import pika
from connection import connect
from models import Contact

def send_email(email):
    print(f"Sending email to {email}...")
    return True

credentials = pika.PlainCredentials('guest', 'guest')

connected = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connected.channel()

channel.queue_declare(queue='email_queue')

def callback(ch,method,properties,body):
    contact = Contact.objects(id = body.decode()).first()
    if contact and not contact.message_sent:
        if send_email(contact.email):
            contact.message_sent=True
            contact.save()

channel.basic_consume(queue='email_queue',on_message_callback=callback,auto_ack=True)

print("Waiting for messages")
channel.start_consuming()
