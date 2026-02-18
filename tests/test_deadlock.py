import unittest
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from os_simulator.deadlock.bankers_algorithm import BankersAlgorithm
from os_simulator.deadlock.deadlock_detection import detect_deadlock

class TestBankersAlgorithm(unittest.TestCase):
    def setUp(self):
        # Total resources: 10, 5, 7
        self.total = [10, 5, 7]
        self.ba = BankersAlgorithm(self.total)

    def test_safe_state(self):
        """Tests safe state detection with the classic 5-process scenario."""
        # Resources: A=10, B=5, C=7
        # P0: Max [7,5,3], Alloc [0,1,0]
        # P1: Max [3,2,2], Alloc [2,0,0]
        # P2: Max [9,0,2], Alloc [3,0,2]
        # P3: Max [2,2,2], Alloc [2,1,1]
        # P4: Max [4,3,3], Alloc [0,0,2]
        # Current Available: [3, 3, 2]
        
        self.ba.add_process(0, [7, 5, 3])
        self.ba.add_process(1, [3, 2, 2])
        self.ba.add_process(2, [9, 0, 2])
        self.ba.add_process(3, [2, 2, 2])
        self.ba.add_process(4, [4, 3, 3])
        
        # Manually set state
        self.ba.available = [3, 3, 2]
        self.ba.allocation[0] = [0, 1, 0]; self.ba.need[0] = [7, 4, 3]
        self.ba.allocation[1] = [2, 0, 0]; self.ba.need[1] = [1, 2, 2]
        self.ba.allocation[2] = [3, 0, 2]; self.ba.need[2] = [6, 0, 0]
        self.ba.allocation[3] = [2, 1, 1]; self.ba.need[3] = [0, 1, 1]
        self.ba.allocation[4] = [0, 0, 2]; self.ba.need[4] = [4, 3, 1]
        
        is_safe, sequence = self.ba.safe_state_check()
        self.assertTrue(is_safe)
        self.assertEqual(len(sequence), 5)
        # One possible safe sequence: [1, 3, 4, 0, 2]
        self.assertEqual(sequence[0], 1)

    def test_request_denial_unsafe(self):
        """Tests that a request leading to an unsafe state is denied."""
        self.ba.add_process(0, [10, 10, 10])
        # Grant almost everything
        self.ba.available = [1, 1, 1]
        self.ba.allocation[0] = [9, 9, 9]
        self.ba.need[0] = [1, 1, 1]
        
        self.ba.add_process(1, [5, 5, 5])
        # P1 requests [2, 2, 2]. Only [1, 1, 1] available.
        # Even if we had [2, 2, 2], it might be unsafe.
        # But here it fails early on "Request <= Available"
        granted = self.ba.request_resources(1, [2, 2, 2])
        self.assertFalse(granted)

    def test_release_logic(self):
        """Tests resource release accounting."""
        self.ba.add_process(0, [5, 5, 5])
        self.ba.allocation[0] = [2, 2, 2]
        self.ba.available = [3, 3, 3]
        
        self.ba.release_resources(0, [2, 2, 2])
        self.assertEqual(self.ba.available, [5, 5, 5])
        self.assertEqual(self.ba.allocation[0], [0, 0, 0])

class TestDeadlockDetection(unittest.TestCase):
    def test_no_deadlock(self):
        """Tests acyclic wait-for graph."""
        # P0 waiting for P1, P1 finished
        alloc = {0: [1, 0], 1: [0, 1]}
        req = {0: [0, 1], 1: [0, 0]}
        result = detect_deadlock(alloc, req)
        self.assertEqual(result, [])

    def test_simple_deadlock(self):
        """Tests circular wait between two processes."""
        # P0 holds R0, wants R1
        # P1 holds R1, wants R0
        alloc = {0: [1, 0], 1: [0, 1]}
        req = {0: [0, 1], 1: [1, 0]}
        result = detect_deadlock(alloc, req)
        self.assertEqual(len(result), 2)
        self.assertIn(0, result)
        self.assertIn(1, result)

    def test_complex_loop(self):
        """Tests deadlock in a larger P0 -> P1 -> P2 -> P0 chain."""
        alloc = {0: [1,0,0], 1: [0,1,0], 2: [0,0,1]}
        req = {0: [0,1,0], 1: [0,0,1], 2: [1,0,0]}
        result = detect_deadlock(alloc, req)
        self.assertEqual(len(result), 3)
        self.assertEqual(result, [0, 1, 2])

if __name__ == '__main__':
    unittest.main()