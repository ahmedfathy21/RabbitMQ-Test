import pika
import json 
import time 
# Establish a connection to RabbitMQ server and create a channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='report_pdf_body', durable=True)
# Create a message body
print("Sender starting to send a heavy message to the queue...")
start_time = time.time()
for i in range(1,6):
    payload = {
        "report_id" : 1,
        "user_email" : "ahmedfathy11876@gmail.com",
        "timestamp" : time.time()
    }

    channel.basic_publish(exchange='', routing_key='report_pdf_body', body=json.dumps(payload),properties=pika.BasicProperties
                      (delivery_mode=pika.DeliveryMode.Persistent))
    print(f" [x] Sent message {i}")

total_time = time.time() - start_time
print(f"Finished sending 5 messages in {total_time:.2f} seconds")

connection.close()




