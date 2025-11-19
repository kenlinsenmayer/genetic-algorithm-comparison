// One-Max Genetic Algorithm Implementation in F#
// Author: Genetic Algorithm Performance Comparison Project
// Date: November 19, 2025

module OneMaxGA

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

/// Initialize a random population of binary individuals
let initializePopulation (size: int) (length: int) : Population =
    Array.init size (fun _ -> Array.init length (fun _ -> random.NextDouble() < 0.5))

/// Evaluate fitness of an individual (count of 1s)
let evaluateFitness (individual: Individual) : int =
    individual |> Array.sumBy (fun bit -> if bit then 1 else 0)

/// Tournament selection with specified tournament size
let tournamentSelection (population: Population) (fitnesses: int array) (tournamentSize: int) : Individual =
    let tournamentIndices = Array.init tournamentSize (fun _ -> random.Next(population.Length))
    let bestIdx = 
        tournamentIndices
        |> Array.maxBy (fun idx -> fitnesses.[idx])
    Array.copy population.[bestIdx]

/// Single-point crossover between two parents
let singlePointCrossover (parent1: Individual) (parent2: Individual) : Individual * Individual =
    if random.NextDouble() > CROSSOVER_RATE then
        (Array.copy parent1, Array.copy parent2)
    else
        let crossoverPoint = random.Next(1, parent1.Length)
        let offspring1 = Array.append parent1.[..crossoverPoint-1] parent2.[crossoverPoint..]
        let offspring2 = Array.append parent2.[..crossoverPoint-1] parent1.[crossoverPoint..]
        (offspring1, offspring2)

/// Mutate an individual with specified mutation rate
let mutate (individual: Individual) (mutationRate: float) : Individual =
    individual
    |> Array.map (fun bit -> 
        if random.NextDouble() < mutationRate then not bit else bit)

/// Main genetic algorithm function
let runGA () : int * int =
    let rec evolve (population: Population) (generation: int) : int * int =
        // Evaluate fitness
        let fitnesses = population |> Array.map evaluateFitness
        
        // Check for optimal solution
        let maxFitness = Array.max fitnesses
        if maxFitness = CHROMOSOME_LENGTH then
            (generation, maxFitness)
        elif generation >= MAX_GENERATIONS then
            (MAX_GENERATIONS, maxFitness)
        else
            // Create new population
            let newPopulation = Array.zeroCreate POPULATION_SIZE
            let mutable i = 0
            
            while i < POPULATION_SIZE do
                // Selection
                let parent1 = tournamentSelection population fitnesses TOURNAMENT_SIZE
                let parent2 = tournamentSelection population fitnesses TOURNAMENT_SIZE
                
                // Crossover
                let offspring1, offspring2 = singlePointCrossover parent1 parent2
                
                // Mutation
                let mutatedOffspring1 = mutate offspring1 MUTATION_RATE
                let mutatedOffspring2 = mutate offspring2 MUTATION_RATE
                
                // Add to new population
                newPopulation.[i] <- mutatedOffspring1
                if i + 1 < POPULATION_SIZE then
                    newPopulation.[i + 1] <- mutatedOffspring2
                
                i <- i + 2
            
            evolve newPopulation (generation + 1)
    
    // Initialize population and start evolution
    let initialPopulation = initializePopulation POPULATION_SIZE CHROMOSOME_LENGTH
    evolve initialPopulation 1

/// Run a single GA instance and return execution time in milliseconds
let benchmarkSingleRun () : float =
    let stopwatch = System.Diagnostics.Stopwatch.StartNew()
    let generations, bestFitness = runGA ()
    stopwatch.Stop()
    stopwatch.Elapsed.TotalMilliseconds