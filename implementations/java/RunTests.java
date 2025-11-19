// Test runner for Java GA implementation
// Runs 25 instances and outputs timing results

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class RunTests {
    
    /**
     * Run the GA benchmark multiple times and collect results.
     */
    public static List<Double> runTests(int numRuns) {
        System.out.println("Java One-Max GA Performance Test");
        System.out.println("Running " + numRuns + " tests...");
        
        List<Double> times = new ArrayList<>();
        
        for (int i = 0; i < numRuns; i++) {
            double elapsed = OneMaxGA.benchmarkSingleRun();
            times.add(elapsed);
            System.out.print("Run " + (i + 1) + ": " + String.format("%.3f", elapsed) + " ms\r");
            System.out.flush();
        }
        
        System.out.println("\nCompleted " + numRuns + " runs");
        
        // Output results in CSV format
        String timesStr = times.stream()
                .map(String::valueOf)
                .collect(Collectors.joining(","));
        System.out.println("java," + timesStr);
        
        return times;
    }
    
    public static void main(String[] args) {
        runTests(25);
    }
}