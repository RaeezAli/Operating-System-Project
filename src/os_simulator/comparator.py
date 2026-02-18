import copy
import csv
import logging
from typing import List, Dict, Any
from os_simulator.kernel import Kernel, Scheduler
from os_simulator.process import Process
from os_simulator.metrics import MetricsCalculator

logger = logging.getLogger("Comparator")

class AlgorithmComparator:
    """
    Automates the comparison of different scheduling algorithms 
    by running them against the same set of processes.
    """

    def __init__(self):
        self.results: Dict[str, Dict[str, Any]] = {}

    def compare(
        self, 
        process_list: List[Process], 
        schedulers: List[Scheduler], 
        context_switch_time: int = 0
    ) -> Dict[str, Dict[str, Any]]:
        """
        Runs isolated simulations for each scheduler and collects metrics.
        
        Args:
            process_list: The baseline list of processes.
            schedulers: List of scheduler objects to benchmark.
            context_switch_time: Overhead to use in the kernel.
            
        Returns:
            A dictionary of results indexed by scheduler class name.
        """
        self.results = {}
        
        for scheduler in schedulers:
            name = type(scheduler).__name__
            logger.info(f"Running benchmark for: {name}")
            
            # 1. Isolate processes (deep copy to avoid state leakage)
            procs_copy = [copy.deepcopy(p) for p in process_list]
            
            # 2. Setup isolated Kernel and Calculator
            kernel = Kernel(context_switch_time=context_switch_time)
            kernel.set_scheduler(scheduler)
            
            for p in procs_copy:
                kernel.add_process(p)
                
            # 3. Execute
            timeline = kernel.run()
            
            # 4. Extract Metrics
            calculator = MetricsCalculator()
            metrics = calculator.calculate(procs_copy, timeline, kernel.system_clock)
            self.results[name] = metrics
            
        return self.results

    def print_comparison_table(self) -> None:
        """Prints the comparison results in a formatted table."""
        if not self.results:
            print("No comparison data available. Call compare() first.")
            return

        # Metrics to display
        metrics_keys = [
            "avg_waiting_time", 
            "avg_turnaround_time", 
            "avg_response_time", 
            "throughput", 
            "cpu_utilization", 
            "fairness_index"
        ]
        
        headers = ["Algorithm"] + [k.replace("_", " ").title() for k in metrics_keys]
        
        print("\n" + "="*120)
        print(f"{'SCHEDULING ALGORITHM COMPARISON':^120}")
        print("="*120)
        
        header_line = f"{headers[0]:<15}"
        for h in headers[1:]:
            header_line += f" | {h:<18}"
        print(header_line)
        print("-" * 120)
        
        for algo_name, metrics in self.results.items():
            row = f"{algo_name:<15}"
            for k in metrics_keys:
                val = metrics.get(k, "N/A")
                if isinstance(val, float):
                    row += f" | {val:<18}"
                else:
                    row += f" | {str(val):<18}"
            print(row)
            
        print("="*120 + "\n")

    def export_csv(self, filepath: str) -> None:
        """Exports the comparison results to a CSV file."""
        if not self.results:
            logger.error("No results to export.")
            return
            
        try:
            with open(filepath, 'w', newline='') as f:
                # Use metrics from first result as keys
                sample_metrics = next(iter(self.results.values()))
                fieldnames = ['Algorithm'] + list(sample_metrics.keys())
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for name, metrics in self.results.items():
                    row = {'Algorithm': name}
                    row.update(metrics)
                    writer.writerow(row)
                    
            logger.info(f"Comparison data exported to {filepath}")
        except Exception as e:
            logger.error(f"CSV Export failed: {e}")
