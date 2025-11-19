# One-Max Genetic Algorithm Implementation in Python
# Author: Genetic Algorithm Performance Comparison Project
# Date: November 19, 2025

import random
import time
from typing import List, Tuple

# GA Parameters
POPULATION_SIZE = 100
CHROMOSOME_LENGTH = 100
MAX_GENERATIONS = 500
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.01
TOURNAMENT_SIZE = 3

Individual = List[bool]
Population = List[Individual]


def initialize_population(size: int, length: int) -> Population:
    """Initialize a random population of binary individuals."""
    population = []
    for _ in range(size):
        individual = [random.choice([True, False]) for _ in range(length)]
        population.append(individual)
    return population


def evaluate_fitness(individual: Individual) -> int:
    """Evaluate fitness of an individual (count of 1s)."""
    return sum(individual)


def tournament_selection(population: Population, fitnesses: List[int], tournament_size: int) -> Individual:
    """Tournament selection with specified tournament size."""
    tournament_indices = random.choices(range(len(population)), k=tournament_size)
    best_idx = tournament_indices[0]
    best_fitness = fitnesses[best_idx]
    
    for idx in tournament_indices[1:]:
        if fitnesses[idx] > best_fitness:
            best_fitness = fitnesses[idx]
            best_idx = idx
    
    return population[best_idx].copy()


def single_point_crossover(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
    """Single-point crossover between two parents."""
    if random.random() > CROSSOVER_RATE:
        return parent1.copy(), parent2.copy()
    
    crossover_point = random.randint(1, len(parent1) - 1)
    
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    
    return offspring1, offspring2


def mutate(individual: Individual, mutation_rate: float) -> Individual:
    """Mutate an individual with specified mutation rate."""
    mutated = individual.copy()
    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            mutated[i] = not mutated[i]
    return mutated


def run_ga() -> Tuple[int, int]:
    """
    Main genetic algorithm function.
    Returns the number of generations and best fitness achieved.
    """
    # Initialize population
    population = initialize_population(POPULATION_SIZE, CHROMOSOME_LENGTH)
    
    for generation in range(1, MAX_GENERATIONS + 1):
        # Evaluate fitness
        fitnesses = [evaluate_fitness(individual) for individual in population]
        
        # Check for optimal solution
        max_fitness = max(fitnesses)
        if max_fitness == CHROMOSOME_LENGTH:
            return generation, max_fitness
        
        # Create new population
        new_population = []
        
        for i in range(0, POPULATION_SIZE, 2):
            # Selection
            parent1 = tournament_selection(population, fitnesses, TOURNAMENT_SIZE)
            parent2 = tournament_selection(population, fitnesses, TOURNAMENT_SIZE)
            
            # Crossover
            offspring1, offspring2 = single_point_crossover(parent1, parent2)
            
            # Mutation
            offspring1 = mutate(offspring1, MUTATION_RATE)
            offspring2 = mutate(offspring2, MUTATION_RATE)
            
            # Add to new population
            new_population.append(offspring1)
            if len(new_population) < POPULATION_SIZE:
                new_population.append(offspring2)
        
        population = new_population
    
    # Final evaluation
    fitnesses = [evaluate_fitness(individual) for individual in population]
    return MAX_GENERATIONS, max(fitnesses)


def benchmark_single_run() -> float:
    """Run a single GA instance and return execution time in milliseconds."""
    start_time = time.perf_counter()
    generations, best_fitness = run_ga()
    end_time = time.perf_counter()
    
    elapsed_ms = (end_time - start_time) * 1000
    return elapsed_ms