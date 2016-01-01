from client import Client

class ClientDumb(Client):
    def __init__(self, model_step):
        super(ClientDumb, self).__init__(model_step)

