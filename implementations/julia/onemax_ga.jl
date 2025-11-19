# One-Max Genetic Algorithm Implementation in Julia
# Author: Genetic Algorithm Performance Comparison Project
# Date: November 19, 2025

using Random

# Individual representation as a vector of booleans
const Individual = Vector{Bool}

# GA Parameters
const POPULATION_SIZE = 100
const CHROMOSOME_LENGTH = 100
const MAX_GENERATIONS = 500
const CROSSOVER_RATE = 0.8
const MUTATION_RATE = 0.01
const TOURNAMENT_SIZE = 3

"""
Initialize a random population of binary individuals.
"""
function initialize_population(size::Int, length::Int)::Vector{Individual}
    population = Vector{Individual}(undef, size)
    for i in 1:size
        population[i] = rand(Bool, length)
    end
    return population
end

"""
Evaluate fitness of an individual (count of 1s).
"""
function evaluate_fitness(individual::Individual)::Int
    return sum(individual)
end

"""
Tournament selection with specified tournament size.
"""
function tournament_selection(population::Vector{Individual}, fitnesses::Vector{Int}, tournament_size::Int)::Individual
    tournament_indices = rand(1:length(population), tournament_size)
    best_idx = tournament_indices[1]
    best_fitness = fitnesses[best_idx]
    
    for i in 2:tournament_size
        idx = tournament_indices[i]
        if fitnesses[idx] > best_fitness
            best_fitness = fitnesses[idx]
            best_idx = idx
        end
    end
    
    return copy(population[best_idx])
end

"""
Single-point crossover between two parents.
"""
function single_point_crossover(parent1::Individual, parent2::Individual)::Tuple{Individual, Individual}
    if rand() > CROSSOVER_RATE
        return copy(parent1), copy(parent2)
    end
    
    crossover_point = rand(1:length(parent1)-1)
    
    offspring1 = vcat(parent1[1:crossover_point], parent2[crossover_point+1:end])
    offspring2 = vcat(parent2[1:crossover_point], parent1[crossover_point+1:end])
    
    return offspring1, offspring2
end

"""
Mutate an individual with specified mutation rate.
"""
function mutate!(individual::Individual, mutation_rate::Float64)::Nothing
    for i in 1:length(individual)
        if rand() < mutation_rate
            individual[i] = !individual[i]
        end
    end
    return nothing
end

"""
Main genetic algorithm function.
Returns the number of generations and best fitness achieved.
"""
function run_ga()::Tuple{Int, Int}
    # Initialize population
    population = initialize_population(POPULATION_SIZE, CHROMOSOME_LENGTH)
    
    for generation in 1:MAX_GENERATIONS
        # Evaluate fitness
        fitnesses = [evaluate_fitness(ind) for ind in population]
        
        # Check for optimal solution
        max_fitness = maximum(fitnesses)
        if max_fitness == CHROMOSOME_LENGTH
            return generation, max_fitness
        end
        
        # Create new population
        new_population = Vector{Individual}(undef, POPULATION_SIZE)
        
        for i in 1:2:POPULATION_SIZE
            # Selection
            parent1 = tournament_selection(population, fitnesses, TOURNAMENT_SIZE)
            parent2 = tournament_selection(population, fitnesses, TOURNAMENT_SIZE)
            
            # Crossover
            offspring1, offspring2 = single_point_crossover(parent1, parent2)
            
            # Mutation
            mutate!(offspring1, MUTATION_RATE)
            mutate!(offspring2, MUTATION_RATE)
            
            # Add to new population
            new_population[i] = offspring1
            if i + 1 <= POPULATION_SIZE
                new_population[i + 1] = offspring2
            end
        end
        
        population = new_population
    end
    
    # Final evaluation
    fitnesses = [evaluate_fitness(ind) for ind in population]
    return MAX_GENERATIONS, maximum(fitnesses)
end

"""
Run a single GA instance and return execution time in milliseconds.
"""
function benchmark_single_run()::Float64
    start_time = time_ns()
    generations, best_fitness = run_ga()
    end_time = time_ns()
    
    elapsed_ms = (end_time - start_time) / 1_000_000
    return elapsed_ms
end