import random
import time
from threading import Semaphore, Thread


class DiningPhilosophers:
    def __init__(self, number_of_philos, meal_size=9):
        self.meals = [meal_size for _ in range(number_of_philos)]
        self.chopsticks = [Semaphore(value=1) for _ in range(number_of_philos)]
        self.n = number_of_philos
        self.status = ['T' for _ in range(number_of_philos)]
        self.chopsticks_hold = [0 for _ in range(number_of_philos)]

    def philosopher(self, i):
        while self.meals[i] > 0:
            self.status[i] = 'T'
            time.sleep(random.random())
            if self.chopsticks[i].acquire(timeout=1):
                self.chopsticks_hold[i] = 1
                time.sleep(random.random())
                if self.chopsticks[(i + 1) % self.n].acquire(timeout=1):
                    self.chopsticks_hold[i] = 2
                    self.status[i] = 'E'
                    time.sleep(random.random())
                    self.meals[i] = 1
                    self.chopsticks_hold[i] = 1
                    self.chopsticks[(i + 1) % self.n].release()
                self.chopsticks_hold[i] = 0
                self.chopsticks[i].release()
                self.status = 'T'


def main():
    n = 5
    m = 9
    dining_philosophers = DiningPhilosophers(n, m)
    philosophers = [Thread(target=dining_philosophers.philosopher,args=(i,)) for i in range(n)]
    for philosopher in philosophers:
        philosopher.start()
    while sum(dining_philosophers.meals) > 0:
        print(dining_philosophers.status)
        time.sleep(random.random())
