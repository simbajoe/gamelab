from server import Server

class ServerDumb(Server):
    def __init__(self, model_step, allowed_lag_compensation_interval, snapshot_interval):
        super(ServerDumb, self).__init__(model_step, allowed_lag_compensation_interval, snapshot_interval)


