import matplotlib.pyplot as plt
from typing import List, Tuple
from os_simulator.scheduling.models import GanttEntry

class SchedulerVisualizer:
    """
    Handles all visualization for scheduling algorithms.
    Decouples logic from UI (SOLID: Single Responsibility).
    """

    @staticmethod
    def plot_gantt(gantt_chart: List[GanttEntry], title: str = "Gantt Chart"):
        if not gantt_chart:
            print("[Visualizer] No execution data to plot.")
            return

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel("Processes")

        # Extract unique PIDs for Y-axis
        pids = list(dict.fromkeys(entry.pid for entry in gantt_chart))
        ax.set_yticks(range(len(pids)))
        ax.set_yticklabels(pids)

        # Plot bars
        for entry in gantt_chart:
            idx = pids.index(entry.pid)
            duration = entry.end_time - entry.start_time
            ax.broken_barh([(entry.start_time, duration)], (idx - 0.4, 0.8), facecolors=('tab:green'))

        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def print_metrics(processes, avg_wait: float, avg_tat: float):
        """Prints formatted metrics to console."""
        print("-" * 60)
        print(f"{'PID':<10} | {'Burst':<10} | {'Wait':<10} | {'Turnaround':<10}")
        print("-" * 60)
        for p in processes:
            print(f"{p.pid:<10} | {p.burst_time:<10} | {p.waiting_time:<10} | {p.turnaround_time:<10}")
        print("-" * 60)
        print(f"Average Waiting Time:    {avg_wait:.2f}")
        print(f"Average Turnaround Time: {avg_tat:.2f}")
        print("-" * 60)
