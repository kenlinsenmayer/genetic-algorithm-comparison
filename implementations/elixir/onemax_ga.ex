defmodule OneMaxGA do
  @moduledoc """
  One-Max Genetic Algorithm implementation in Elixir
  
  This module implements a genetic algorithm to solve the One-Max problem,
  where the goal is to evolve a binary string to maximize the number of 1s.
  """

  # GA Parameters
  @population_size 100
  @chromosome_length 100
  @max_generations 500
  @crossover_rate 0.8
  @mutation_rate 0.01

  @doc """
  Create a random binary chromosome of specified length.
  """
  def create_individual do
    for _ <- 1..@chromosome_length, do: Enum.random(0..1)
  end

  @doc """
  Create initial population of random individuals.
  """
  def create_population do
    for _ <- 1..@population_size, do: create_individual()
  end

  @doc """
  Calculate fitness (number of 1s in chromosome).
  """
  def fitness(individual) do
    Enum.sum(individual)
  end

  @doc """
  Tournament selection with pre-computed fitnesses.
  """
  def tournament_selection(population, fitnesses, tournament_size \\ 3) do
    tournament_indices = Enum.take_random(0..length(population)-1, tournament_size)
    
    best_index = tournament_indices
                 |> Enum.max_by(fn i -> Enum.at(fitnesses, i) end)
    
    Enum.at(population, best_index)
  end

  @doc """
  Single-point crossover between two parents.
  """
  def crossover(parent1, parent2) do
    if :rand.uniform() > @crossover_rate do
      {parent1, parent2}
    else
      point = :rand.uniform(@chromosome_length - 1)
      
      {p1_left, p1_right} = Enum.split(parent1, point)
      {p2_left, p2_right} = Enum.split(parent2, point)
      
      child1 = p1_left ++ p2_right
      child2 = p2_left ++ p1_right
      
      {child1, child2}
    end
  end

  @doc """
  Bit-flip mutation for an individual.
  """
  def mutate(individual) do
    individual
    |> Enum.map(fn bit ->
      if :rand.uniform() < @mutation_rate do
        1 - bit
      else
        bit
      end
    end)
  end

  @doc """
  Create new generation using selection, crossover, and mutation.
  """
  def create_new_generation(population, fitnesses) do
    create_new_generation(population, fitnesses, [])
  end

  defp create_new_generation(population, fitnesses, acc) when length(acc) >= @population_size do
    Enum.take(acc, @population_size)
  end

  defp create_new_generation(population, fitnesses, acc) do
    parent1 = tournament_selection(population, fitnesses)
    parent2 = tournament_selection(population, fitnesses)
    
    {child1, child2} = crossover(parent1, parent2)
    
    child1 = mutate(child1)
    child2 = mutate(child2)
    
    create_new_generation(population, fitnesses, [child1, child2 | acc])
  end

  @doc """
  Run the genetic algorithm and return {generations, best_fitness}.
  """
  def run_ga do
    population = create_population()
    run_ga_loop(population, 0)
  end

  defp run_ga_loop(population, generation) when generation >= @max_generations do
    fitnesses = Enum.map(population, &fitness/1)
    max_fitness = Enum.max(fitnesses)
    {@max_generations, max_fitness}
  end

  defp run_ga_loop(population, generation) do
    # Pre-compute fitnesses once per generation
    fitnesses = Enum.map(population, &fitness/1)
    max_fitness = Enum.max(fitnesses)
    
    if max_fitness >= @chromosome_length do
      {generation, max_fitness}
    else
      new_population = create_new_generation(population, fitnesses)
      run_ga_loop(new_population, generation + 1)
    end
  end

  @doc """
  Run a single GA instance and return execution time in milliseconds.
  """
  def benchmark_single_run do
    start_time = :erlang.monotonic_time(:millisecond)
    {_generations, _best_fitness} = run_ga()
    end_time = :erlang.monotonic_time(:millisecond)
    
    end_time - start_time
  end

  @doc """
  Run the GA benchmark multiple times.
  """
  def run_tests(num_runs \\ 25) do
    IO.puts("Elixir One-Max GA Performance Test")
    IO.puts("Running #{num_runs} tests...")
    
    times = for i <- 1..num_runs do
      elapsed = benchmark_single_run()
      IO.write("\rRun #{i}: #{elapsed} ms")
      elapsed
    end
    
    IO.puts("\nCompleted #{num_runs} runs")
    
    # Output results in CSV format
    times_str = times |> Enum.map(&to_string/1) |> Enum.join(",")
    IO.puts("elixir,#{times_str}")
    
    times
  end
end

# Main execution when run as script
if System.argv() |> length() == 0 do
  OneMaxGA.run_tests(25)
end