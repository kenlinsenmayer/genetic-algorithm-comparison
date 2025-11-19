# Test runner for Julia GA implementation
# Runs 25 instances and outputs timing results

include("onemax_ga.jl")

function run_tests(num_runs::Int = 25)
    println("Julia One-Max GA Performance Test")
    println("Running $num_runs tests...")
    
    times = Vector{Float64}(undef, num_runs)
    
    for i in 1:num_runs
        times[i] = benchmark_single_run()
        print("Run $i: $(times[i]) ms\r")
        flush(stdout)
    end
    
    println("\nCompleted $num_runs runs")
    
    # Output results in CSV format
    println("julia,$(join(times, ','))")
    
    return times
end

# Run if this is the main script
if abspath(PROGRAM_FILE) == @__FILE__
    run_tests()
end