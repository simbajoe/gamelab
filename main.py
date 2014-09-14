from scenario import Scenario
from simulation import Simulation

if __name__ == '__main__':

    scenario = Scenario('scenario/01.scn')
    simulation = Simulation(scenario)
    snapshots = [x for x in simulation.run()]

