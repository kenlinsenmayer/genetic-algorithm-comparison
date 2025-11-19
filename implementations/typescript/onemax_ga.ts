// One-Max Genetic Algorithm Implementation in TypeScript
// Author: Genetic Algorithm Performance Comparison Project
// Date: November 19, 2025

// GA Parameters
const POPULATION_SIZE = 100;
const CHROMOSOME_LENGTH = 100;
const MAX_GENERATIONS = 500;
const CROSSOVER_RATE = 0.8;
const MUTATION_RATE = 0.01;
const TOURNAMENT_SIZE = 3;

type Individual = boolean[];
type Population = Individual[];

/**
 * Initialize a random population of binary individuals.
 */
function initializePopulation(size: number, length: number): Population {
    const population: Population = [];
    for (let i = 0; i < size; i++) {
        const individual: Individual = [];
        for (let j = 0; j < length; j++) {
            individual.push(Math.random() < 0.5);
        }
        population.push(individual);
    }
    return population;
}

/**
 * Evaluate fitness of an individual (count of trues).
 */
function evaluateFitness(individual: Individual): number {
    return individual.filter(gene => gene).length;
}

/**
 * Tournament selection with pre-computed fitnesses.
 */
function tournamentSelection(population: Population, fitnesses: number[], tournamentSize: number): Individual {
    let best: Individual | null = null;
    let bestFitness = -1;

    for (let i = 0; i < tournamentSize; i++) {
        const candidateIndex = Math.floor(Math.random() * population.length);
        const candidate = population[candidateIndex];
        const fitness = fitnesses[candidateIndex];

        if (fitness > bestFitness) {
            bestFitness = fitness;
            best = candidate;
        }
    }

    return [...(best as Individual)]; // Copy the individual
}

/**
 * Single-point crossover between two parents.
 */
function singlePointCrossover(parent1: Individual, parent2: Individual): [Individual, Individual] {
    if (Math.random() > CROSSOVER_RATE) {
        return [[...parent1], [...parent2]];
    }

    const crossoverPoint = Math.floor(Math.random() * (CHROMOSOME_LENGTH - 1)) + 1;

    const offspring1 = [
        ...parent1.slice(0, crossoverPoint),
        ...parent2.slice(crossoverPoint)
    ];

    const offspring2 = [
        ...parent2.slice(0, crossoverPoint),
        ...parent1.slice(crossoverPoint)
    ];

    return [offspring1, offspring2];
}

/**
 * Mutate an individual with specified mutation rate.
 */
function mutate(individual: Individual, mutationRate: number): Individual {
    return individual.map(gene => 
        Math.random() < mutationRate ? !gene : gene
    );
}

/**
 * Main genetic algorithm function.
 * Returns [generations, bestFitness].
 */
function runGA(): [number, number] {
    let population = initializePopulation(POPULATION_SIZE, CHROMOSOME_LENGTH);

    for (let generation = 1; generation <= MAX_GENERATIONS; generation++) {
        const fitnesses = population.map(evaluateFitness);
        const maxFitness = Math.max(...fitnesses);

        if (maxFitness === CHROMOSOME_LENGTH) {
            return [generation, maxFitness];
        }

        const newPopulation: Population = [];

        while (newPopulation.length < POPULATION_SIZE) {
            const parent1 = tournamentSelection(population, fitnesses, TOURNAMENT_SIZE);
            const parent2 = tournamentSelection(population, fitnesses, TOURNAMENT_SIZE);

            const [offspring1, offspring2] = singlePointCrossover(parent1, parent2);

            const mutatedOffspring1 = mutate(offspring1, MUTATION_RATE);
            const mutatedOffspring2 = mutate(offspring2, MUTATION_RATE);

            newPopulation.push(mutatedOffspring1);
            if (newPopulation.length < POPULATION_SIZE) {
                newPopulation.push(mutatedOffspring2);
            }
        }

        population = newPopulation;
    }

    const finalFitnesses = population.map(evaluateFitness);
    return [MAX_GENERATIONS, Math.max(...finalFitnesses)];
}

/**
 * Run a single GA instance and return execution time in milliseconds.
 */
export function benchmarkSingleRun(): number {
    const startTime = performance.now();
    const [generations, bestFitness] = runGA();
    const endTime = performance.now();

    return endTime - startTime;
}

// Export for CommonJS compatibility
declare const module: any;
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { benchmarkSingleRun };
}