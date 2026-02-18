import logging
from typing import List, Dict, Set

logger = logging.getLogger("Deadlock-Detection")

def detect_deadlock(allocation: Dict[int, List[int]], request: Dict[int, List[int]]) -> List[int]:
    """
    Detects deadlocked processes using a Wait-For Graph (WFG).
    
    A cycle in the WFG indicates a deadlock (assuming single-instance resources 
    or simplified dependency mapping).
    
    Args:
        allocation: {pid: [count_res_A, count_res_B, ...]}
        request: {pid: [count_res_A, count_res_B, ...]}
        
    Returns:
        List of PIDs involved in a deadlock.
    """
    # 1. Construct the Wait-For Graph (WFG)
    # Edge (Pi -> Pj) if Pi needs a resource held by Pj
    pids = list(allocation.keys())
    num_resources = len(next(iter(allocation.values()))) if allocation else 0
    
    wfg: Dict[int, Set[int]] = {pid: set() for pid in pids}
    
    for pi in pids:
        for r_idx in range(num_resources):
            if request[pi][r_idx] > 0:
                # Pi is waiting for resource r_idx. 
                # Find who currently holds resource r_idx.
                for pj in pids:
                    if pi != pj and allocation[pj][r_idx] > 0:
                        wfg[pi].add(pj)

    logger.info(f"Wait-For Graph constructed: {wfg}")

    # 2. Find nodes involved in cycles using DFS
    deadlocked_pids = set()
    
    def find_deadlocked_nodes(current_pid: int, visited: Set[int], path: List[int]):
        visited.add(current_pid)
        path.append(current_pid)
        
        for neighbor in wfg.get(current_pid, []):
            if neighbor in path:
                # Cycle detected! All nodes from neighbor to end of path are deadlocked.
                cycle_start_idx = path.index(neighbor)
                for i in range(cycle_start_idx, len(path)):
                    deadlocked_pids.add(path[i])
            elif neighbor not in visited:
                find_deadlocked_nodes(neighbor, visited, path)
        
        path.pop()

    visited = set()
    for pid in pids:
        if pid not in visited:
            find_deadlocked_nodes(pid, visited, [])

    result = sorted(list(deadlocked_pids))
    if result:
        logger.warning(f"Deadlock detected! Processes involved: {result}")
    else:
        logger.info("No deadlock detected.")
        
    return result