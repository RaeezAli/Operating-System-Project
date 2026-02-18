from typing import List, Tuple, Dict, Any, Optional
from os_simulator.process import Process
from os_simulator.system_clock import SystemClock

class MetricsCalculator:
    """
    Computes performance indicators for the OS simulator based on 
    simulation execution data.
    """

    def __init__(self):
        self.results: Dict[str, Any] = {}

    def calculate(
        self, 
        process_list: List[Process], 
        execution_timeline: List[Tuple[Any, int, int]], 
        system_clock: SystemClock
    ) -> Dict[str, Any]:
        """
        Calculates all key metrics from the simulation results.
        
        Args:
            process_list: Final list of processes after simulation.
            execution_timeline: The sequence of execution segments.
            system_clock: The clock instance used during simulation.
            
        Returns:
            A dictionary containing various metrics.
        """
        if not process_list:
            return {}

        n = len(process_list)
        total_wt = sum(p.waiting_time for p in process_list)
        total_tat = sum(p.turnaround_time for p in process_list)
        
        # Calculate Response Times
        response_times = self._get_response_times(process_list, execution_timeline)
        avg_rt = sum(response_times.values()) / n if n > 0 else 0
        
        # Performance metrics
        total_time = system_clock.get_time()
        throughput = n / total_time if total_time > 0 else 0
        utilization = system_clock.get_cpu_utilization()
        
        # Fairness Index (Jain's Fairness Index on Waiting Times)
        fairness = self._calculate_fairness(process_list)

        self.results = {
            "avg_waiting_time": round(total_wt / n, 2),
            "avg_turnaround_time": round(total_tat / n, 2),
            "avg_response_time": round(avg_rt, 2),
            "throughput": round(throughput, 4),
            "cpu_utilization": utilization,
            "fairness_index": round(fairness, 4),
            "total_processes": n,
            "simulation_duration": total_time
        }
        
        return self.results

    def _get_response_times(self, process_list: List[Process], timeline: List[Tuple[Any, int, int]]) -> Dict[int, int]:
        """
        Helper to find first CPU access for each process to calculate Response Time.
        RT = First Start - Arrival
        """
        first_starts = {}
        for pid_or_msg, start, _ in timeline:
            if isinstance(pid_or_msg, int) and pid_or_msg not in first_starts:
                first_starts[pid_or_msg] = start
        
        response_times = {}
        for p in process_list:
            first_start = first_starts.get(p.pid, p.arrival_time) # Fallback if not scheduled
            response_times[p.pid] = first_start - p.arrival_time
            
        return response_times

    def _calculate_fairness(self, process_list: List[Process]) -> float:
        """
        Calculates Jain's Fairness Index for process waiting times.
        JFI = (sum(xi))^2 / (n * sum(xi^2))
        """
        x = [p.waiting_time for p in process_list]
        n = len(x)
        if n == 0: return 0.0
        
        sum_x = sum(x)
        sum_x_sq = sum(val**2 for val in x)
        
        if sum_x_sq == 0: return 1.0 # Perfectly fair if everyone waited 0
        
        return (sum_x**2) / (n * sum_x_sq)

    def pretty_print(self) -> None:
        """Prints a formatted summary of the calculated metrics."""
        if not self.results:
            print("No metrics calculated yet. Call calculate() first.")
            return

        print("\n" + "="*40)
        print(" OS SIMULATION PERFORMANCE SUMMARY")
        print("="*40)
        print(f"{'Metric':<25} | {'Value':<10}")
        print("-" * 40)
        print(f"{'Total Processes':<25} | {self.results['total_processes']}")
        print(f"{'Simulation Duration':<25} | {self.results['simulation_duration']} units")
        print(f"{'CPU Utilization':<25} | {self.results['cpu_utilization']}%")
        print(f"{'Throughput':<25} | {self.results['throughput']} proc/unit")
        print("-" * 40)
        print(f"{'Avg Waiting Time':<25} | {self.results['avg_waiting_time']} units")
        print(f"{'Avg Turnaround Time':<25} | {self.results['avg_turnaround_time']} units")
        print(f"{'Avg Response Time':<25} | {self.results['avg_response_time']} units")
        print("-" * 40)
        print(f"{'Fairness Index (Jain)':<25} | {self.results['fairness_index']}")
        print("="*40 + "\n")
