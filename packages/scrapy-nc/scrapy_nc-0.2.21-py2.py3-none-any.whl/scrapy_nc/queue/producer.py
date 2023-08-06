import logging
import json
import pika

class Producer:

    def __init__(self, host, port, virtual_host, username, password):
        if virtual_host == '':
            virtual_host = '/'
        self._is_enable = host and len(host) > 0
        if self._is_enable:
            self._params = pika.connection.ConnectionParameters(
                host=host,
                port=port,
                virtual_host=virtual_host,
                heartbeat=0,
                credentials=pika.credentials.PlainCredentials(username, password))
            self.queue_names = []

        self._conn = None
        self._channel = None

    def connect(self):
        if self._is_enable and ( not self._conn or self._conn.is_closed) :
            self._conn = pika.BlockingConnection(self._params)
            self._channel = self._conn.channel()

    def _publish(self, queue_name, msg):

        if not queue_name in self.queue_names:
            self._channel.queue_declare(queue_name,
                                            passive=False,
                                            durable=True,
                                            exclusive=False,
                                            auto_delete=False,
                                            arguments=None,
                                            )
            self.queue_names.append(queue_name)
        self._channel.basic_publish('',
                                    queue_name,
                                    msg,
                                    pika.BasicProperties(
                                            content_type='application/json',
                                            delivery_mode=2),
                                    )


    def publish(self, queue_name, msg):
        """Publish msg, reconnecting if necessary."""
        if self._is_enable:
            try:
                self._publish(queue_name,msg)
                logging.info(f'send to queue {queue_name}')
            except pika.exceptions.ConnectionClosed:
                logging.debug('reconnecting to queue')
                self.connect()
                self._publish(queue_name,msg)

    def close(self):
        if self._conn and self._conn.is_open:
            logging.debug('closing queue connection')
            self._conn.close()
