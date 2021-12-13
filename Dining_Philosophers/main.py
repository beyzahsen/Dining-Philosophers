import random
import time
from threading import Lock, Thread


class DiningPhilosophers:
    def __init__(self, number_of_phis, meal_size):
        self.meals = [meal_size for _ in range(number_of_phis)]
        self.chopsticks = [Lock() for _ in range(number_of_phis)]

    def philosopher(self, i):
        while self.meals[i] > 0:
            print("Philosopher %d is thinking" % i)
            time.sleep(random.random())
            self.chopsticks[i].acquire()
            print("Philosopher %d is picked the chopstick %d" % (i, i))
            time.sleep(random.random())
            if self.chopsticks[(i + 1) % 5].locked():
                self.chopsticks[i].release()
            else:
                self.chopsticks[(i + 1) % 5].acquire()
                print("Philosopher %d has two chopsticks" % i)
                time.sleep(random.random())
                print("Philosopher %d is eating" % i)
                self.meals[i] -= 1
                self.chopsticks[(i + 1) % 5].release()
                self.chopsticks[i].release()


if __name__ == "__main__":
    n = 5
    m = 10
    dining_philos = DiningPhilosophers(n, m)
    philosophers = [Thread(target=dining_philos.philosopher, args=(i,)) for i in range(n)]
    for philosopher in philosophers:
        philosopher.start()

    for philosopher in philosophers:
        philosopher.join()
