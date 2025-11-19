#!/usr/bin/env python3
# Test runner for Python GA implementation
# Runs 25 instances and outputs timing results

from onemax_ga import benchmark_single_run
import sys


def run_tests(num_runs: int = 25) -> list:
    """Run the GA benchmark multiple times and collect results."""
    print(f"Python One-Max GA Performance Test")
    print(f"Running {num_runs} tests...")
    
    times = []
    
    for i in range(num_runs):
        elapsed = benchmark_single_run()
        times.append(elapsed)
        print(f"Run {i+1}: {elapsed:.3f} ms", end='\r')
        sys.stdout.flush()
    
    print(f"\nCompleted {num_runs} runs")
    
    # Output results in CSV format
    print(f"python,{','.join(map(str, times))}")
    
    return times


if __name__ == "__main__":
    run_tests()