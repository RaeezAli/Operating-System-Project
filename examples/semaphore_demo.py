import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import threading
import time
import random
import logging
from src.os_simulator.process_sync.semaphore import CountingSemaphore

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(threadName)s] %(message)s')
logger = logging.getLogger("Sync-Demo")

def access_resource(user_id: int, semaphore: CountingSemaphore):
    """Simulates a user requesting and using a resource from a limited pool."""
    logger.info(f"User {user_id} requesting a resource...")
    
    with semaphore:
        logger.info(f"User {user_id} ACQUIRED resource. Logic: Working...")
        # Simulate work
        time.sleep(random.uniform(0.5, 2.0))
        logger.info(f"User {user_id} RELEASING resource.")

def run_semaphore_demo():
    print(">>> COUNTING SEMAPHORE SYNC DEMO <<<\n")
    print("Scenario: 3 Shared Printers, 8 Users trying to print simultaneously.\n")

    # 1. Initialize semaphore with pool size of 3
    printer_pool = CountingSemaphore(initial_value=3)
    
    # 2. Start multiple threads representing users
    threads = []
    for i in range(8):
        t = threading.Thread(target=access_resource, args=(i, printer_pool), name=f"UserThread-{i}")
        threads.append(t)
        t.start()
        # Stagger intake slightly
        time.sleep(0.1)

    # 3. Wait for all to finish
    for t in threads:
        t.join()

    print("\nAll users have finished printing. Demonstration complete.")

if __name__ == "__main__":
    run_semaphore_demo()
