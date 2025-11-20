# Genetic Algorithm Performance Comparison

A comprehensive benchmark comparing the execution speed and implementation characteristics of a genetic algorithm solving the One-Max problem across 11 different programming languages.
Note: This project and code were created using AI tools (Sonnet 4) as an experiment in AI code generation. Although the code runs I'm sure they could all be better optimized.

## Languages Tested

- **Julia** - High-performance scientific computing
- **Python** - General-purpose interpreted language
- **PyPy** - Python with JIT compilation (added during project)
- **F#** - Functional-first .NET language
- **Java** - Object-oriented JVM language
- **Clojure** - Functional Lisp dialect on JVM
- **C#** - Object-oriented .NET language
- **TypeScript** - Typed JavaScript superset
- **Swift** - Apple's systems programming language
- **Elixir** - Functional concurrent language on BEAM VM (added during project)
- **Go** - Systems programming language with garbage collection (added during project)

## The One-Max Problem

The One-Max problem is a classic genetic algorithm benchmark where the goal is to evolve a binary string of length 100 to maximize the number of 1s (target: all 1s).

### Algorithm Parameters
- Population size: 100 individuals
- Chromosome length: 100 bits
- Max generations: 500
- Crossover rate: 80%
- Mutation rate: 1% per bit
- Selection: Tournament selection (size 3)
- Crossover: Single-point crossover

## Project Structure

```
GATests/
├── DESIGN_DOCUMENT.md          # Detailed project specification
├── README.md                   # This file
├── implementations/            # Language implementations
│   ├── julia/
│   ├── python/
│   ├── fsharp/
│   ├── java/
│   ├── clojure/
│   ├── csharp/
│   ├── typescript/
│   ├── swift/
│   ├── elixir/
│   └── go/
├── scripts/
│   ├── run_all_tests.sh       # Master test runner
│   └── analyze_results.py     # Results analysis and plotting
└── results/
    ├── raw_data/              # Benchmark timing data
    └── analysis/              # Processed results and plots
```

## Key Discoveries and Project Evolution

### Critical Algorithmic Fix

During implementation, a major algorithmic inconsistency was discovered: some languages were recalculating fitness in every tournament selection (600+ evaluations per generation) while others pre-computed fitness once per generation (100 evaluations). This 6x difference in computational work was initially mistaken for language performance differences.

**Impact of the fix**:
- **Clojure**: Improved from 350ms to 13ms (27x faster!)
- **Java, Swift, TypeScript, C#**: All became significantly more competitive
- **Fair comparison**: Now reflects actual language performance rather than algorithmic implementation differences

### Performance Optimizations Added

1. **PyPy Runtime**: Added as alternative Python implementation
   - Performance: 4.77ms vs CPython's 18.81ms (3.9x improvement)
   - Demonstrates JIT compilation benefits

2. **Aggressive Swift Optimization**: Enhanced compiler flags
   - Added `-whole-module-optimization -cross-module-optimization`
   - Improved peak performance by 14%

3. **Build System Fixes**: Resolved multiple automation issues
   - Fixed directory navigation problems
   - Updated framework versions for compatibility
   - Corrected language-specific compilation issues

## Final Performance Results

After implementing algorithmic consistency fixes and optimizations, here are the benchmark results (25 runs each, mean execution time):

| Rank | Language   | Mean Time | Relative Speed | Notes |
|------|------------|-----------|----------------|--------|
| 1    | Julia      | 2.01 ms   | 1.00x         | JIT scientific computing |
| 2    | Go         | 3.62 ms   | 1.80x         | Systems language with GC |
| 3    | Java       | 3.67 ms   | 1.83x         | JVM optimization |
| 4    | F#         | 3.87 ms   | 1.93x         | Functional .NET |
| 5    | PyPy       | 4.68 ms   | 2.33x         | JIT Python |
| 6    | TypeScript | 5.49 ms   | 2.73x         | V8 JavaScript |
| 7    | C#         | 9.00 ms   | 4.48x         | .NET OOP |
| 8    | Clojure    | 12.43 ms  | 6.18x         | Functional Lisp |
| 9    | Swift      | 14.84 ms  | 7.39x         | Systems language |
| 10   | Python     | 19.17 ms  | 9.54x         | Interpreted CPython |
| 11   | Elixir     | 21.84 ms  | 10.87x        | Functional concurrent (BEAM VM) |

