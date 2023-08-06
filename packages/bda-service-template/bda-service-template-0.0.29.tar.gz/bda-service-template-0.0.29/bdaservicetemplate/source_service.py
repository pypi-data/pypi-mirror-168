from abc import abstractclassmethod
from .streaming_service import StreamingService
from bdaserviceutils import get_kafka_binder_brokers, get_output_channel
from kafka import KafkaProducer
from abc import ABC, abstractclassmethod
import json


class SourceService(ABC, StreamingService):
    
    alida_service_mode = "source"
    
    def __init__(self, parser):
        super().__init__(parser)
        self.producer = KafkaProducer(bootstrap_servers=[get_kafka_binder_brokers()])

    
    @abstractclassmethod
    def run(self):
        pass

    def send_message(self, message):
        self.producer.send(get_output_channel(), json.dumps(message).encode('utf-8'))
