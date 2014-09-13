
class Scenario(object):
    def __init__(self, file_name):
        self.clients_number = 0
        self.events = []
        with open(file_name) as f:
            for line in f:
                line = line.split(';')[0].strip()
                if not len(line):
                    continue
                if not self.clients_number:
                    self.clients_number = int(line)
                    continue
                data = [x.strip() for x in line.split('|')]
                time = data[0]
                actions = data[1:]
                self.events.append({'time': int(time), 'actions': actions})

