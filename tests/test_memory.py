import unittest
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from os_simulator.memory_management.paging import PagingMemoryManager
from os_simulator.memory_management.page_replacement import fifo_replacement, lru_replacement

class TestPaging(unittest.TestCase):
    def setUp(self):
        # 1KB memory, 256B frame size -> 4 frames
        self.mm = PagingMemoryManager(total_memory=1024, frame_size=256)

    def test_allocation_success(self):
        """Tests successful memory allocation for multiple processes."""
        # Process 1: 400 bytes -> 2 pages
        self.assertTrue(self.mm.allocate(1, 400))
        status = self.mm.get_status()
        self.assertEqual(status["used_frames"], 2)
        self.assertEqual(status["free_frames"], 2)
        self.assertIn(1, self.mm.page_tables)
        self.assertEqual(len(self.mm.page_tables[1]), 2)

    def test_allocation_failure(self):
        """Tests failure when requesting more memory than available."""
        # Process 1: 1200 bytes -> 5 pages (Total frames = 4)
        self.assertFalse(self.mm.allocate(1, 1200))
        status = self.mm.get_status()
        self.assertEqual(status["used_frames"], 0)

    def test_deallocation(self):
        """Tests that deallocating memory frees up frames."""
        self.mm.allocate(1, 400) # 2 frames
        self.mm.deallocate(1)
        status = self.mm.get_status()
        self.assertEqual(status["used_frames"], 0)
        self.assertNotIn(1, self.mm.page_tables)

    def test_address_translation(self):
        """Tests logical-to-physical address translation."""
        # Process 1: 400 bytes -> 2 pages
        self.mm.allocate(1, 400)
        
        # Frame size is 256. 
        # Logical address 300: Page 1 (300 // 256), Offset 44 (300 % 256)
        page_table = self.mm.page_tables[1]
        page_1_frame = page_table[1]
        expected_physical = (page_1_frame * 256) + 44
        
        translated = self.mm.translate(1, 300)
        self.assertEqual(translated, expected_physical)

    def test_page_fault_on_invalid_translation(self):
        """Tests translation failure for unallocated process."""
        self.assertIsNone(self.mm.translate(99, 100))
        self.assertEqual(self.mm.get_status()["page_faults"], 1)

class TestPageReplacement(unittest.TestCase):
    def test_fifo_logic(self):
        """Tests FIFO page replacement with a standard reference string."""
        # String: [1, 2, 3, 1, 4, 5] with 3 frames
        # 1: Fault [1]
        # 2: Fault [1, 2]
        # 3: Fault [1, 2, 3]
        # 1: Hit   [1, 2, 3]
        # 4: Fault [2, 3, 4] (1 was earliest)
        # 5: Fault [3, 4, 5] (2 was earliest)
        # Total Faults: 5, Hits: 1
        ref = [1, 2, 3, 1, 4, 5]
        result = fifo_replacement(ref, 3)
        self.assertEqual(result["page_faults"], 5)
        self.assertEqual(result["page_hits"], 1)

    def test_lru_logic(self):
        """Tests LRU page replacement logic."""
        # String: [1, 2, 3, 1, 4, 5] with 3 frames
        # 1: Fault [1]
        # 2: Fault [1, 2]
        # 3: Fault [1, 2, 3]
        # 1: Hit   [2, 3, 1] (1 moved to MRU)
        # 4: Fault [3, 1, 4] (2 was LRU)
        # 5: Fault [1, 4, 5] (3 was LRU)
        # Total Faults: 5, Hits: 1
        ref = [1, 2, 3, 1, 4, 5]
        result = lru_replacement(ref, 3)
        self.assertEqual(result["page_faults"], 5)
        self.assertEqual(result["page_hits"], 1)

if __name__ == '__main__':
    unittest.main()