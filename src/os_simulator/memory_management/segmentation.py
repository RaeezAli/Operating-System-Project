import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger("Segmentation-MMU")

class SegmentTableEntry:
    """Represents an entry in the segment table."""
    def __init__(self, base: int, limit: int):
        self.base = base
        self.limit = limit

    def __repr__(self):
        return f"[Base: {self.base}, Limit: {self.limit}]"

class SegmentationMemoryManager:
    """
    Implements a basic segmentation model for memory management.
    Each process has its own segment table.
    """
    def __init__(self, total_memory: int):
        self.total_memory = total_memory
        self.segment_tables: Dict[int, List[SegmentTableEntry]] = {}
        # Simple free space tracking (not a full allocator for this simulation)
        self.free_pointer = 0
        logger.info(f"Segmentation Memory Manager initialized with {total_memory} bytes.")

    def allocate(self, pid: int, segments: List[int]) -> bool:
        """
        Allocates memory segments for a process.
        segments: List of sizes for each segment (e.g., [code_size, data_size, stack_size])
        """
        total_requested = sum(segments)
        if self.free_pointer + total_requested > self.total_memory:
            logger.error(f"Allocation failed for PID {pid}: Not enough contiguous memory.")
            return False

        table = []
        current_base = self.free_pointer
        for size in segments:
            table.append(SegmentTableEntry(base=current_base, limit=size))
            current_base += size
        
        self.segment_tables[pid] = table
        self.free_pointer = current_base
        logger.info(f"Allocated {len(segments)} segments to PID {pid}. Table: {table}")
        return True

    def translate(self, pid: int, segment_id: int, offset: int) -> Optional[int]:
        """
        Translates (segment_id, offset) to a physical address.
        """
        if pid not in self.segment_tables:
            logger.error(f"Segmentation Fault: No segment table for PID {pid}.")
            return None
        
        table = self.segment_tables[pid]
        if segment_id < 0 or segment_id >= len(table):
            logger.error(f"Segmentation Fault: Invalid segment ID {segment_id} for PID {pid}.")
            return None
        
        entry = table[segment_id]
        if offset < 0 or offset >= entry.limit:
            logger.error(f"Segmentation Fault: Offset {offset} exceeds limit {entry.limit} for segment {segment_id}.")
            return None
        
        physical_address = entry.base + offset
        return physical_address

    def get_status(self, pid: int) -> Dict:
        """Returns the segment table for a specific process."""
        return {
            "pid": pid,
            "segments": self.segment_tables.get(pid, []),
            "total_memory": self.total_memory,
            "used_memory": self.free_pointer
        }

def run_segmentation_demo():
    """Internal demo for segmentation logic."""
    print(">>> SEGMENTATION MMU DEMO <<<\n")
    mmu = SegmentationMemoryManager(total_memory=65536) # 64KB

    # Process 1: Code (1000 bytes), Data (2000 bytes), Stack (500 bytes)
    print("1. Allocating segments for PID 1...")
    mmu.allocate(1, [1000, 2000, 500])

    # Successful translation
    # Segment 1 (Data), Offset 50
    print("\n2. Translating (Segment 1, Offset 50):")
    phys = mmu.translate(1, 1, 50)
    print(f"   Physical Address: {phys}")

    # Boundary Violation
    print("\n3. Testing Limit Violation (Segment 0, Offset 1001):")
    phys_fail = mmu.translate(1, 0, 1001)
    if phys_fail is None:
        print("   Result: Correctly caught limit violation.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_segmentation_demo()