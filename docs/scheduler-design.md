# OS Scheduler Design

This component simulates how an Operating System manages process execution.

## 🔄 Round Robin (RR)

The current implementation uses a starvation-free pre-emptive algorithm.

- **Quantum**: The time slice allocated to each process.
- **Queue**: A list of tasks processed in order.
- **Visualization**: A Matplotlib-based Gantt chart showing the timeline of process execution.

## 🗺️ Planned Algorithms

- **First-Come, First-Served (FCFS)**: Non-preemptive scheduling.
- **Shortest Job First (SJF)**: Optimizing for average waiting time.
- **Priority Scheduling**: Handling critical tasks first.