**Key Insights:**
- **Julia leads** with excellent JIT optimization for numerical computing
- **Compiled languages** (F#, Java) show strong performance
- **PyPy dramatically improves Python** by 3.8x over CPython
- **Elixir shows BEAM VM overhead** for CPU-intensive tasks vs concurrent workloads
- **Algorithmic consistency** was crucial for fair comparison
- **Runtime choice matters** as much as language choice

## Requirements

### Core Requirements
- **Julia** 1.6+
- **Python** 3.8+ with matplotlib, seaborn, pandas, scipy, numpy
- **Java** 11+ (OpenJDK recommended)
- **Node.js** 16+ and TypeScript

### Optional (for full comparison)
- **.NET** 6.0+ (for F# and C#)
- **Clojure** 1.10+
- **Swift** 5.0+ (macOS/Linux)

## Quick Start

1. **Clone or navigate to the project directory**
2. **Install Python dependencies:**
   ```bash
   pip install matplotlib seaborn pandas scipy numpy
   ```

3. **Run the complete benchmark:**
   ```bash
   ./scripts/run_all_tests.sh
   ```

4. **Generate analysis and plots:**
   ```bash
   python3 scripts/analyze_results.py
   ```

## Running Individual Languages

Each implementation can be tested individually:

```bash
# Julia
cd implementations/julia && julia run_tests.jl

# Python
cd implementations/python && python3 run_tests.py

# F# (with .NET)
cd implementations/fsharp && dotnet run --configuration Release

# Java
cd implementations/java && javac *.java && java RunTests

# Clojure
cd implementations/clojure && clojure run_tests.clj

# C# (with .NET)
cd implementations/csharp && dotnet run --configuration Release

# TypeScript
cd implementations/typescript && npm install && npx tsc --target ES2020 *.ts && node run_tests.js

# Swift
cd implementations/swift && swift -O -o RunTests *.swift && ./RunTests
```

## Compilation Flags

For fair comparison, all compiled languages use standard optimization flags:
- **Swift**: `-O` (standard optimization)
- **C#**: Release mode with optimizations
- **F#**: Release mode compilation
- **Java**: Standard javac + JIT optimization
- **TypeScript**: Compiled to ES2020

## Output

The benchmark produces:
1. **Raw timing data** (`results/raw_data/benchmark_results.csv`)
2. **Performance visualization** (`results/analysis/performance_comparison.png`)
3. **Statistical summary** (`results/analysis/performance_summary.txt`)
4. **Detailed statistics** (`results/analysis/detailed_statistics.csv`)

## Methodology

- **25 runs** per language for statistical significance
- **Identical algorithm** implementation across all languages
- **Pure execution time** measurement (excludes I/O, setup)
- **Statistical analysis** with confidence intervals
- **Controlled environment** with consistent parameters

## Results Interpretation

The benchmark measures:
- **Mean execution time** (primary metric)
- **Statistical variability** (standard deviation, CV)
- **Confidence intervals** (95% CI)
- **Relative performance** (speed factors)
- **Implementation consistency** across runs

## Language-Specific Notes

### Julia
- Uses type annotations for performance
- Leverages native array operations
- Benefits from just-ahead-of-time compilation

### Python
- Pure Python implementation (no NumPy for core GA)
- Uses built-in data structures
- Interpreted execution

### F#
- Functional programming style with immutable data
- Compiled to .NET bytecode
- Uses pattern matching and pipe operators

### Java
- Object-oriented design with proper encapsulation
- JIT compilation provides runtime optimization
- Uses ArrayList for dynamic collections

### Clojure
- Functional programming with immutable data structures
- Runs on JVM with JIT compilation
- Uses persistent data structures

### C#
- Modern C# features (LINQ, generics, tuples)
- Compiled to .NET bytecode
- Object-oriented with functional elements

### TypeScript
- Compiled to optimized JavaScript (ES2020)
- Static typing for better performance
- Runs on V8 JavaScript engine

### Swift
- Value types and reference types
- Compiled to native code
- Automatic Reference Counting (ARC)

## Troubleshooting

### Missing Compilers/Runtimes
The test runner will skip languages that aren't installed and mark them as ERROR in the results.

### Performance Variations
- Run on a quiet system with minimal background processes
- Results may vary between runs due to system load
- The benchmark includes 25 runs per language to account for variability

### Common Issues
- **F#/C#**: Requires .NET SDK
- **Clojure**: May need manual installation of Clojure tools
- **Swift**: Only available on macOS and Linux
- **TypeScript**: Needs Node.js and npm/TypeScript compiler

## License

This project is for educational and benchmarking purposes. Each language implementation follows the same algorithmic specification for fair comparison.

---

**Note**: Performance results are specific to the hardware, operating system, and language versions used. Results should be interpreted as relative comparisons rather than absolute benchmarks.
