from player import Player


class World(object):

    MESSAGE_TYPE_CONNECT = 'connect'
    MESSAGE_TYPE_INPUT = 'input'

    def __init__(self, time):
        self.time = time
        self.players = {}

    def apply_messages(self, messages):
        for message in messages:
            if message['type'] == World.MESSAGE_TYPE_CONNECT:
                player_id = message['client_id']
                x, y = self.get_player_starting_position(player_id)
                self.players[player_id] = Player(x, y)
            if message['type'] == World.MESSAGE_TYPE_INPUT:
                player_id = message['client_id']
                player = self.players[player_id]
                player.apply_input(message['data']['keys'])

    def get_player_starting_position(self, player_id):
        raise NotImplementedError()

    def model(self, step):
        for player_id, player in self.players.items():
            player.model(step)
        self.time += step

    def snapshot(self):
        return {
            'time': self.time,
            'players': {player_id: player.snapshot() for player_id, player in self.players.items()}
        }

    @staticmethod
    def from_snapshot(snapshot):
        world = World(snapshot['time'])
        world.players = {player_id: Player.from_snapshot(player) for player_id, player in snapshot['players'].items()}
        return world
