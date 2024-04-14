import pika
from mongoengine import disconnect
from connection import connect
from faker import Faker
import json
from models import Contact

# fake = Faker()
#
#
# contact = Contact(fullname = 'alan wealker', email='alanwalker@gmail.com')
# contact.save()
#
# credentials = pika.PlainCredentials('guest', 'guest')
#
# connected = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672,credentials=credentials))
# channel = connected.channel()
#
# channel.queue_declare(queue='email_queue')
#
# for _ in range(100):
#     fullname = fake.name()
#     print(fullname)
#     contact = Contact(fullname=fullname,email=fake.email())
#     contact.save()
#
#     channel.basic_publish(exchange='',routing_key='email_queue',body=str(contact.id))
#
# connected.close()

fake = Faker()

credentials = pika.PlainCredentials('guest', 'guest')

connected = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port = 5672, credentials=credentials))

channel = connected.channel()

channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')

for i in range(10):
    print(i)
    contact = Contact(fullname=fake.name(), email=fake.email(), phone_number = fake.phone_number(),preferred_way=fake.random_element(elements=('email', 'sms')))
    contact.save()
    if contact.preferred_way == 'email':
        channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id))
    else:
        channel.basic_publish(exchange='', routing_key='sms_queue', body=str(contact.id))
        print('1')


connected.close()