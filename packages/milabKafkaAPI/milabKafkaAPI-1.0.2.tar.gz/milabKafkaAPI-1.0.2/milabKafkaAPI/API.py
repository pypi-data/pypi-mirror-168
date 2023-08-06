import json
from datetime import datetime
import lxml
from kafka import KafkaProducer, KafkaConsumer

class KafkaAPI:
    """
    API for the kafka communications for milab.
    written by Noam Freund & Omer Sadeh.
    """

    @staticmethod
    def ConnectKafkaProducer() -> KafkaProducer:
        """
        Generate a kafka producer instance connected to the milab kafka server.
        Needed for the Publish method.

        IMPORTANT: after finished with the producer, call KafkaProducer.close() to terminate instance.

        :return: producer_instance object
        """

        _producer = None
        try:
            _producer = KafkaProducer(bootstrap_servers=['192.168.57.12:9092'])  # ip depends on the computer the kafka runs from
        except Exception as ex:
            print('Exception while connecting Kafka. Reason: ' + str(ex) + "\n")
        finally:
            return _producer

    @staticmethod
    def Publish(producer_instance: KafkaProducer, topic: str, data: dict):
        """
        Publish a message to the kafka server.

        :param producer_instance: the kafka producer used
        :param topic: the topic in the kafka server to publish to
        :param data: the message itself, as a dict
        """

        try:
            key = 'raw'
            data["time"] = datetime.now().strftime("%H:%M:%S")
            value = json.dumps(data)
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            producer_instance.send(topic, key=key_bytes, value=value_bytes)
            producer_instance.flush()
            print('Message published successfully.')
        except Exception as ex:
            print('Exception in publishing message. Reason: ' + str(ex) + "\n")

    @staticmethod
    def Subscribe(topic: str, duration: int, offset: str, callback: any):
        """
        Subscribe to a topic in the kafka server, and execute a callback function on each message read.

        :param topic: the kafka topic
        :param duration: the time duration for listening (-1 for infinite duration)
        :param offset: start reading from 'earliest' or 'latest' message recorded
        :param callback: function to execute on each message ( callback(result: dict) )
        """

        try:
            if (offset != 'earliest') and (offset != 'latest'):
                raise Exception("Offset must be 'earliest' or 'lateset' onlY!")
            consumer = KafkaConsumer(topic, auto_offset_reset=offset,
                                     bootstrap_servers=['192.168.57.12:9092'], consumer_timeout_ms=(duration * 1000))
            for msg in consumer:
                callback(json.loads(msg.value))
            if consumer is not None:
                consumer.close()
        except Exception as ex:
            print('Exception in subscribing to kafka. Reason: ' + str(ex) + "\n")
