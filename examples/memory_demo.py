import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.os_simulator.kernel import Kernel
from src.os_simulator.process import Process
from src.os_simulator.memory_management.paging import PagingMemoryManager

def run_memory_demo():
    print(">>> PAGING MEMORY MANAGER DEMO <<<\n")
    
    # 1. Initialize Kernel (already has a memory manager)
    kernel = Kernel()
    mem_manager = kernel.memory_manager
    
    # 2. Add processes with different memory requirements
    # Assuming frame size is 4096 (4KB)
    print("--- Adding Processes ---")
    p1 = Process(pid=1, name="Process A", arrival_time=0, burst_time=5, memory_required=8192)  # 2 Pages
    p2 = Process(pid=2, name="Process B", arrival_time=1, burst_time=3, memory_required=12000) # 3 Pages
    p3 = Process(pid=3, name="Process C", arrival_time=2, burst_time=1, memory_required=5000)  # 2 Pages
    
    kernel.add_process(p1)
    kernel.add_process(p2)
    kernel.add_process(p3)
    
    # 3. Check Memory Status
    status = mem_manager.get_status()
    print(f"\nMemory Status: {status}")
    
    # 4. Simulate Logical to Physical Address Translation
    print("\n--- Address Translation ---")
    # For Process B (PID 2)
    # Logical Address 5000 -> Should be in its 2nd page (Page 1)
    # Local Address 5000 // 4096 = 1, 5000 % 4096 = 904
    logical_addr = 5000
    physical_addr = mem_manager.translate(2, logical_addr)
    print(f"PID 2 | Logical Address {logical_addr} -> Physical Address {physical_addr}")
    
    # Test out of bounds (Page Fault)
    fault_addr = 20000
    print(f"PID 2 | Accessing {fault_addr} (Out of bounds)...")
    result = mem_manager.translate(2, fault_addr)
    if result is None:
        print("RESULT: Page Fault Recorded.")

    # 5. Deallocate and check status
    print("\n--- Deallocating Process B ---")
    mem_manager.deallocate(2)
    status_after = mem_manager.get_status()
    print(f"Memory Status: {status_after}")

    # 6. Re-allocate for a new process
    print("\n--- Adding Process D (Large Memory) ---")
    p4 = Process(pid=4, name="Process D", arrival_time=3, burst_time=4, memory_required=40000) # ~10 Pages
    kernel.add_process(p4)
    print(f"Memory Status: {mem_manager.get_status()}")

if __name__ == "__main__":
    run_memory_demo()
