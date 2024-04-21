from faker import Faker
import pika

from models import Contact

faker = Faker()

# docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

exchange = "mailing_email"
queue_name = "mailing"

channel.exchange_declare(exchange=exchange, exchange_type="direct")
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange, queue=queue_name)


def create_contact():
    contact = Contact(
        fullname=faker.name(),
        email=faker.email(),
    )
    contact.save()
    return contact


def create_tasks(nums: int):
    for _ in range(nums):
        contact = create_contact()

        channel.basic_publish(
            exchange=exchange,
            routing_key=queue_name,
            body=str(contact.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    connection.close()


if __name__ == "__main__":
    create_tasks(30)
