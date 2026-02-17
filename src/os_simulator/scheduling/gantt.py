import matplotlib.pyplot as plt

def plot_gantt_chart(processes, gantt_chart, title="Scheduling Gantt Chart"):
    """Visualizes the scheduling sequence using a Gantt chart."""
    if not processes or not gantt_chart:
        print("[WARNING] No data to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")
    
    # Process names to indices for plotting
    unique_processes = list(dict.fromkeys(processes))
    ax.set_yticks(range(len(unique_processes)))
    ax.set_yticklabels(unique_processes)

    for p, start, end in gantt_chart:
        idx = unique_processes.index(p)
        ax.broken_barh([(start, end - start)], (idx - 0.4, 0.8), facecolors=('tab:blue'))

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
