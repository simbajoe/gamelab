
class Network(object):
    MESSAGE_TYPE_CONNECT = 'connect'
    MESSAGE_TYPE_SEND = 'send'

    def __init__(self):
        self.server = None
        self.clients = {}
        self.client_id = 1

    def set_server(self, server):
        self.server = server

    def add_client(self, client):
        if self.server is None:
            raise "No server yet"
        client.id = self.client_id
        self.client_id += 1
        client.connect = lambda: self.server.queue_message({'type': self.MESSAGE_TYPE_CONNECT, 'client': client.id})
        client.send = lambda message: self.server.queue_message({'type': self.MESSAGE_TYPE_SEND, 'client': client.id, 'message': message})
        self.clients[client.id] = client



