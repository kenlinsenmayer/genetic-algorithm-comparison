// Test runner for TypeScript GA implementation
// Runs 25 instances and outputs timing results
import { benchmarkSingleRun } from './onemax_ga.js';
/**
 * Run the GA benchmark multiple times and collect results.
 */
function runTests(numRuns = 25) {
    console.log("TypeScript One-Max GA Performance Test");
    console.log(`Running ${numRuns} tests...`);
    const times = [];
    for (let i = 0; i < numRuns; i++) {
        const elapsed = benchmarkSingleRun();
        times.push(elapsed);
        process.stdout.write(`Run ${i + 1}: ${elapsed.toFixed(3)} ms\r`);
    }
    console.log(`\nCompleted ${numRuns} runs`);
    // Output results in CSV format
    const timesStr = times.join(',');
    console.log(`typescript,${timesStr}`);
    return times;
}
// Run automatically
runTests(25);
export { runTests };
