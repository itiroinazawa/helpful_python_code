import pika
import json

def produce_messages():
    """Function to produce messages to a RabbitMQ queue."""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    queue_name = 'example_queue'
    channel.queue_declare(queue=queue_name)

    messages = [{'id': i, 'value': f'message {i}'} for i in range(10)]

    for message in messages:
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message)
        )
        print(f"Produced: {message}")

    connection.close()

def consume_messages():
    """Function to consume messages from a RabbitMQ queue."""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    queue_name = 'example_queue'
    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        print(f"Consumed: {message}")

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    print("Starting to consume messages...")
    channel.start_consuming()

def main():
    choice = input("Enter 'p' to produce messages or 'c' to consume messages: ").strip().lower()

    if choice == 'p':
        produce_messages()
    elif choice == 'c':
        consume_messages()
    else:
        print("Invalid choice. Please enter 'p' or 'c'.")

if __name__ == "__main__":
    main()
