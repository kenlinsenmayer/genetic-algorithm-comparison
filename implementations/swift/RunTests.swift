// Test runner for Swift GA implementation
// Runs 25 instances and outputs timing results

import Foundation

struct RunTests {
    /// Run the GA benchmark multiple times and collect results
    static func runTests(numRuns: Int = 25) -> [Double] {
        print("Swift One-Max GA Performance Test")
        print("Running \(numRuns) tests...")
        
        var times: [Double] = []
        
        for i in 0..<numRuns {
            let elapsed = OneMaxGA.benchmarkSingleRun()
            times.append(elapsed)
            print("Run \(i + 1): \(String(format: "%.3f", elapsed)) ms", terminator: "\r")
            fflush(stdout)
        }
        
        print("\nCompleted \(numRuns) runs")
        
        // Output results in CSV format
        let timesStr = times.map { String($0) }.joined(separator: ",")
        print("swift,\(timesStr)")
        
        return times
    }
}

// Main execution
@main
struct Main {
    static func main() {
        RunTests.runTests(numRuns: 25)
    }
}