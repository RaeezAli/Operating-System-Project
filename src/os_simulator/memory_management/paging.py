import logging
import math
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("Memory-Manager")

class PagingMemoryManager:
    """
    Simulates a Paging-based Memory Management Unit (MMU).
    
    Manages physical memory frames, process page tables, and performs 
    logical-to-physical address translation.
    """

    def __init__(self, total_memory: int = 262144, frame_size: int = 4096):
        """
        Initializes the memory manager.
        
        Args:
            total_memory: Total physical memory in bytes (default 256KB).
            frame_size: Size of each frame in bytes (default 4KB).
        """
        self.frame_size = frame_size
        self.total_frames = total_memory // frame_size
        
        # Physical memory frames: None means free, otherwise stores process PID
        self.physical_frames: List[Optional[int]] = [None] * self.total_frames
        
        # Page tables: {pid: [frame_index_1, frame_index_2, ...]}
        self.page_tables: Dict[int, List[int]] = {}
        
        self.page_faults = 0
        logger.info(f"Paging Memory Manager initialized. Total frames: {self.total_frames}, Frame size: {self.frame_size}B")

    def allocate(self, pid: int, memory_required: int) -> bool:
        """
        Allocates memory for a process by mapping its logical pages to physical frames.
        
        Args:
            pid: Process ID.
            memory_required: Memory needed in bytes.
            
        Returns:
            True if allocation was successful, False if not enough free frames.
        """
        num_pages = math.ceil(memory_required / self.frame_size)
        
        # Check if enough free frames exist
        free_frames = [i for i, frame in enumerate(self.physical_frames) if frame is None]
        
        if len(free_frames) < num_pages:
            logger.warning(f"Memory allocation failed for PID {pid}. Needed {num_pages} frames, actually have {len(free_frames)}.")
            return False

        # Allocate frames and update page table
        allocated_frames = free_frames[:num_pages]
        for frame_idx in allocated_frames:
            self.physical_frames[frame_idx] = pid
            
        self.page_tables[pid] = allocated_frames
        logger.info(f"Allocated {num_pages} pages ({memory_required} bytes) to PID {pid}. Frames: {allocated_frames}")
        return True

    def deallocate(self, pid: int) -> None:
        """
        Frees all memory frames associated with a process.
        
        Args:
            pid: Process ID.
        """
        if pid not in self.page_tables:
            logger.warning(f"Attempted to deallocate memory for PID {pid}, but no page table found.")
            return

        frames_to_free = self.page_tables[pid]
        for frame_idx in frames_to_free:
            self.physical_frames[frame_idx] = None
            
        del self.page_tables[pid]
        logger.info(f"Deallocated memory for PID {pid}. Freed frames: {frames_to_free}")

    def translate(self, pid: int, logical_address: int) -> Optional[int]:
        """
        Translates a logical address to a physical address using the process's page table.
        
        Address Translation:
        1. Logical Page Number = logical_address // frame_size
        2. Offset = logical_address % frame_size
        3. Physical Address = (PageTable[PageNumber] * frame_size) + Offset
        
        Args:
            pid: Process ID.
            logical_address: The address within the process's logical space.
            
        Returns:
            The translated physical address, or None if a page fault occurs.
        """
        if pid not in self.page_tables:
            logger.error(f"Page fault: PID {pid} has no memory allocated.")
            self.page_faults += 1
            return None

        page_number = logical_address // self.frame_size
        offset = logical_address % self.frame_size
        
        process_page_table = self.page_tables[pid]
        
        if page_number >= len(process_page_table):
            logger.error(f"Page fault: PID {pid} requested invalid logical address {logical_address} (Page {page_number}).")
            self.page_faults += 1
            return None

        frame_number = process_page_table[page_number]
        physical_address = (frame_number * self.frame_size) + offset
        
        logger.debug(f"Translated: PID {pid} | Logical {logical_address} -> Physical {physical_address}")
        return physical_address

    def get_status(self) -> Dict[str, Any]:
        """Returns statistics on memory consumption and page faults."""
        used_frames = sum(1 for f in self.physical_frames if f is not None)
        return {
            "total_frames": self.total_frames,
            "used_frames": used_frames,
            "free_frames": self.total_frames - used_frames,
            "utilization": (used_frames / self.total_frames) * 100,
            "page_faults": self.page_faults
        }

    def reset(self) -> None:
        """Resets the memory manager state."""
        self.physical_frames = [None] * self.total_frames
        self.page_tables = {}
        self.page_faults = 0
        logger.info("Memory Manager state reset.")