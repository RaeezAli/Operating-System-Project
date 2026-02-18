# Jarvis OS Simulator 🤖 (Terminal-Based)

A **terminal-based Operating System Simulation Framework** integrated with a **Voice-Controlled AI Assistant (Jarvis)**.

This project is designed for academic learning and system-level experimentation. It simulates core Operating System concepts such as scheduling, memory management, deadlock handling, and synchronization — all executable from the terminal using structured commands or voice input.

> This is a CLI (Command-Line Interface) / Terminal-Based project.  
> There is no GUI — all simulations and outputs are displayed in the terminal.

---

# 🚀 Key Features

## 💻 OS Simulation Subsystem (Terminal-Based)

### 🧠 CPU Scheduling

- Algorithms:
  - FCFS
  - Round Robin (Configurable Quantum)
  - Priority Scheduling
  - (Optional) SJF
- Features:
  - Arrival-time aware simulation
  - Context switching support
  - Gantt-style terminal timeline output
  - Metrics:
    - Turnaround Time (TAT)
    - Waiting Time (WT)
    - Response Time (RT)
    - Throughput
    - CPU Utilization
    - Jain’s Fairness Index
- Comparator Mode:
  - Run multiple algorithms on the same process set
  - Terminal-based comparison output

### 🧮 Memory Management

- **Paging**
  - Logical → Physical address translation
  - Frame allocation
  - Page fault tracking
- **Page Replacement Algorithms**
  - FIFO
  - LRU
  - Optimal
- **Segmentation**
  - Segment table per process
  - Base & Limit protection
  - Logical address validation

All memory simulations are terminal-driven and output detailed step-by-step traces.

### 🔒 Deadlock Management

- **Avoidance**
  - Banker’s Algorithm
  - Safe state detection
  - Safe sequence generation
- **Detection**
  - Wait-For Graph (WFG)
  - Cycle detection using DFS

### 🔄 Process Synchronization

Thread-safe implementations of classic OS problems:

- Producer–Consumer (Bounded Buffer)
- Dining Philosophers

Built using counting semaphores and threading.

---

## 🎙️ Jarvis AI Assistant (Terminal + Voice)

Jarvis acts as a smart command router that bridges:

User (Voice/Text) → Parser → OS Simulator / Automation Layer

### Capabilities

- Voice or text-based command execution
- Add and schedule processes via speech
- Run memory simulations via speech
- Check deadlock states
- Open system applications
- Perform web searches
- Play YouTube content
- Provide system information (IP, battery, date, time)

---

# 🛠️ Installation

## 1️⃣ Prerequisites

- Python 3.10+
- Virtual environment (recommended)
- Microphone (for voice mode)

## 2️⃣ Setup

```powershell
# Clone the repository
git clone https://github.com/RaeezAli/Operating-System-Project.git
cd Operating-System-Project

# Install dependencies
pip install -r requirements.txt
```
