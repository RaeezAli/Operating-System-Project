import unittest
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from os_simulator.process import Process
from os_simulator.scheduling.fcfs import FCFSScheduler
from os_simulator.scheduling.round_robin import RoundRobinScheduler
from os_simulator.scheduling.priority import PriorityScheduler

class TestSchedulers(unittest.TestCase):

    def setUp(self):
        # Create a standard set of processes for testing
        # P1: Arrival 0, Burst 5, Priority 3
        # P2: Arrival 1, Burst 3, Priority 1 (High)
        # P3: Arrival 2, Burst 4, Priority 2
        self.p1 = Process(1, "P1", 0, 5, 3)
        self.p2 = Process(2, "P2", 1, 3, 1)
        self.p3 = Process(3, "P3", 2, 4, 2)
        self.processes = [self.p1, self.p2, self.p3]

    def test_fcfs_scheduling(self):
        """Tests FCFS execution order and metrics."""
        scheduler = FCFSScheduler()
        timeline = scheduler.schedule(self.processes)
        
        # Expected Timeline:
        # P1: 0-5
        # P2: 5-8
        # P3: 8-12
        expected_timeline = [(1, 0, 5), (2, 5, 8), (3, 8, 12)]
        self.assertEqual(timeline, expected_timeline)
        
        # Verify Metrics
        # P1: completion 5, arrival 0, burst 5 -> TAT=5, WT=0
        # P2: completion 8, arrival 1, burst 3 -> TAT=7, WT=4
        # P3: completion 12, arrival 2, burst 4 -> TAT=10, WT=6
        self.assertEqual(self.p1.turnaround_time, 5)
        self.assertEqual(self.p1.waiting_time, 0)
        self.assertEqual(self.p2.turnaround_time, 7)
        self.assertEqual(self.p2.waiting_time, 4)
        self.assertEqual(self.p3.turnaround_time, 10)
        self.assertEqual(self.p3.waiting_time, 6)

    def test_round_robin_scheduling(self):
        """Tests Round Robin preemption and quantum behavior."""
        # Use quantum=2
        scheduler = RoundRobinScheduler(quantum=2)
        timeline = scheduler.schedule(self.processes)
        
        # Expected Timeline (Quantum 2):
        # Time 0: P1 arrives. Runs [0-2]. Remaining: P1=3. Ready: [P1]
        # Time 1: P2 arrives.
        # Time 2: P1 preempted, moved to end. P3 arrives. Ready: [P2, P3, P1]
        # Time 2-4: P2 runs. Remaining: P2=1. Ready: [P3, P1, P2]
        # Time 4-6: P3 runs. Remaining: P3=2. Ready: [P1, P2, P3]
        # Time 6-8: P1 runs. Remaining: P1=1. Ready: [P2, P3, P1]
        # Time 8-9: P2 runs. Finished. Ready: [P3, P1]
        # Time 9-11: P3 runs. Finished. Ready: [P1]
        # Time 11-12: P1 runs. Finished.
        
        expected_timeline = [
            (1, 0, 2), (2, 2, 4), (3, 4, 6), 
            (1, 6, 8), (2, 8, 9), (3, 9, 11), (1, 11, 12)
        ]
        self.assertEqual(timeline, expected_timeline)
        
        # Verify Completion Times
        # P2 finishes at 9. Arrival 1. TAT=8. WT=5 (8-3 burst)
        # P3 finishes at 11. Arrival 2. TAT=9. WT=5 (9-4 burst)
        # P1 finishes at 12. Arrival 0. TAT=12. WT=7 (12-5 burst)
        self.assertEqual(self.p2.turnaround_time, 8)
        self.assertEqual(self.p3.turnaround_time, 9)
        self.assertEqual(self.p1.turnaround_time, 12)

    def test_priority_scheduling(self):
        """Tests Non-preemptive Priority scheduling."""
        scheduler = PriorityScheduler()
        timeline = scheduler.schedule(self.processes)
        
        # Expected Timeline (Higher value = Higher priority? Or Lower value = Higher priority?)
        # BaseScheduler in priority.py says: "assuming higher value = higher priority"
        # Current Priorities: P1=3, P2=1, P3=2
        # Order: P1 (arrives at 0, runs 0-5), then P3 (priority 2), then P2 (priority 1)
        # (Wait, if higher = higher priority, P1 is highest)
        
        # Time 0: P1 arrives. Runs [0-5].
        # Time 1: P2 arrives.
        # Time 2: P3 arrives.
        # Time 5: P1 finishes. Ready: [P2, P3]. Priority: P2=1, P3=2. 
        # Select P1 (3) -> Then P3 (2) -> Then P2 (1)
        
        expected_timeline = [(1, 0, 5), (3, 5, 9), (2, 9, 12)]
        self.assertEqual(timeline, expected_timeline)
        
        # Verify Metrics
        # P3: completion 9, arrival 2 -> TAT=7, WT=3
        self.assertEqual(self.p3.turnaround_time, 7)
        self.assertEqual(self.p3.waiting_time, 3)

    def test_idle_handling(self):
        """Tests how schedulers handle gaps in arrival times."""
        p_late = Process(4, "P4", 20, 5) # Arrives much later
        scheduler = FCFSScheduler()
        timeline = scheduler.schedule([self.p1, p_late])
        
        # P1: 0-5
        # Idle: 5-20
        # P4: 20-25
        expected_timeline = [(1, 0, 5), (4, 20, 25)]
        self.assertEqual(timeline, expected_timeline)

if __name__ == '__main__':
    unittest.main()