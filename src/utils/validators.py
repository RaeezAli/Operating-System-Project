from typing import List, Dict, Any
import logging

logger = logging.getLogger("Validators")

def validate_process_input(arrival: int, burst: int, priority: int = 0) -> bool:
    """
    Validates process parameters.
    """
    if arrival < 0 or burst <= 0:
        logger.error(f"Invalid process timing: arrival={arrival}, burst={burst}")
        return False
    return True

def validate_reference_string(ref_string: List[int]) -> bool:
    """
    Checks if a page reference string is valid (non-negative integers).
    """
    if not ref_string:
        return False
    return all(isinstance(p, int) and p >= 0 for p in ref_string)

def validate_resource_matrices(allocation: Dict[int, List[int]], 
                               max_demand: Dict[int, List[int]]) -> bool:
    """
    Ensures allocation and max matrices are consistent for Banker's Algorithm.
    """
    if not allocation or not max_demand:
        return False
    
    for pid in allocation:
        if pid not in max_demand:
            logger.error(f"PID {pid} missing from max_demand matrix.")
            return False
        if len(allocation[pid]) != len(max_demand[pid]):
            logger.error(f"Matrix dimension mismatch for PID {pid}.")
            return False
    return True

def validate_scheduler_choice(choice: str, available_schedulers: List[str]) -> bool:
    """
    Validates if the selected scheduler exists in the system.
    """
    if choice not in available_schedulers:
        logger.error(f"Scheduler '{choice}' is not supported.")
        return False
    return True