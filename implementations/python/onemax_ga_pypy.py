#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyPy-compatible One-Max Genetic Algorithm
Python 2.7 version without type annotations
"""

import random
import time

# GA Parameters
POPULATION_SIZE = 100
CHROMOSOME_LENGTH = 100
MAX_GENERATIONS = 500
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.01

def create_individual():
    """Create a random binary chromosome."""
    return [random.randint(0, 1) for _ in range(CHROMOSOME_LENGTH)]

def create_population():
    """Create initial population."""
    return [create_individual() for _ in range(POPULATION_SIZE)]

def fitness(individual):
    """Calculate fitness (number of 1s in chromosome)."""
    return sum(individual)

def tournament_selection(population, fitnesses, tournament_size=3):
    """Select parent using tournament selection with pre-computed fitnesses."""
    tournament_indices = random.sample(range(len(population)), tournament_size)
    best_idx = max(tournament_indices, key=lambda i: fitnesses[i])
    return population[best_idx]

def crossover(parent1, parent2):
    """Single-point crossover."""
    if random.random() > CROSSOVER_RATE:
        return parent1[:], parent2[:]
    
    point = random.randint(1, CHROMOSOME_LENGTH - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(individual):
    """Bit-flip mutation."""
    mutated = individual[:]
    for i in range(len(mutated)):
        if random.random() < MUTATION_RATE:
            mutated[i] = 1 - mutated[i]
    return mutated

def create_new_generation(population, fitnesses):
    """Create new generation using selection, crossover, and mutation."""
    new_population = []
    
    while len(new_population) < POPULATION_SIZE:
        parent1 = tournament_selection(population, fitnesses)
        parent2 = tournament_selection(population, fitnesses)
        
        child1, child2 = crossover(parent1, parent2)
        
        child1 = mutate(child1)
        child2 = mutate(child2)
        
        new_population.extend([child1, child2])
    
    return new_population[:POPULATION_SIZE]

def run_ga():
    """Run the genetic algorithm and return (generations, best_fitness)."""
    population = create_population()
    generation = 0
    
    while generation < MAX_GENERATIONS:
        # Pre-compute fitnesses once per generation
        fitnesses = [fitness(individual) for individual in population]
        max_fitness = max(fitnesses)
        
        if max_fitness >= CHROMOSOME_LENGTH:
            return generation, max_fitness
        
        population = create_new_generation(population, fitnesses)
        generation += 1
    
    # Final fitness calculation
    fitnesses = [fitness(individual) for individual in population]
    max_fitness = max(fitnesses)
    return MAX_GENERATIONS, max_fitness

def benchmark_single_run():
    """Run a single GA instance and return execution time in milliseconds."""
    start_time = time.time()
    generations, best_fitness = run_ga()
    end_time = time.time()
    elapsed_ms = (end_time - start_time) * 1000.0
    return elapsed_ms

def run_tests(num_runs=25):
    """Run the GA benchmark multiple times."""
    print("PyPy One-Max GA Performance Test")
    print("Running {} tests...".format(num_runs))
    
    times = []
    for i in range(num_runs):
        elapsed = benchmark_single_run()
        times.append(elapsed)
        print("Run {}: {:.3f} ms\r".format(i + 1, elapsed)),
    
    print("\nCompleted {} runs".format(num_runs))
    
    # Output results in CSV format
    times_str = ",".join(str(t) for t in times)
    print("pypy,{}".format(times_str))
    
    return times

if __name__ == "__main__":
    run_tests(25)