import threading
import time
import random
import logging
from typing import List
from src.os_simulator.process_sync.semaphore import CountingSemaphore

logger = logging.getLogger("Dining-Philosophers")

class Philosopher(threading.Thread):
    """
    Represent a philosopher using threads.
    Implements deadlock avoidance via resource ordering (Hierarchical Resource Allocation).
    """
    def __init__(self, id: int, left_fork: CountingSemaphore, right_fork: CountingSemaphore, 
                 left_idx: int, right_idx: int):
        super().__init__(name=f"Philosopher-{id}")
        self.id = id
        # In a hierarchical approach, we always pick up the lower-indexed fork first
        if left_idx < right_idx:
            self.first_fork = left_fork
            self.second_fork = right_fork
        else:
            self.first_fork = right_fork
            self.second_fork = left_fork
        
        self.running = True

    def run(self):
        while self.running:
            self.think()
            self.eat()

    def think(self):
        logger.info(f"Philosopher {self.id} is thinking...")
        time.sleep(random.uniform(0.5, 1.5))

    def eat(self):
        logger.info(f"Philosopher {self.id} is hungry. Trying to pick forks.")
        
        with self.first_fork:
            logger.info(f"Philosopher {self.id} picked up first fork.")
            with self.second_fork:
                logger.info(f"Philosopher {self.id} is EATING.")
                time.sleep(random.uniform(0.5, 1.0))
                logger.info(f"Philosopher {self.id} finished eating and put down second fork.")
            logger.info(f"Philosopher {self.id} put down first fork.")

    def stop(self):
        self.running = False

def run_dining_demo():
    """Demonstrates the Dining Philosophers problem with deadlock avoidance."""
    print(">>> DINING PHILOSOPHERS DEMO <<<\n")
    num_philosophers = 5
    forks = [CountingSemaphore(1) for _ in range(num_philosophers)]
    
    philosophers = []
    for i in range(num_philosophers):
        # Philosopher i has forks i and (i+1)%n
        left_idx = i
        right_idx = (i + 1) % num_philosophers
        p = Philosopher(i, forks[left_idx], forks[right_idx], left_idx, right_idx)
        philosophers.append(p)
    
    for p in philosophers:
        p.start()
    
    # Let them eat for some time
    time.sleep(5)
    
    print("\nStopping philosophers...")
    for p in philosophers:
        p.stop()
    for p in philosophers:
        p.join()
        
    print("\nDemonstration complete. No deadlocks occurred.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(threadName)s] %(message)s')
    run_dining_demo()