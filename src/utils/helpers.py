import copy
from typing import List, Any
import logging

logger = logging.getLogger("Helpers")

def deep_copy_process_list(process_list: List[Any]) -> List[Any]:
    """
    Creates a deep copy of a list of Process objects to avoid state leakage
    between different simulation runs.
    """
    return copy.deepcopy(process_list)

def format_timeline(timeline: List[tuple]) -> str:
    """
    Formats a simulation timeline into a readable string.
    Example: [(1, 0, 5), ("CS", 5, 6)] -> "0-5: P1, 5-6: CS"
    """
    parts = []
    for pid, start, end in timeline:
        label = f"P{pid}" if isinstance(pid, int) else str(pid)
        parts.append(f"{start}-{end}: {label}")
    return ", ".join(parts)

def generate_pid(existing_pids: List[int]) -> int:
    """
    Generates a new unique PID based on existing ones.
    """
    if not existing_pids:
        return 1
    return max(existing_pids) + 1

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Performs division safely, handling division by zero.
    """
    try:
        return numerator / denominator
    except ZeroDivisionError:
        logger.warning("Division by zero encountered. Returning default value.")
        return default

def pretty_print_table(headers: List[str], data: List[List[Any]]):
    """
    Prints a formatted table to the console.
    """
    if not data:
        print("No data to display.")
        return

    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in data:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))

    # Print headers
    header_row = " | ".join(f"{str(h):<{widths[i]}}" for i, h in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))

    # Print data
    for row in data:
        print(" | ".join(f"{str(v):<{widths[i]}}" for i, v in enumerate(row)))