// One-Max Genetic Algorithm Implementation in C#
// Author: Genetic Algorithm Performance Comparison Project
// Date: November 19, 2025

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;

public class OneMaxGA
{
    // GA Parameters
    private const int POPULATION_SIZE = 100;
    private const int CHROMOSOME_LENGTH = 100;
    private const int MAX_GENERATIONS = 500;
    private const double CROSSOVER_RATE = 0.8;
    private const double MUTATION_RATE = 0.01;
    private const int TOURNAMENT_SIZE = 3;

    private static readonly Random random = new Random();

    // Individual representation as boolean array
    public class Individual
    {
        public bool[] Genes { get; set; }

        public Individual(int length)
        {
            Genes = new bool[length];
            for (int i = 0; i < length; i++)
            {
                Genes[i] = random.NextDouble() < 0.5;
            }
        }

        public Individual(bool[] genes)
        {
            Genes = (bool[])genes.Clone();
        }

        public int Fitness => Genes.Count(gene => gene);

        public Individual Copy() => new Individual(Genes);
    }

    /// <summary>
    /// Initialize a random population of binary individuals.
    /// </summary>
    private static List<Individual> InitializePopulation(int size, int length)
    {
        return Enumerable.Range(0, size)
            .Select(_ => new Individual(length))
            .ToList();
    }

    /// <summary>
    /// Tournament selection with pre-computed fitnesses.
    /// </summary>
    private static Individual TournamentSelection(List<Individual> population, int[] fitnesses, int tournamentSize)
    {
        Individual best = null;
        int bestFitness = -1;

        for (int i = 0; i < tournamentSize; i++)
        {
            int candidateIndex = random.Next(population.Count);
            Individual candidate = population[candidateIndex];
            int fitness = fitnesses[candidateIndex];

            if (fitness > bestFitness)
            {
                bestFitness = fitness;
                best = candidate;
            }
        }

        return best.Copy();
    }

    /// <summary>
    /// Single-point crossover between two parents.
    /// </summary>
    private static (Individual, Individual) SinglePointCrossover(Individual parent1, Individual parent2)
    {
        if (random.NextDouble() > CROSSOVER_RATE)
        {
            return (parent1.Copy(), parent2.Copy());
        }

        int crossoverPoint = random.Next(1, CHROMOSOME_LENGTH);

        var offspring1Genes = parent1.Genes.Take(crossoverPoint)
            .Concat(parent2.Genes.Skip(crossoverPoint))
            .ToArray();

        var offspring2Genes = parent2.Genes.Take(crossoverPoint)
            .Concat(parent1.Genes.Skip(crossoverPoint))
            .ToArray();

        return (new Individual(offspring1Genes), new Individual(offspring2Genes));
    }

    /// <summary>
    /// Mutate an individual with specified mutation rate.
    /// </summary>
    private static void Mutate(Individual individual, double mutationRate)
    {
        for (int i = 0; i < individual.Genes.Length; i++)
        {
            if (random.NextDouble() < mutationRate)
            {
                individual.Genes[i] = !individual.Genes[i];
            }
        }
    }

    /// <summary>
    /// Main genetic algorithm function.
    /// Returns tuple with (generations, bestFitness).
    /// </summary>
    public static (int, int) RunGA()
    {
        var population = InitializePopulation(POPULATION_SIZE, CHROMOSOME_LENGTH);

        for (int generation = 1; generation <= MAX_GENERATIONS; generation++)
        {
            // Evaluate fitness once per generation
            var fitnesses = new int[population.Count];
            for (int i = 0; i < population.Count; i++)
            {
                fitnesses[i] = population[i].Fitness;
            }

            int maxFitness = fitnesses.Max();

            if (maxFitness == CHROMOSOME_LENGTH)
            {
                return (generation, maxFitness);
            }

            var newPopulation = new List<Individual>();

            while (newPopulation.Count < POPULATION_SIZE)
            {
                var parent1 = TournamentSelection(population, fitnesses, TOURNAMENT_SIZE);
                var parent2 = TournamentSelection(population, fitnesses, TOURNAMENT_SIZE);

                var (offspring1, offspring2) = SinglePointCrossover(parent1, parent2);

                Mutate(offspring1, MUTATION_RATE);
                Mutate(offspring2, MUTATION_RATE);

                newPopulation.Add(offspring1);
                if (newPopulation.Count < POPULATION_SIZE)
                {
                    newPopulation.Add(offspring2);
                }
            }

            population = newPopulation;
        }

        var finalFitnesses = new int[population.Count];
        for (int i = 0; i < population.Count; i++)
        {
            finalFitnesses[i] = population[i].Fitness;
        }
        int finalMaxFitness = finalFitnesses.Max();
        return (MAX_GENERATIONS, finalMaxFitness);
    }

    /// <summary>
    /// Run a single GA instance and return execution time in milliseconds.
    /// </summary>
    public static double BenchmarkSingleRun()
    {
        var stopwatch = Stopwatch.StartNew();
        var (generations, bestFitness) = RunGA();
        stopwatch.Stop();

        return stopwatch.Elapsed.TotalMilliseconds;
    }
}