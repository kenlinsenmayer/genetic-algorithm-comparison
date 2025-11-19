// Test runner for F# GA implementation
// Runs 25 instances and outputs timing results

#load "OneMaxGA.fs"

/// Run the GA benchmark multiple times and collect results
let runTests (numRuns: int) : float array =
    printfn "F# One-Max GA Performance Test"
    printfn "Running %d tests..." numRuns
    
    let times = Array.zeroCreate numRuns
    
    for i in 0 .. numRuns - 1 do
        let elapsed = benchmarkSingleRun ()
        times.[i] <- elapsed
        printf "Run %d: %.3f ms\r" (i + 1) elapsed
        System.Console.Out.Flush()
    
    printfn "\nCompleted %d runs" numRuns
    
    // Output results in CSV format
    let timesStr = times |> Array.map string |> String.concat ","
    printfn "fsharp,%s" timesStr
    
    times

// Run if this is the main script
let main () =
    runTests 25 |> ignore

// Execute main if this file is run directly
if System.Environment.GetCommandLineArgs().[0].Contains("fsi") then
    main ()