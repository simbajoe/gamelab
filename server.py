from world import World

class Server(object):
    MESSAGE_TYPE_CONNECT = 'connect'
    MESSAGE_TYPE_SEND = 'send'

    def __init__(self, model_step, allowed_lag_compensation_interval, snapshot_interval):
        self.clients = {}
        self.send = None
        self.receive = None
        self.get_time = None
        self.get_ping = None
        self.time = None
        self.messages = []

        self.waiting_clients = {}
        self.ping_count = 10

        self.snapshots = []
        self.model_step = model_step
        self.start_time = None
        self.next_message_to_apply = None
        self.allowed_lag_compensation_interval = allowed_lag_compensation_interval
        self.snapshot_interval = snapshot_interval

    def setup(self):
        self.start_time = self.get_time()

    def mainloop(self):
        self.time = self.get_time()

        messages = self.receive()
        first_new_message_time, first_new_message_pos = self.insert_messages(messages)

        if first_new_message_time is None: # no ready clients yet
            return

        world = self.pick_world(first_new_message_time)

        time_end = self.time - self.time % self.model_step

        message_start_pos = first_new_message_pos
        start_time = world.time
        while world.time + self.model_step <= time_end:
            messages_to_apply, message_start_pos = self.get_messages_to_apply(message_start_pos, world.time + self.model_step)
            # put code about player last message id and applied period in world
            # player will need to know this for prediction
            world.apply_messages(messages_to_apply, world.time + self.model_step)
            world.model(self.model_step)
            time_passed = world.time - start_time
            if time_passed % self.snapshot_interval:
                self.snapshots.append(world.snapshot())
        self.broadcast(world.snapshot())

    def broadcast(self, snapshot):
        pass

    def get_messages_to_apply(self, message_start_pos, time_till):
        messages_to_apply = []
        while message_start_pos < len(self.messages) and self.messages[message_start_pos]['data']['server_time'] < time_till:
            messages_to_apply.append(self.messages[message_start_pos])
            message_start_pos += 1
        return messages_to_apply, message_start_pos


    def pick_world(self, time):
        pos = len(self.snapshots)
        while pos > 0 and self.snapshots[pos - 1]['time'] > time:
            pos -= 1
        self.snapshots = self.snapshots[:pos]
        if pos == 0:
            return World(self.start_time)
        return World.from_snapshot(self.snapshots[pos - 1])

    def insert_messages(self, messages):
        first_new_message_time = None
        first_new_message_pos = None
        for message in messages:
            client_id = message['client']

            if client_id not in self.clients:
                self.process_new_client(client_id, message)
                continue

            client = self.clients[client_id]
            message['data']['server_time'] = self.get_message_server_time(client, message['data']['client_time'])
            if len(self.messages) > 0 and self.messages[-1]['data']['server_time'] - message['data']['server_time'] > self.allowed_lag_compensation_interval:
                continue
            pos = self.insert_message(message)
            if first_new_message_time is None or message['data']['server_time'] < first_new_message_time:
                first_new_message_time = message['data']['server_time']
                first_new_message_pos = pos
        return first_new_message_time, first_new_message_pos

    def insert_message(self, message):
        pos = len(self.messages) # 10
        while pos > 0 and self.messages[pos - 1]['data']['server_time'] > message['data']['server_time']:
            pos -= 1
        self.messages.insert(pos, message)
        return pos

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

