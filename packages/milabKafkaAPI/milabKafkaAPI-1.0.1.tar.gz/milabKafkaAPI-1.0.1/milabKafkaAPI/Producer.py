from API import KafkaAPI
import random
import time

"""
Sending messages to the kafka server example.

General instructions:
Step 1: create a kafka producer instance using KafkaAPI.ConnectKafkaProducer().
Step 2: create a dict of the message to send.
Step 3: send the message to the kafka server using KafkaAPI.Publish(producer, topic, message).
Step 4: repeat steps 2-3 as much as needed.
Step 5: terminate the producer instance using <producer instance>.close().
"""

if __name__ == '__main__':
    producer = KafkaAPI.ConnectKafkaProducer()

    for i in range(50): # send 50 random messages
        randomDict = {
            "name": "gazer",
            "distance": random.randrange(0, 20),
            "angle": random.randrange(0, 180)
        }
        KafkaAPI.Publish(producer, 'gazer', randomDict)
        time.sleep(1)

    if producer is not None: # close the producer when done
        producer.close()
