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
    self.avg_book_wait = statistics.mean([c.book_wait for c in self.users]) 
    self.avg_food_wait = statistics.mean([c.food_wait for c in self.users]) 
    self.avg_check_wait = statistics.mean([c.check_wait for c in self.users]) 
    self.avg_wait = statistics.mean([c.total_wait for c in self.users]) 
    self.avg_service_time = statistics.mean([c.total_service_time for c in self.users]) 
    self.finish_time = self.env.now
    
class Customer(object): 
  def __init__(self, theatre, time): 
    self.theatre = theatre 
    self.arrival_time = time 
    self.action = self.theatre.env.process(self.run()) 
  
  def run(self): 
    yield self.theatre.env.timeout(self.arrival_time - self.theatre.env.now)
    #booking ticket 
    with self.theatre.book_ctr.request() as request: 
      self.book_start = self.theatre.env.now 
      yield request 
      self.book_wait = self.theatre.env.now - self.book_start 
      yield self.theatre.env.timeout(random.randint(2,5)) #2 to 5 minutes for booking the ticket 
    #buying food 
    choice = random.choice([True, False]) 
    if(choice): 
      with self.theatre.food_ctr.request() as request: 
        self.food_start = self.theatre.env.now 
        yield request 
        self.food_wait = self.theatre.env.now - self.food_start 
        yield self.theatre.env.timeout(random.randint(4,10)) #4 to 10 minutes for buying food 
    else :
      self.food_wait = 0 
    #checking ticket 
    with self.theatre.check_ctr.request() as request: 
      self.check_start = self.theatre.env.now 
      yield request 
      self.check_wait = self.theatre.env.now - self.check_start 
      yield self.theatre.env.timeout(random.randint(1,3)) #1 to 3 minutes for checking the ticket 
      self.total_wait = self.book_wait + self.food_wait + self.check_wait 
      self.total_service_time = self.theatre.env.now - self.arrival_time 
          
  def displaySummary(self): 
    pass

def main(): 
  res1 = [] 
  for n_book in range(1,11): 
    t = Theatre(n_book, NUM_FOOD, NUM_CHECK, NUM_USERS) 
    t.env.run() 
    t.displaySummary() 
    res1.append(t) 
  
  res2 = [] 
  for n_food in range(1,11): 
    t = Theatre(NUM_BOOK, n_food, NUM_CHECK, NUM_USERS) 
    t.env.run() 
    t.displaySummary() 
    res2.append(t) 
  
  res3 = [] 
  for n_check in range(1,11): 
    t = Theatre(NUM_BOOK, NUM_FOOD, n_check, NUM_USERS) 
    t.env.run() 
    t.displaySummary() 
    res3.append(t) 
  
  res4 = [] 
  for n_users in range(10, 500, 10): 
    t = Theatre(NUM_BOOK, NUM_FOOD, NUM_CHECK, n_users) 
    t.env.run() 
    t.displaySummary() 
    res4.append(t) 
    
  fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize = (10, 10)) 
  ax[0][0].plot(range(1, 11), [i.avg_service_time for i in res1]) 
  ax[0][0].set(title = 'v/s no. of booking counters', xlabel='number of booking counters', ylabel = 'avg. service time(min)') 
  ax[0][1].plot(range(1, 11), [i.avg_service_time for i in res2]) 
  ax[0][1].set(title = 'v/s no. of food counters', xlabel='number of food counters', ylabel = 'avg. service time(min)') 
  ax[1][0].plot(range(1, 11), [i.avg_service_time for i in res3]) 
  ax[1][0].set(title = 'v/s no. of checking counters', xlabel='number of checking counters', ylabel = 'avg. service time(min)') 
  ax[1][1].plot(range(10, 500, 10), [i.avg_service_time for i in res4]) 
  ax[1][1].set(title = 'v/s no. of customers', xlabel='number of customers', ylabel = 'avg. service time(min)') 
  fig.savefig('plot_inference_result.png') 
  plt.show()

if __name__ == "__main__": 
  main()