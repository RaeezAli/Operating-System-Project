from typing import List, Dict, Any

def fifo_replacement(reference_string: List[int], frame_size: int) -> Dict[str, Any]:
    """
    First-In-First-Out (FIFO) Page Replacement Algorithm.
    Replaces the page that was brought in earliest.
    """
    frames = []
    faults = 0
    hits = 0

    for page in reference_string:
        if page in frames:
            hits += 1
        else:
            faults += 1
            if len(frames) < frame_size:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)

    total = len(reference_string)
    return {
        "page_faults": faults,
        "page_hits": hits,
        "fault_ratio": round(faults / total, 2) if total > 0 else 0
    }

def lru_replacement(reference_string: List[int], frame_size: int) -> Dict[str, Any]:
    """
    Least Recently Used (LRU) Page Replacement Algorithm.
    Replaces the page that has not been used for the longest period of time.
    """
    frames = []
    faults = 0
    hits = 0

    for page in reference_string:
        if page in frames:
            hits += 1
            # Move the hit page to the end (most recently used)
            frames.remove(page)
            frames.append(page)
        else:
            faults += 1
            if len(frames) < frame_size:
                frames.append(page)
            else:
                # Remove the first element (least recently used)
                frames.pop(0)
                frames.append(page)

    total = len(reference_string)
    return {
        "page_faults": faults,
        "page_hits": hits,
        "fault_ratio": round(faults / total, 2) if total > 0 else 0
    }

def optimal_replacement(reference_string: List[int], frame_size: int) -> Dict[str, Any]:
    """
    Optimal Page Replacement Algorithm.
    Replaces the page that will not be used for the longest period of time in the future.
    """
    frames = []
    faults = 0
    hits = 0

    for i in range(len(reference_string)):
        page = reference_string[i]
        
        if page in frames:
            hits += 1
        else:
            faults += 1
            if len(frames) < frame_size:
                frames.append(page)
            else:
                # Decide which page to replace
                farthest_idx = -1
                page_to_replace = -1
                
                for f in frames:
                    try:
                        # Find the next occurrence of f in the remainder of the reference string
                        next_usage = reference_string.index(f, i + 1)
                        if next_usage > farthest_idx:
                            farthest_idx = next_usage
                            page_to_replace = f
                    except ValueError:
                        # If page f is never used again, select it for replacement
                        page_to_replace = f
                        break
                
                frames[frames.index(page_to_replace)] = page

    total = len(reference_string)
    return {
        "page_faults": faults,
        "page_hits": hits,
        "fault_ratio": round(faults / total, 2) if total > 0 else 0
    }