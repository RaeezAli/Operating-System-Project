# OS Simulator Examples

This directory contains various demonstration scripts that showcase the features of the Operating System Simulator.

## How to Run Demos

All demos should be executed from the **project root directory** to ensure imports resolve correctly.

### Basic Execution

Use the following command format:

```powershell
python examples/demo_name.py
```

## Available Demos

### 1. Kernel & Scheduling

- `kernel_demo.py`: Showcases FCFS, Priority, and Round Robin scheduling algorithms.
- `context_switch_demo.py`: Demonstrates the impact of context switching overhead on simulation time.

### 2. Memory Management

- `memory_demo.py`: Demonstrates paging, logical-to-physical address translation, and page fault handling.
- `page_replacement_demo.py`: Compares FIFO, LRU, and Optimal page replacement algorithms.

### 3. Deadlock Handling

- `deadlock_demo.py`: Showcases Deadlock Avoidance using the Banker's Algorithm.
- `deadlock_detection_demo.py`: Demonstrates Deadlock Detection using Wait-For Graphs.

### 4. Synchronization & IPC

- `semaphore_demo.py`: Demonstrates thread synchronization using a Counting Semaphore.

### 5. System Components

- `clock_demo.py`: Showcases the system clock, CPU utilization tracking, and busy/idle time reporting.
- `metrics_demo.py`: Demonstrates the calculation of performance metrics (TAT, WT, RT, Throughput).
- `config_demo.py`: Shows how to use the YAML-based Configuration Loader.

### 6. AI Integration

- `assistant_integration_demo.py`: Showcases interaction with the Jarvis AI Assistant.

## Requirements

Ensure you have the required dependencies installed:

```powershell
pip install -r requirements.txt
```
