import pika 
import json
import time
import os
import sys
# Establish a connection to RabbitMQ server and create a channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # create a queue named report_pdf_body
    channel.queue_declare(queue='report_pdf_body',durable=True)


    def callback(ch, method, properties, body):
        data = json.loads(body.decode())
        report_id = data['report_id']
        user_email = data['user_email']

        print(f" [x] Received report_id: {report_id}, user_email: {user_email}")
        
        time.sleep(3)  # Simulate time-consuming processing
        print(f" [Worker] is processing report_id: {report_id}")
        print("_" * 50)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='report_pdf_body', on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down...")
        try:
            connection.close()
        except Exception as e:
            print(f"Error closing connection: {e}")
        sys.exit(0)
