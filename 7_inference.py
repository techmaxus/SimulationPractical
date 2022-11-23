#Theatre simulation with three counters 
#1. Movie Booking 
#2. Buying Food 
#3. Checking Ticket and going inside 
import simpy 
import random 
import statistics 
import matplotlib.pyplot as plt 

NUM_BOOK = 5 
NUM_FOOD = 5 
NUM_CHECK = 3 
NUM_USERS = 20 
ARRIVAL_LIMIT = 12 

class Theatre(object): 
  def __init__(self, num_book, num_food, num_check, num_users = 50): 
    self.env = simpy.Environment() 
    self.book_ctr = simpy.Resource(self.env, num_book) 
    self.food_ctr = simpy.Resource(self.env, num_food) 
    self.check_ctr = simpy.Resource(self.env, num_check) 
    self.generateUsers(num_users) 
  
  def generateUsers(self, num_users): 
    self.users = [ Customer(self, random.randint(0, ARRIVAL_LIMIT)) for i in range(num_users) ] 
  
  def displaySummary(self):
    for i in range(0, len(self.users)): 
        print("\n---Customer#"+str(i+1)+"---") 
        self.users[i].displaySummary()
    print("\n---Overall Metrics (in minutes)---")
    self.avg_book_wait = statistics.mean([c.book_wait for c in self.users])
    self.avg_food_wait = statistics.mean([c.food_wait for c in self.users])
    self.avg_check_wait = statistics.mean([c.check_wait for c in self.users])
    self.avg_wait = statistics.mean([c.total_wait for c in self.users])
    self.avg_service_time = statistics.mean([c.total_service_time for c in self.users])
    self.finish_time = self.env.now
    print("average wait at booking counter:", self.avg_book_wait) 
    print("average wait at food counter:", self.avg_food_wait) 
    print("average wait at checking counter:", self.avg_check_wait) 
    print("average wait time: ", self.avg_wait)
    print("average service time: ", self.avg_service_time) 
    print("time until all bookings finish:", self.finish_time)
    
class Customer(object):
    def __init__(self, theatre, time):
        self.theatre = theatre
        self.arrival_time = time
        self.action = self.theatre.env.process(self.run())
    def run(self):
        yield self.theatre.env.timeout(self.arrival_time - self.theatre.env.now)
        print("arrived")
        #booking ticket
        with self.theatre.book_ctr.request() as request:
            self.book_start = self.theatre.env.now
            yield request
            self.book_wait = self.theatre.env.now - self.book_start
            yield self.theatre.env.timeout(random.randint(2,5)) 
        #2 to 5 minutes for booking the ticket
        print('ticket booked')
        #buying food
        choice = random.choice([True, False])
        if(choice):
            with self.theatre.food_ctr.request() as request:
                self.food_start = self.theatre.env.now
                yield request
                self.food_wait = self.theatre.env.now - self.food_start
                yield self.theatre.env.timeout(random.randint(4,10)) 
            #4 to 10 minutes for buying food
            print("bought food")
        else :
            self.food_wait = 0
            print("not buying food")
        #checking ticket
        with self.theatre.check_ctr.request() as request:
            self.check_start = self.theatre.env.now
            yield request
            self.check_wait = self.theatre.env.now - self.check_start
            yield self.theatre.env.timeout(random.randint(1,3)) 
        #1 to 3 minutes for checking the ticket
        print("going in the theatre")
        self.total_wait = self.book_wait + self.food_wait + self.check_wait
        self.total_service_time = self.theatre.env.now - self.arrival_time

    def displaySummary(self):
        print("arrival time:", self.arrival_time)
        print("wait in booking counter:", self.book_wait)
        print("wait in food counter:", self.food_wait)
        print("wait in checking counter:", self.check_wait)
        print("total wait:", self.total_wait)
        print("total service time:", self.total_service_time)

def main(): 
    t = Theatre(NUM_BOOK, NUM_FOOD, NUM_CHECK, NUM_USERS)
    t.env.run()
    t.displaySummary()


if __name__ == "__main__": 
  main()