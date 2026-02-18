import logging
from typing import Any, List, Dict, Optional, Tuple

logger = logging.getLogger("Bankers-Algorithm")

class BankersAlgorithm:
    """
    Implementation of the Banker's Algorithm for Deadlock Avoidance.
    
    Tracks Available, Allocation, Max, and Need matrices to ensure the system
    stays in a safe state.
    """

    def __init__(self, total_resources: List[int]):
        """
        Initializes the algorithm with the total resource vector.
        
        Args:
            total_resources: List or Vector of total counts for each resource type.
        """
        self.total_resources = total_resources
        self.num_types = len(total_resources)
        
        self.available = list(total_resources)
        self.allocation: Dict[int, List[int]] = {}
        self.max_demand: Dict[int, List[int]] = {}
        self.need: Dict[int, List[int]] = {}

        logger.info(f"Banker's Algorithm initialized with resources: {self.total_resources}")

    def add_process(self, pid: int, max_vector: List[int]) -> bool:
        """
        Registers a process and its maximum resource demand.
        """
        if len(max_vector) != self.num_types:
            logger.error(f"Invalid max vector size for PID {pid}. Expected {self.num_types}.")
            return False

        # Basic check: Can this process even run given total resources?
        for i in range(self.num_types):
            if max_vector[i] > self.total_resources[i]:
                logger.error(f"PID {pid} demands more of resource {i} than system total.")
                return False

        self.max_demand[pid] = list(max_vector)
        self.allocation[pid] = [0] * self.num_types
        self.need[pid] = list(max_vector)
        
        logger.info(f"Process {pid} added. Max: {max_vector}")
        return True

    def request_resources(self, pid: int, request: List[int]) -> bool:
        """
        Processes a resource request using the Banker's Algorithm criteria.
        
        Criteria:
        1. Request <= Need (Process hasn't exceeded its stated max)
        2. Request <= Available (System has enough to grant right now)
        3. Safety Check (Pretend to grant, see if system remains safe)
        """
        if pid not in self.allocation:
            logger.error(f"Process {pid} not registered.")
            return False

        # 1. Check Request vs Need
        for i in range(self.num_types):
            if request[i] > self.need[pid][i]:
                logger.error(f"PID {pid} requested more than its declared Need.")
                return False

        # 2. Check Request vs Available
        for i in range(self.num_types):
            if request[i] > self.available[i]:
                logger.info(f"PID {pid} must wait: insufficient available resources.")
                return False

        # 3. Safety Check - Predictive grant
        # Backup original state
        orig_available = list(self.available)
        orig_allocation = list(self.allocation[pid])
        orig_need = list(self.need[pid])

        # Pretend allocation
        for i in range(self.num_types):
            self.available[i] -= request[i]
            self.allocation[pid][i] += request[i]
            self.need[pid][i] -= request[i]

        is_safe, sequence = self.safe_state_check()

        if is_safe:
            logger.info(f"Request granted to PID {pid}. System remains safe (Sequence: {sequence}).")
            return True
        else:
            # Granting would lead to unsafe state - Rollback
            self.available = orig_available
            self.allocation[pid] = orig_allocation
            self.need[pid] = orig_need
            logger.warning(f"Request denied to PID {pid}. Granting would lead to unsafe state.")
            return False

    def release_resources(self, pid: int, release: List[int]) -> None:
        """
        Releases allocated resources back to the available pool.
        """
        if pid not in self.allocation:
            return

        for i in range(self.num_types):
            # Clamp release to what's actually held
            actual_release = min(release[i], self.allocation[pid][i])
            self.allocation[pid][i] -= actual_release
            self.available[i] += actual_release
            self.need[pid][i] = self.max_demand[pid][i] - self.allocation[pid][i]

        logger.info(f"PID {pid} released {release}. Available: {self.available}")

    def safe_state_check(self) -> Tuple[bool, List[int]]:
        """
        Safety Algorithm to determine if the system is in a safe state.
        Returns (is_safe, execution_sequence).
        """
        work = list(self.available)
        finish = {pid: False for pid in self.allocation.keys()}
        sequence = []

        while len(sequence) < len(self.allocation):
            found_at_least_one = False
            for pid, done in finish.items():
                if not done:
                    # Can this process finish with current 'work'?
                    can_finish = True
                    for i in range(self.num_types):
                        if self.need[pid][i] > work[i]:
                            can_finish = False
                            break
                    
                    if can_finish:
                        # Assume process finishes and returns its allocation to 'work'
                        for i in range(self.num_types):
                            work[i] += self.allocation[pid][i]
                        finish[pid] = True
                        sequence.append(pid)
                        found_at_least_one = True
            
            if not found_at_least_one:
                break

        return (len(sequence) == len(self.allocation)), sequence

    def get_matrices(self) -> Dict[str, Any]:
        """Returns current algorithm state for visualization."""
        return {
            "available": self.available,
            "allocation": self.allocation,
            "max": self.max_demand,
            "need": self.need
        }