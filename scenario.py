
class Scenario(object):
    def __init__(self, file_name):
        lines = self.get_lines(file_name)

        self.clients_number = self.read_int(lines)
        self.start = self.read_int(lines)
        self.end = self.read_int(lines)
        self.model_step = self.read_int(lines)
        self.client_interpolation_backstep = self.read_int(lines)
        self.allowed_lag_compensation_interval = self.read_int(lines)
        self.snapshot_interval = self.read_int(lines)

        self.read_void(lines)

        self.props = self.read_props(lines)

        self.read_void(lines)

        self.events = self.read_events(lines)

    def get_lines(self, file_name):
        lines = []
        for line in open(file_name):
            line = line.split(';')[0].strip()
            if not len(line):
                continue
            lines.append(line)
        return lines

    def read_int(self, lines):
        return int(lines.pop(0))

    def read_props(self, lines):
        props = {
            'local_time_start': self.read_prop(lines, int),
            'ping': self.read_prop(lines, int),
            'main_loop_period': self.read_prop(lines, int),
        }
        return props

    def read_prop(self, lines, cast=None):
        props = self.read_piped_line(lines)
        return {
            'server': self.cast_prop(props.pop(0), cast),
            'client': [self.cast_prop(prop, cast) for prop in props]
        }

    def cast_prop(self, prop, cast=None):
        if not len(prop):
            return None
        if cast:
            return cast(prop)
        return prop

    def read_events(self, lines):
        events = {}
        while len(lines):
            data = self.read_piped_line(lines)
            time = data[0]
            events[int(time)] = [x if len(x) else None for x in data[1:]]
        return events

    def read_piped_line(self, lines):
        return [x.strip() for x in lines.pop(0).split('|')]

    def read_void(self, lines):
        line = lines.pop(0)
        if line != '--':
            raise "Wrong format, expecting --"

