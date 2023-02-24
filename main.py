import simpy
import random

# Set simulation parameters
NUM_STATIONS = 5
SIM_TIME = 1000
CW_MIN = 16
CW_MAX = 1024

# Define Station class
class Station:
    def __init__(self, env, id):
        self.env = env
        self.id = id
        self.backoff = 0
        self.waiting = False

    def send_packet(self):
        print(f"Station {self.id} is sending a packet", env.now)
        self.waiting = False
        self.env.timeout(1)

    def wait_for_packet(self):
        print(f"Station {self.id} is waiting for a packet", env.now)
        self.waiting = True
        yield self.env.timeout(1)

    def start(self):
        while True:
            if self.backoff == 0:
                # Send packet
                self.send_packet()
                self.backoff = random.randint(0, CW_MIN - 1)
            elif self.waiting:
                # Wait for packet
                yield self.wait_for_packet()
                self.backoff = random.randint(0, CW_MIN - 1)
            else:
                # Decrement backoff
                self.backoff -= 1
                yield self.env.timeout(1)

# Define simulation function
def simulate(env, stations):
    for station in stations:
        env.process(station.start())

    while True:
        yield env.timeout(1)
        for station in stations:
            if station.waiting:
                continue
            elif station.backoff == 0:
                # Start waiting for packet
                env.process(station.wait_for_packet())
            else:
                # Decrement backoff
                station.backoff -= 1

# Initialize simulation environment
env = simpy.Environment()
stations = [Station(env, i) for i in range(NUM_STATIONS)]

# Run simulation
env.process(simulate(env, stations))
env.run(until=SIM_TIME)
"""This program defines a Station class that represents a single station in the network. Each station has a backoff counter that determines when it can transmit a packet, and a waiting flag that indicates whether it is currently waiting for a packet from another station.

The simulate function sets up the simulation environment and creates the Station objects. It then runs a loop that simulates the passage of time in the network. During each iteration of the loop, the function decrements each station's backoff counter and checks whether it is time for the station to transmit or wait for a packet.

The start method of the Station class is the main loop that each station runs during the simulation. It first checks whether it is waiting for a packet, and if so, it waits for one second before resetting its backoff counter. If the station's backoff counter reaches zero, it sends a packet and then sets its backoff counter to a new random value between 0 and CW_MIN - 1. Otherwise, it decrements its backoff counter and waits for one second."""