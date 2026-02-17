def round_robin_scheduling(processes, burst_time, quantum):
    """
    Executes the Round Robin scheduling algorithm.
    Returns a list of (process_name, start_time, end_time) representing the execution sequence.
    """
    n = len(processes)
    remaining_burst = burst_time[:]
    waiting_time = [0] * n
    turnaround_time = [0] * n
    t = 0
    gantt_chart = []

    while True:
        done = True
        for i in range(n):
            if remaining_burst[i] > 0:
                done = False
                exec_time = min(quantum, remaining_burst[i])
                gantt_chart.append((processes[i], t, t + exec_time))
                t += exec_time
                remaining_burst[i] -= exec_time
                for j in range(n):
                    if j != i and remaining_burst[j] > 0:
                        waiting_time[j] += exec_time
        if done:
            break

    for i in range(n):
        turnaround_time[i] = waiting_time[i] + burst_time[i]

    # Return results for printing/visualization
    return gantt_chart, waiting_time, turnaround_time
