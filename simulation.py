from client import Client
from server import Server

class Simulation(object):
    MESSAGE_TYPE_CONNECT = 'connect'
    MESSAGE_TYPE_SEND = 'send'

    def __init__(self, scenario):
        self.scenario = scenario
        self.start = self.scenario.start
        self.end = self.scenario.end
        self.time = self.start

        self.server = Server()
        self.server.queue = []
        self.server.send = self.server_send()
        self.server.receive = self.server_receive()
        self.server.get_time = self.server_time()

        self.clients = []
        for i in range(scenario.clients_number):
            client = Client()
            client.id = i
            client.queue = []
            client.connect = self.client_connect(client.id)
            client.send = self.client_send(client.id)
            client.receive = self.client_receive(client.id)
            client.get_time = self.client_time(client.id)
            client.connection_time = None
            self.clients.append(client)

    def run(self):
        for time in range(self.start, self.end + 1):
            self.time = time
            yield self.model()

    def model(self):
        self.apply_events()
        if (self.time - self.start) % self.scenario.props['main_loop_period']['server'] == 0:
            self.server.mainloop()
        for client in self.clients:
            if client.connection_time is None:
                continue
            if (self.time - client.connection_time) % self.scenario.props['main_loop_period']['client'][client.id] == 0:
                client.mainloop()
        return {
            'server': self.server.snapshot(),
            'client': [client.snapshot() for client in self.clients]
        }

    def apply_events(self):
        events = [None] * len(self.clients)
        if self.time in self.scenario.events:
            events = self.scenario.events[self.time]
        for client_id, event in enumerate(events):
            if not event:
                continue
            if event == '^':
                self.clients[client_id].connect()
                continue
            for key in event:
                event_type = 'keyup'
                if key.istitle():
                    event_type = 'keypress'
                method = getattr(self.clients[client_id], event_type)
                method(key.lower())

    def server_time(self):
        return lambda: self.scenario.props['local_time_start']['server'] + self.time

    def client_time(self, client_id):
        def get_time():
            return self.scenario.props['local_time_start']['client'][client_id] + self.time
        return get_time

    def server_send(self):
        def send(client_id, message):
            return self.clients[client_id].queue.append(message)
        return send

    def server_receive(self):
        def receive():
            queue = [x for x in self.server.queue]
            self.server.queue = []
            return queue
        return receive

    def client_connect(self, client_id):
        def connect():
            self.clients[client_id].connection_time = self.time
            return self.server.queue.append({'type': self.MESSAGE_TYPE_CONNECT, 'client': client_id})
        return connect

    def client_send(self, client_id):
        def send(message):
            return self.server.queue.append({'type': self.MESSAGE_TYPE_SEND, 'client': client_id, 'message': message})
        return send

    def client_receive(self, client_id):
        def receive():
            queue = [x for x in self.clients[client_id].queue]
            self.clients[client_id].queue = []
            return queue
        return receive

