import os
import sys

import pika
from models import Contact


def sending_message(fullname, email):
    print(f"На електронну пошту {email} відправлено повідомлення для {fullname} ")


def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

    queue_name = "mailing"
    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        pk = body.decode()
        contact = Contact.objects(id=pk, sending_mail=False).first()
        if contact:
            sending_message(contact.fullname, contact.email)
            contact.update(set__sending_mail=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
