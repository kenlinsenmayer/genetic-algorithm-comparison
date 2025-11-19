// Test runner for C# GA implementation
// Runs 25 instances and outputs timing results

using System;
using System.Collections.Generic;
using System.Linq;

public class RunTests
{
    /// <summary>
    /// Run the GA benchmark multiple times and collect results.
    /// </summary>
    public static List<double> RunTestBench(int numRuns = 25)
    {
        Console.WriteLine("C# One-Max GA Performance Test");
        Console.WriteLine($"Running {numRuns} tests...");

        var times = new List<double>();

        for (int i = 0; i < numRuns; i++)
        {
            double elapsed = OneMaxGA.BenchmarkSingleRun();
            times.Add(elapsed);
            Console.Write($"Run {i + 1}: {elapsed:F3} ms\r");
        }

        Console.WriteLine($"\nCompleted {numRuns} runs");

        // Output results in CSV format
        string timesStr = string.Join(",", times.Select(t => t.ToString()));
        Console.WriteLine($"csharp,{timesStr}");

        return times;
    }

    public static void Main(string[] args)
    {
        RunTestBench(25);
    }
}