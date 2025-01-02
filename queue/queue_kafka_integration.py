from kafka import KafkaProducer, KafkaConsumer
import json

def produce_messages():
    """Function to produce messages to a Kafka topic."""
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    topic = 'example_topic'
    messages = [{'id': i, 'value': f'message {i}'} for i in range(10)]

    for message in messages:
        producer.send(topic, value=message)
        print(f"Produced: {message}")

    producer.flush()
    producer.close()

def consume_messages():
    """Function to consume messages from a Kafka topic."""
    consumer = KafkaConsumer(
        'example_topic',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    print("Starting to consume messages...")
    for message in consumer:
        print(f"Consumed: {message.value}")

    consumer.close()

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
