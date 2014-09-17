
class Server(object):
    MESSAGE_TYPE_CONNECT = 'connect'
    MESSAGE_TYPE_SEND = 'send'

    def __init__(self):
        self.clients = {}
        self.send = None
        self.receive = None
        self.get_time = None
        self.get_ping = None
        self.time = None
        self.messages = []

        self.waiting_clients = {}
        self.ping_count = 10

    def mainloop(self):
        self.time = self.get_time()

        messages = self.receive()
        for message in messages:
            client_id = message['client']

            if client_id not in self.clients:
                self.process_new_client(client_id, message)
                continue

            client = self.clients[client_id]
            message['data']['server_time'] = self.get_message_server_time(client, message['data']['client_time'])


    def get_message_server_time(self, client, message_client_time):
        message_server_time = self.time - client['ping']
        if client['last_message_time'] is not None:
            interval_since_last_message = message_client_time - client['last_message_client_time']
            message_server_time = client['last_message_time'] + interval_since_last_message
        client['last_message_time'] = message_server_time
        client['last_message_client_time'] = message_client_time
        return message_server_time

    def process_new_client(self, client_id, message):
        ping = self.measure_ping(client_id, message)
        if ping is not None:
            self.clients[client_id] = {
                'ping': ping,
                'last_message_client_time': None,
                'last_message_time': None
            }

    def measure_ping(self, client_id, message):
        if message['type'] != Server.MESSAGE_TYPE_CONNECT:
            raise "%s before connect" % message['type']
        return self.get_ping(client_id)

    def snapshot(self):
        return None

