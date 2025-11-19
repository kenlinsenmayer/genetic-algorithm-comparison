// One-Max Genetic Algorithm Implementation in Swift
// Author: Genetic Algorithm Performance Comparison Project
// Date: November 19, 2025

import Foundation

// GA Parameters
private let POPULATION_SIZE = 100
private let CHROMOSOME_LENGTH = 100
private let MAX_GENERATIONS = 500
private let CROSSOVER_RATE = 0.8
private let MUTATION_RATE = 0.01
private let TOURNAMENT_SIZE = 3

typealias Individual = [Bool]
typealias Population = [Individual]

struct OneMaxGA {
    
    /// Initialize a random population of binary individuals
    static func initializePopulation(size: Int, length: Int) -> Population {
        var population: Population = []
        for _ in 0..<size {
            let individual = (0..<length).map { _ in Bool.random() }
            population.append(individual)
        }
        return population
    }
    
    /// Evaluate fitness of an individual (count of trues)
    static func evaluateFitness(individual: Individual) -> Int {
        return individual.filter { $0 }.count
    }
    
    /// Tournament selection with pre-computed fitnesses
    static func tournamentSelection(population: Population, fitnesses: [Int], tournamentSize: Int) -> Individual {
        var best: Individual?
        var bestFitness = -1
        
        for _ in 0..<tournamentSize {
            let candidateIndex = Int.random(in: 0..<population.count)
            let candidate = population[candidateIndex]
            let fitness = fitnesses[candidateIndex]
            
            if fitness > bestFitness {
                bestFitness = fitness
                best = candidate
            }
        }
        
        return best!
    }
    
    /// Single-point crossover between two parents
    static func singlePointCrossover(parent1: Individual, parent2: Individual) -> (Individual, Individual) {
        if Double.random(in: 0...1) > CROSSOVER_RATE {
            return (parent1, parent2)
        }
        
        let crossoverPoint = Int.random(in: 1..<CHROMOSOME_LENGTH)
        
        let offspring1 = Array(parent1[0..<crossoverPoint] + parent2[crossoverPoint..<CHROMOSOME_LENGTH])
        let offspring2 = Array(parent2[0..<crossoverPoint] + parent1[crossoverPoint..<CHROMOSOME_LENGTH])
        
        return (offspring1, offspring2)
    }
    
    /// Mutate an individual with specified mutation rate
    static func mutate(individual: Individual, mutationRate: Double) -> Individual {
        return individual.map { gene in
            Double.random(in: 0...1) < mutationRate ? !gene : gene
        }
    }
    
    /// Main genetic algorithm function
    /// Returns (generations, bestFitness)
    static func runGA() -> (Int, Int) {
        var population = initializePopulation(size: POPULATION_SIZE, length: CHROMOSOME_LENGTH)
        
        for generation in 1...MAX_GENERATIONS {
            let fitnesses = population.map { evaluateFitness(individual: $0) }
            let maxFitness = fitnesses.max() ?? 0
            
            if maxFitness == CHROMOSOME_LENGTH {
                return (generation, maxFitness)
            }
            
            var newPopulation: Population = []
            
            while newPopulation.count < POPULATION_SIZE {
                let parent1 = tournamentSelection(population: population, fitnesses: fitnesses, tournamentSize: TOURNAMENT_SIZE)
                let parent2 = tournamentSelection(population: population, fitnesses: fitnesses, tournamentSize: TOURNAMENT_SIZE)
                
                let (offspring1, offspring2) = singlePointCrossover(parent1: parent1, parent2: parent2)
                
                let mutatedOffspring1 = mutate(individual: offspring1, mutationRate: MUTATION_RATE)
                let mutatedOffspring2 = mutate(individual: offspring2, mutationRate: MUTATION_RATE)
                
                newPopulation.append(mutatedOffspring1)
                if newPopulation.count < POPULATION_SIZE {
                    newPopulation.append(mutatedOffspring2)
                }
            }
            
            population = newPopulation
        }
        
        let finalFitnesses = population.map { evaluateFitness(individual: $0) }
        return (MAX_GENERATIONS, finalFitnesses.max() ?? 0)
    }
    
    /// Run a single GA instance and return execution time in milliseconds
    static func benchmarkSingleRun() -> Double {
        let startTime = CFAbsoluteTimeGetCurrent()
        let (_, _) = runGA()
        let endTime = CFAbsoluteTimeGetCurrent()
        
        return (endTime - startTime) * 1000.0 // Convert to milliseconds
    }
}