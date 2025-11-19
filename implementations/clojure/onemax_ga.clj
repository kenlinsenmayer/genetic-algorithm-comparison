;; Improved One-Max Genetic Algorithm Implementation in Clojure
;; Author: Genetic Algorithm Performance Comparison Project  
;; Date: November 19, 2025

(ns onemax-ga
  (:require [clojure.string :as str]))

;; GA Parameters
(def ^:const POPULATION-SIZE 100)
(def ^:const CHROMOSOME-LENGTH 100) 
(def ^:const MAX-GENERATIONS 500)
(def ^:const CROSSOVER-RATE 0.8)
(def ^:const MUTATION-RATE 0.01)
(def ^:const TOURNAMENT-SIZE 3)

;; Use type hints and more efficient operations
(defn random-individual
  "Create a random individual (vector of booleans)."
  [^long length]
  (vec (repeatedly length #(< (rand) 0.5))))

(defn initialize-population  
  "Initialize a random population of binary individuals."
  [^long size ^long length]
  (vec (repeatedly size #(random-individual length))))

(defn evaluate-fitness
  "Evaluate fitness of an individual (count of trues)."
  [individual]
  ;; Use reduce instead of filter for better performance
  (reduce (fn [acc bit] (if bit (inc acc) acc)) 0 individual))

(defn tournament-selection
  "Tournament selection with pre-computed fitnesses."
  [population fitnesses ^long tournament-size]
  (let [pop-size (count population)]
    (loop [i 0 best-idx 0 best-fitness -1]
      (if (< i tournament-size)
        (let [candidate-idx (rand-int pop-size)
              candidate-fitness (nth fitnesses candidate-idx)]
          (if (> candidate-fitness best-fitness)
            (recur (inc i) candidate-idx candidate-fitness)
            (recur (inc i) best-idx best-fitness)))
        (nth population best-idx)))))

(defn single-point-crossover
  "Single-point crossover between two parents."
  [parent1 parent2]
  (if (> (rand) CROSSOVER-RATE)
    [parent1 parent2]
    (let [crossover-point (inc (rand-int (dec (count parent1))))]
      ;; Use subvec for better performance than concat
      [(vec (concat (subvec parent1 0 crossover-point) 
                    (subvec parent2 crossover-point)))
       (vec (concat (subvec parent2 0 crossover-point)
                    (subvec parent1 crossover-point)))])))

(defn mutate
  "Mutate an individual with specified mutation rate."
  [individual ^double mutation-rate]
  ;; Use mapv with type hint
  (mapv #(if (< (rand) mutation-rate) (not %) %) individual))

(defn create-new-generation
  "Create a new generation from current population."
  [population fitnesses]
  ;; Pre-calculate population size and use loop/recur
  (loop [new-pop [] i 0]
    (if (>= i POPULATION-SIZE)
      new-pop
      (let [parent1 (tournament-selection population fitnesses TOURNAMENT-SIZE)
            parent2 (tournament-selection population fitnesses TOURNAMENT-SIZE)
            [offspring1 offspring2] (single-point-crossover parent1 parent2)
            mutated1 (mutate offspring1 MUTATION-RATE)
            mutated2 (mutate offspring2 MUTATION-RATE)]
        (if (< (inc i) POPULATION-SIZE)
          (recur (conj (conj new-pop mutated1) mutated2) (+ i 2))
          (recur (conj new-pop mutated1) (inc i)))))))

(defn run-ga-improved
  "Main genetic algorithm function with improvements."
  []
  (loop [population (initialize-population POPULATION-SIZE CHROMOSOME-LENGTH)
         generation 1]
    ;; Pre-compute fitnesses once per generation
    (let [fitnesses (mapv evaluate-fitness population)
          max-fitness (apply max fitnesses)]
      (cond
        (= max-fitness CHROMOSOME-LENGTH) [generation max-fitness]
        (>= generation MAX-GENERATIONS) [MAX-GENERATIONS max-fitness]
        :else (recur (create-new-generation population fitnesses) (inc generation))))))

(defn benchmark-single-run
  "Run a single GA instance and return execution time in milliseconds."
  []
  (let [start-time (System/nanoTime)
        [generations best-fitness] (run-ga-improved)
        end-time (System/nanoTime)
        elapsed-ms (/ (- end-time start-time) 1000000.0)]
    elapsed-ms))

(defn run-tests
  "Run the GA benchmark multiple times."
  [num-runs]
  (println "Clojure One-Max GA Performance Test")
  (println (str "Running " num-runs " tests..."))
  
  (let [times (atom [])]
    (dotimes [i num-runs]
      (let [elapsed (benchmark-single-run)]
        (swap! times conj elapsed)
        (print (str "Run " (inc i) ": " (format "%.3f" elapsed) " ms\r"))
        (flush)))
    
    (println (str "\nCompleted " num-runs " runs"))
    
    ;; Output results in CSV format
    (let [times-str (clojure.string/join "," @times)]
      (println (str "clojure," times-str)))
    
    @times))

;; Main execution for benchmarking
(run-tests 25)