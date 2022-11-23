#Import important library
from random import randint
import simpy

## Inital variables
TALKS_PER_SESSION = 2
TALK_LENGTH = 45
BREAK_LENGTH = 15
ATTENDEES = 3

def attendee(env, name, knowledge=0, hunger=0):
    talks = 0
    breaks = 0
    #Repeat sessions
    while True:
        # Visit talks
        for i in range(TALKS_PER_SESSION):
            print("Talk {0} begins at {1}".format(talks+1, env.now))
            knowledge += randint(0, 3) / (1 + hunger)
            hunger += randint(1, 4)
            talks += 1
            yield env.timeout(TALK_LENGTH)
            print(f"Talk {talks} ends at {env.now}")
        print("Attendee %s finished talks with knowledge %.2f and hunger %.2f" %( name, knowledge, hunger))
        #Take a break, Go to buffet
        food = randint(3, 12)
        hunger -= min(food, hunger)
        yield env.timeout(BREAK_LENGTH)
        print("Attendee %s finished eating with hunger %.2f " %(name, hunger))

# Run Simulation
env = simpy.Environment()
for i in range(ATTENDEES):
    env.process(attendee(env, i))
env.run(until=120)