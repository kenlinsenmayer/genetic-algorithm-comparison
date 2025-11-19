open System

// GA Parameters
let POPULATION_SIZE = 100
let CHROMOSOME_LENGTH = 100
let MAX_GENERATIONS = 500
let CROSSOVER_RATE = 0.8
let MUTATION_RATE = 0.01
let TOURNAMENT_SIZE = 3

type Individual = bool array
type Population = Individual array

let random = Random()

let initializePopulation (size: int) (length: int) : Population =
    Array.init size (fun _ -> Array.init length (fun _ -> random.NextDouble() < 0.5))

let evaluateFitness (individual: Individual) : int =
    individual |> Array.sumBy (fun bit -> if bit then 1 else 0)

let tournamentSelection (population: Population) (fitnesses: int array) (tournamentSize: int) : Individual =
    let tournamentIndices = Array.init tournamentSize (fun _ -> random.Next(population.Length))
    let bestIdx = tournamentIndices |> Array.maxBy (fun idx -> fitnesses.[idx])
    Array.copy population.[bestIdx]

let singlePointCrossover (parent1: Individual) (parent2: Individual) : Individual * Individual =
    if random.NextDouble() > CROSSOVER_RATE then
        (Array.copy parent1, Array.copy parent2)
    else
        let crossoverPoint = random.Next(1, parent1.Length)
        let offspring1 = Array.append parent1.[..crossoverPoint-1] parent2.[crossoverPoint..]
        let offspring2 = Array.append parent2.[..crossoverPoint-1] parent1.[crossoverPoint..]
        (offspring1, offspring2)

let mutate (individual: Individual) (mutationRate: float) : Individual =
    individual |> Array.map (fun bit -> if random.NextDouble() < mutationRate then not bit else bit)

let runGA () : int * int =
    let rec evolve (population: Population) (generation: int) : int * int =
        let fitnesses = population |> Array.map evaluateFitness
        let maxFitness = Array.max fitnesses
        if maxFitness = CHROMOSOME_LENGTH then
            (generation, maxFitness)
        elif generation >= MAX_GENERATIONS then
            (MAX_GENERATIONS, maxFitness)
        else
            let newPopulation = Array.zeroCreate POPULATION_SIZE
            let mutable i = 0
            while i < POPULATION_SIZE do
                let parent1 = tournamentSelection population fitnesses TOURNAMENT_SIZE
                let parent2 = tournamentSelection population fitnesses TOURNAMENT_SIZE
                let offspring1, offspring2 = singlePointCrossover parent1 parent2
                let mutatedOffspring1 = mutate offspring1 MUTATION_RATE
                let mutatedOffspring2 = mutate offspring2 MUTATION_RATE
                newPopulation.[i] <- mutatedOffspring1
                if i + 1 < POPULATION_SIZE then
                    newPopulation.[i + 1] <- mutatedOffspring2
                i <- i + 2
            evolve newPopulation (generation + 1)
    
    let initialPopulation = initializePopulation POPULATION_SIZE CHROMOSOME_LENGTH
    evolve initialPopulation 1

let benchmarkSingleRun () : float =
    let stopwatch = System.Diagnostics.Stopwatch.StartNew()
    let generations, bestFitness = runGA ()
    stopwatch.Stop()
    stopwatch.Elapsed.TotalMilliseconds

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
    let timesStr = times |> Array.map string |> String.concat ","
    printfn "fsharp,%s" timesStr
    times

[<EntryPoint>]
let main argv =
    runTests 25 |> ignore
    0