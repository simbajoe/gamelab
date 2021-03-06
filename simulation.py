from client_dumb import ClientDumb
from server_dumb import ServerDumb
from world import World


class Simulation(object):

    def __init__(self, scenario):
        self.scenario = scenario
        self.start = self.scenario.start
        self.end = self.scenario.end
        self.time = self.start

        World.get_player_starting_position =  lambda world, client_id: self.get_client_prop(client_id, 'starting_position')

        self.server = ServerDumb(scenario.model_step, scenario.allowed_lag_compensation_interval, scenario.snapshot_interval)
        self.server.queue = []
        self.server.send = self.server_send()
        self.server.receive = self.server_receive()
        self.server.get_time = self.server_time()
        self.server.get_ping = lambda client_id: self.get_client_prop(client_id, 'ping')
        self.server.setup()

        self.clients = []
        for i in range(scenario.clients_number):
            client = ClientDumb(scenario.model_step)
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
        if (self.time - self.start) % self.get_server_prop('main_loop_period') == 0:
            self.server.mainloop()
        for client in self.clients:
            if client.connection_time is None:
                continue
            if (self.time - client.connection_time) % self.get_client_prop(client.id, 'main_loop_period') == 0:
                client.mainloop()
        return {
            'server': self.server.snapshot(),
            'client': [client.snapshot() for client in self.clients],
            'time': self.time
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
                event_type = 'key_up'
                if key.istitle():
                    event_type = 'key_down'
                method = getattr(self.clients[client_id], event_type)
                method(key.lower())

    def server_time(self):
        return lambda: self.get_server_prop('local_time_start') + self.time

    def client_time(self, client_id):
        def get_time():
            return self.get_client_prop(client_id, 'local_time_start')
        return get_time

    def server_send(self):
        def send(client_id, message):
            return self.clients[client_id].queue.append({
                'data': message,
                'delivered': self.time + self.get_client_prop(client_id, 'ping')
            })
        return send

    def server_receive(self):
        def receive():
            queue = filter(lambda x: x['delivered'] <= self.time, self.server.queue)
            self.server.queue = filter(lambda x: x['delivered'] > self.time, self.server.queue)
            return queue
        return receive

    def client_connect(self, client_id):
        def connect():
            self.clients[client_id].connection_time = self.time + self.get_client_prop(client_id, 'ping')
            return self.server.queue.append({
                'type': ServerDumb.MESSAGE_TYPE_CONNECT,
                'client': client_id,
                'delivered': self.clients[client_id].connection_time
            })
        return connect

    def client_send(self, client_id):
        def send(message):
            return self.server.queue.append({
                'type': ServerDumb.MESSAGE_TYPE_SEND,
                'client': client_id,
                'data': message,
                'delivered': self.time + self.get_client_prop(client_id, 'ping')
            })
        return send

    def client_receive(self, client_id):
        def receive():
            queue = filter(lambda x: x['delivered'] <= self.time, self.clients[client_id].queue)
            self.clients[client_id].queue = filter(lambda x: x['delivered'] > self.time, self.clients[client_id].queue)
            return queue
        return receive

    def get_client_prop(self, client_id, prop):
        return self.scenario.props[prop]['client'][client_id]

    def get_server_prop(self, prop):
        return self.scenario.props[prop]['server']

