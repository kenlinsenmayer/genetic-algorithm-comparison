package main

import (
	"fmt"
	"math/rand"
	"time"
)

const (
	PopulationSize   = 100
	ChromosomeLength = 100
	MaxGenerations   = 500
	CrossoverRate    = 0.8
	MutationRate     = 0.01
)

type Individual []int

func createIndividual() Individual {
	individual := make(Individual, ChromosomeLength)
	for i := 0; i < ChromosomeLength; i++ {
		individual[i] = rand.Intn(2)
	}
	return individual
}

func createPopulation() []Individual {
	population := make([]Individual, PopulationSize)
	for i := 0; i < PopulationSize; i++ {
		population[i] = createIndividual()
	}
	return population
}

func fitness(individual Individual) int {
	sum := 0
	for _, bit := range individual {
		sum += bit
	}
	return sum
}

func tournamentSelection(population []Individual, fitnesses []int) Individual {
	tournamentSize := 3
	tournamentIndices := make([]int, tournamentSize)
	
	for i := 0; i < tournamentSize; i++ {
		tournamentIndices[i] = rand.Intn(len(population))
	}
	
	bestIndex := tournamentIndices[0]
	bestFitness := fitnesses[bestIndex]
	
	for _, idx := range tournamentIndices[1:] {
		if fitnesses[idx] > bestFitness {
			bestIndex = idx
			bestFitness = fitnesses[idx]
		}
	}
	
	result := make(Individual, len(population[bestIndex]))
	copy(result, population[bestIndex])
	return result
}

func crossover(parent1, parent2 Individual) (Individual, Individual) {
	if rand.Float64() > CrossoverRate {
		child1 := make(Individual, len(parent1))
		child2 := make(Individual, len(parent2))
		copy(child1, parent1)
		copy(child2, parent2)
		return child1, child2
	}
	
	point := rand.Intn(ChromosomeLength-1) + 1
	
	child1 := make(Individual, ChromosomeLength)
	child2 := make(Individual, ChromosomeLength)
	
	copy(child1[:point], parent1[:point])
	copy(child1[point:], parent2[point:])
	
	copy(child2[:point], parent2[:point])
	copy(child2[point:], parent1[point:])
	
	return child1, child2
}

func mutate(individual Individual) Individual {
	mutated := make(Individual, len(individual))
	copy(mutated, individual)
	
	for i := 0; i < len(mutated); i++ {
		if rand.Float64() < MutationRate {
			mutated[i] = 1 - mutated[i]
		}
	}
	
	return mutated
}

func createNewGeneration(population []Individual, fitnesses []int) []Individual {
	newPopulation := make([]Individual, 0, PopulationSize)
	
	for len(newPopulation) < PopulationSize {
		parent1 := tournamentSelection(population, fitnesses)
		parent2 := tournamentSelection(population, fitnesses)
		
		child1, child2 := crossover(parent1, parent2)
		
		child1 = mutate(child1)
		child2 = mutate(child2)
		
		newPopulation = append(newPopulation, child1, child2)
	}
	
	return newPopulation[:PopulationSize]
}

func runGA() (int, int) {
	population := createPopulation()
	
	for generation := 0; generation < MaxGenerations; generation++ {
		fitnesses := make([]int, len(population))
		maxFitness := 0
		
		for i, individual := range population {
			fitnesses[i] = fitness(individual)
			if fitnesses[i] > maxFitness {
				maxFitness = fitnesses[i]
			}
		}
		
		if maxFitness >= ChromosomeLength {
			return generation, maxFitness
		}
		
		population = createNewGeneration(population, fitnesses)
	}
	
	fitnesses := make([]int, len(population))
	maxFitness := 0
	for i, individual := range population {
		fitnesses[i] = fitness(individual)
		if fitnesses[i] > maxFitness {
			maxFitness = fitnesses[i]
		}
	}
	
	return MaxGenerations, maxFitness
}

func benchmarkSingleRun() float64 {
	start := time.Now()
	runGA()
	elapsed := time.Since(start)
	return float64(elapsed.Nanoseconds()) / 1000000.0
}

func runTests(numRuns int) []float64 {
	fmt.Println("Go One-Max GA Performance Test")
	fmt.Printf("Running %d tests...\n", numRuns)
	
	times := make([]float64, numRuns)
	
	for i := 0; i < numRuns; i++ {
		elapsed := benchmarkSingleRun()
		times[i] = elapsed
		fmt.Printf("\rRun %d: %.3f ms", i+1, elapsed)
	}
	
	fmt.Printf("\nCompleted %d runs\n", numRuns)
	
	fmt.Print("go,")
	for i, time := range times {
		if i > 0 {
			fmt.Print(",")
		}
		fmt.Printf("%.6f", time)
	}
	fmt.Println()
	
	return times
}

func main() {
	rand.Seed(time.Now().UnixNano())
	runTests(25)
}