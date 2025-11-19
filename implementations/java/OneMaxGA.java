// One-Max Genetic Algorithm Implementation in Java
// Author: Genetic Algorithm Performance Comparison Project
// Date: November 19, 2025

import java.util.*;

public class OneMaxGA {
    // GA Parameters
    private static final int POPULATION_SIZE = 100;
    private static final int CHROMOSOME_LENGTH = 100;
    private static final int MAX_GENERATIONS = 500;
    private static final double CROSSOVER_RATE = 0.8;
    private static final double MUTATION_RATE = 0.01;
    private static final int TOURNAMENT_SIZE = 3;
    
    private static final Random random = new Random();
    
    // Individual representation as boolean array
    private static class Individual {
        private boolean[] genes;
        
        public Individual(int length) {
            genes = new boolean[length];
            for (int i = 0; i < length; i++) {
                genes[i] = random.nextBoolean();
            }
        }
        
        public Individual(boolean[] genes) {
            this.genes = genes.clone();
        }
        
        public boolean[] getGenes() {
            return genes.clone();
        }
        
        public int getFitness() {
            int count = 0;
            for (boolean gene : genes) {
                if (gene) count++;
            }
            return count;
        }
        
        public Individual copy() {
            return new Individual(this.genes);
        }
    }
    
    /**
     * Initialize a random population of binary individuals.
     */
    private static List<Individual> initializePopulation(int size, int length) {
        List<Individual> population = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            population.add(new Individual(length));
        }
        return population;
    }
    
    /**
     * Tournament selection with pre-computed fitnesses.
     */
    private static Individual tournamentSelection(List<Individual> population, int[] fitnesses, int tournamentSize) {
        Individual best = null;
        int bestFitness = -1;
        
        for (int i = 0; i < tournamentSize; i++) {
            int candidateIndex = random.nextInt(population.size());
            Individual candidate = population.get(candidateIndex);
            int fitness = fitnesses[candidateIndex];
            if (fitness > bestFitness) {
                bestFitness = fitness;
                best = candidate;
            }
        }
        
        return best.copy();
    }
    
    /**
     * Single-point crossover between two parents.
     */
    private static Individual[] singlePointCrossover(Individual parent1, Individual parent2) {
        if (random.nextDouble() > CROSSOVER_RATE) {
            return new Individual[]{parent1.copy(), parent2.copy()};
        }
        
        int crossoverPoint = random.nextInt(CHROMOSOME_LENGTH - 1) + 1;
        boolean[] genes1 = parent1.getGenes();
        boolean[] genes2 = parent2.getGenes();
        
        boolean[] offspring1Genes = new boolean[CHROMOSOME_LENGTH];
        boolean[] offspring2Genes = new boolean[CHROMOSOME_LENGTH];
        
        System.arraycopy(genes1, 0, offspring1Genes, 0, crossoverPoint);
        System.arraycopy(genes2, crossoverPoint, offspring1Genes, crossoverPoint, 
                        CHROMOSOME_LENGTH - crossoverPoint);
        
        System.arraycopy(genes2, 0, offspring2Genes, 0, crossoverPoint);
        System.arraycopy(genes1, crossoverPoint, offspring2Genes, crossoverPoint, 
                        CHROMOSOME_LENGTH - crossoverPoint);
        
        return new Individual[]{new Individual(offspring1Genes), new Individual(offspring2Genes)};
    }
    
    /**
     * Mutate an individual with specified mutation rate.
     */
    private static void mutate(Individual individual, double mutationRate) {
        boolean[] genes = individual.genes;
        for (int i = 0; i < genes.length; i++) {
            if (random.nextDouble() < mutationRate) {
                genes[i] = !genes[i];
            }
        }
    }
    
    /**
     * Main genetic algorithm function.
     * Returns array with [generations, bestFitness].
     */
    public static int[] runGA() {
        // Initialize population
        List<Individual> population = initializePopulation(POPULATION_SIZE, CHROMOSOME_LENGTH);
        
        for (int generation = 1; generation <= MAX_GENERATIONS; generation++) {
            // Evaluate fitness once per generation
            int[] fitnesses = new int[population.size()];
            for (int i = 0; i < population.size(); i++) {
                fitnesses[i] = population.get(i).getFitness();
            }
            
            // Check for optimal solution
            int maxFitness = 0;
            for (int fitness : fitnesses) {
                if (fitness > maxFitness) maxFitness = fitness;
            }
            
            if (maxFitness == CHROMOSOME_LENGTH) {
                return new int[]{generation, maxFitness};
            }
            
            // Create new population
            List<Individual> newPopulation = new ArrayList<>();
            
            while (newPopulation.size() < POPULATION_SIZE) {
                // Selection
                Individual parent1 = tournamentSelection(population, fitnesses, TOURNAMENT_SIZE);
                Individual parent2 = tournamentSelection(population, fitnesses, TOURNAMENT_SIZE);
                
                // Crossover
                Individual[] offspring = singlePointCrossover(parent1, parent2);
                
                // Mutation
                mutate(offspring[0], MUTATION_RATE);
                mutate(offspring[1], MUTATION_RATE);
                
                // Add to new population
                newPopulation.add(offspring[0]);
                if (newPopulation.size() < POPULATION_SIZE) {
                    newPopulation.add(offspring[1]);
                }
            }
            
            population = newPopulation;
        }
        
        // Final evaluation
        int[] finalFitnesses = new int[population.size()];
        for (int i = 0; i < population.size(); i++) {
            finalFitnesses[i] = population.get(i).getFitness();
        }
        int finalMaxFitness = 0;
        for (int fitness : finalFitnesses) {
            if (fitness > finalMaxFitness) finalMaxFitness = fitness;
        }
        
        return new int[]{MAX_GENERATIONS, finalMaxFitness};
    }
    
    /**
     * Run a single GA instance and return execution time in milliseconds.
     */
    public static double benchmarkSingleRun() {
        long startTime = System.nanoTime();
        int[] result = runGA();
        long endTime = System.nanoTime();
        
        return (endTime - startTime) / 1_000_000.0;
    }
}