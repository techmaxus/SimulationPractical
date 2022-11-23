import time
import simpy.rt

def documentProcessing(env):
    while True:
        print("time ", env.now, "; Wall-clock Time: ", time.perf_counter())
        print("Reading Document")
        yield env.timeout(20)
        print("time ", env.now, "; Wall-clock Time: ", time.perf_counter())
        print("Submitting Document \n")
        yield env.timeout(10)

env = simpy.rt.RealtimeEnvironment(factor = 1, strict=False)
print("Let the time to read the document be: 20")
print("Let the time to submit the document be: 10")

env.process(documentProcessing(env))
env.run(until = 300)
