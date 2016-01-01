from scenario import Scenario
from simulation import Simulation
import json
from copy import deepcopy

def snapshot_remove_time(snapshot):
    if type(snapshot) is dict:
        if 'time' in snapshot:
            snapshot.pop('time', None)
        for key, value in snapshot.items():
            snapshot_remove_time(value)
    if type(snapshot) is list:
        for value in snapshot:
            snapshot_remove_time(value)

if __name__ == '__main__':

    scenario = Scenario('scenario/01.scn')
    simulation = Simulation(scenario)
    snapshots = [x for x in simulation.run()]
    last_snapshot_string = ""
    print "var res = ["
    for snapshot in snapshots:
        snapshot_string = json.dumps(snapshot, sort_keys=True, indent=4)
        snapshot_copy = deepcopy(snapshot)
        snapshot_remove_time(snapshot_copy)
        snapshot_string_without_time = json.dumps(snapshot_copy)
        if snapshot_string_without_time != last_snapshot_string:
            print snapshot_string
            print ",\n"
            last_snapshot_string = snapshot_string_without_time
    print "]"


