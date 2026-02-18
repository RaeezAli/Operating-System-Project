from os_simulator.process import Process, ProcessState

def run_example():
    # 1. Create a simulated process
    # PID 101, Name 'WebServer', Arrival time 0, Burst time 5, Priority 1, Memory 1024
    p = Process(pid=101, name="WebServer", arrival_time=0, burst_time=5, priority=1, memory_required=1024)
    
    print(f"--- Initial State ---")
    print(p)
    
    # 2. Transition to READY
    p.update_state(ProcessState.READY)
    print(f"\n--- State Transition ---")
    print(p)
    
    # 3. Simulate execution loop
    p.update_state(ProcessState.RUNNING)
    print(f"\n--- Starting Execution ---")
    
    current_time = 0
    while not p.is_completed():
        current_time += 1
        p.execute_one_unit()
        print(f"Time {current_time}: {p}")
        
    # 4. Calculate metrics upon completion
    p.calculate_metrics(current_time)
    
    print(f"\n--- Final Metrics ---")
    print(f"Name:            {p.name}")
    print(f"PID:             {p.pid}")
    print(f"Arrival Time:    {p.arrival_time}")
    print(f"Burst Time:      {p.burst_time}")
    print(f"Completion Time: {p.completion_time}")
    print(f"Turnaround Time: {p.turnaround_time}")
    print(f"Waiting Time:    {p.waiting_time}")
    print(f"Final State:     {p.state.name}")

if __name__ == "__main__":
    run_example()
