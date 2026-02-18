import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.os_simulator.memory_management.page_replacement import fifo_replacement, lru_replacement, optimal_replacement

def run_replacement_demo():
    # Common reference string used in OS textbooks
    reference_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    frame_size = 3

    print(">>> PAGE REPLACEMENT ALGORITHMS COMPARISON <<<\n")
    print(f"Reference String: {reference_string}")
    print(f"Frame Size: {frame_size}\n")
    
    # 1. FIFO
    fifo_results = fifo_replacement(reference_string, frame_size)
    print(f"--- FIFO Results ---")
    print(f"Page Faults: {fifo_results['page_faults']}")
    print(f"Page Hits:   {fifo_results['page_hits']}")
    print(f"Fault Ratio: {fifo_results['fault_ratio']}\n")

    # 2. LRU
    lru_results = lru_replacement(reference_string, frame_size)
    print(f"--- LRU Results ---")
    print(f"Page Faults: {lru_results['page_faults']}")
    print(f"Page Hits:   {lru_results['page_hits']}")
    print(f"Fault Ratio: {lru_results['fault_ratio']}\n")

    # 3. Optimal
    opt_results = optimal_replacement(reference_string, frame_size)
    print(f"--- Optimal Results ---")
    print(f"Page Faults: {opt_results['page_faults']}")
    print(f"Page Hits:   {opt_results['page_hits']}")
    print(f"Fault Ratio: {opt_results['fault_ratio']}\n")

    print("Summary Comparison:")
    print(f"{'Algorithm':<10} | {'Faults':<7} | {'Hits':<7} | {'Ratio':<7}")
    print("-" * 40)
    print(f"{'FIFO':<10} | {fifo_results['page_faults']:<7} | {fifo_results['page_hits']:<7} | {fifo_results['fault_ratio']:<7}")
    print(f"{'LRU':<10} | {lru_results['page_faults']:<7} | {lru_results['page_hits']:<7} | {lru_results['fault_ratio']:<7}")
    print(f"{'Optimal':<10} | {opt_results['page_faults']:<7} | {opt_results['page_hits']:<7} | {opt_results['fault_ratio']:<7}")

if __name__ == "__main__":
    run_replacement_demo()
