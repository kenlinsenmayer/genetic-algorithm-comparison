#!/bin/bash
# Master test runner for Genetic Algorithm Performance Comparison
# Author: Genetic Algorithm Performance Comparison Project
# Date: November 19, 2025

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Results directory
RESULTS_DIR="$(pwd)/results/raw_data"
mkdir -p "$RESULTS_DIR"

# Output file
OUTPUT_FILE="$RESULTS_DIR/benchmark_results.csv"

echo "=== Genetic Algorithm Performance Comparison ==="
echo "Running benchmarks for all 8 languages..."
echo "Results will be saved to: $OUTPUT_FILE"
echo

# Initialize CSV file with header
echo "language,run1,run2,run3,run4,run5,run6,run7,run8,run9,run10,run11,run12,run13,run14,run15,run16,run17,run18,run19,run20,run21,run22,run23,run24,run25" > "$OUTPUT_FILE"

# Function to run a language test
run_language_test() {
    local lang="$1"
    local dir="$2"
    local command="$3"
    
    echo -e "${YELLOW}Testing $lang...${NC}"
    cd "$dir"
    
    # Capture output and append to CSV
    if eval "$command" >> "$OUTPUT_FILE" 2>/dev/null; then
        echo -e "${GREEN}✓ $lang completed successfully${NC}"
    else
        echo -e "${RED}✗ $lang failed${NC}"
        echo "$lang,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR" >> "$OUTPUT_FILE"
    fi
    
    cd - > /dev/null
}

# Julia
echo -e "${YELLOW}=== Running Julia GA ===${NC}"
run_language_test "Julia" "implementations/julia" "julia run_tests.jl"

# Python
echo -e "${YELLOW}=== Running Python GA ===${NC}"
run_language_test "Python" "implementations/python" "python3 run_tests.py"

# PyPy (if available)
echo -e "${YELLOW}=== Running PyPy GA ===${NC}"
if command -v pypy &> /dev/null; then
    run_language_test "PyPy" "implementations/python" "pypy onemax_ga_pypy.py"
else
    echo -e "${RED}✗ PyPy not found${NC}"
    echo "pypy,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR" >> "$OUTPUT_FILE"
fi

# F#
echo -e "${YELLOW}=== Running F# GA ===${NC}"
if command -v dotnet &> /dev/null; then
    echo "Compiling F#..."
    cd implementations/fsharp
    if [ ! -f "OneMaxGA.fsproj" ]; then
        cat > OneMaxGA.fsproj << 'EOF'
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
  </PropertyGroup>
  <ItemGroup>
    <Compile Include="OneMaxGA.fs" />
    <Compile Include="run_tests.fsx" />
  </ItemGroup>
</Project>
EOF
    fi
    dotnet build --configuration Release > /dev/null 2>&1
    cd - > /dev/null
    run_language_test "F#" "implementations/fsharp" "dotnet run --configuration Release"
elif command -v fsharpi &> /dev/null; then
    # Use F# interactive
    run_language_test "F#" "implementations/fsharp" "fsharpi run_tests.fsx"
else
    echo -e "${RED}✗ F# compiler not found${NC}"
    echo "fsharp,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR" >> "$OUTPUT_FILE"
fi

# Java
echo -e "${YELLOW}=== Running Java GA ===${NC}"
echo "Compiling Java..."
cd implementations/java
if javac *.java 2>/dev/null; then
    cd - > /dev/null
    run_language_test "Java" "implementations/java" "java RunTests"
else
    echo -e "${RED}✗ Java compilation failed${NC}"
    echo "java,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR" >> "$OUTPUT_FILE"
    cd - > /dev/null
fi

# Clojure
echo -e "${YELLOW}=== Running Clojure GA ===${NC}"
if command -v clojure &> /dev/null; then
    run_language_test "Clojure" "implementations/clojure" "clojure -M onemax_ga.clj"
elif command -v java &> /dev/null && [ -f "/usr/local/lib/clojure.jar" ]; then
    # Fallback to java -cp if clojure command not available
    run_language_test "Clojure" "implementations/clojure" "java -cp /usr/local/lib/clojure.jar clojure.main onemax_ga.clj"
else
    echo -e "${RED}✗ Clojure not found${NC}"
    echo "clojure,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR" >> "$OUTPUT_FILE"
fi

# C#
echo -e "${YELLOW}=== Running C# GA ===${NC}"
if command -v dotnet &> /dev/null; then
    echo "Compiling C#..."
    cd implementations/csharp
    if [ ! -f "OneMaxGA.csproj" ]; then
        cat > OneMaxGA.csproj << 'EOF'
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
    <StartupObject>RunTests</StartupObject>
  </PropertyGroup>
</Project>
EOF
    fi
    dotnet build --configuration Release > /dev/null 2>&1
    cd - > /dev/null
    run_language_test "C#" "implementations/csharp" "dotnet run --configuration Release"
elif command -v mcs &> /dev/null; then
    # Use Mono compiler
    echo "Compiling C# with Mono..."
    cd implementations/csharp
    if mcs -optimize+ *.cs -out:RunTests.exe 2>/dev/null; then
        cd - > /dev/null
        run_language_test "C#" "implementations/csharp" "mono RunTests.exe"
    else
        echo -e "${RED}✗ C# compilation failed${NC}"
        echo "csharp,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR" >> "$OUTPUT_FILE"
        cd - > /dev/null
    fi
else
    echo -e "${RED}✗ C# compiler not found${NC}"
    echo "csharp,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR" >> "$OUTPUT_FILE"
fi

# TypeScript
echo -e "${YELLOW}=== Running TypeScript GA ===${NC}"
if command -v tsc &> /dev/null && command -v node &> /dev/null; then
    echo "Compiling TypeScript..."
    cd implementations/typescript
    tsc --target ES2020 --skipLibCheck *.ts 2>/dev/null
    cd - > /dev/null
    run_language_test "TypeScript" "implementations/typescript" "node run_tests.js"
else
    echo -e "${RED}✗ TypeScript/Node.js not found${NC}"
    echo "typescript,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR" >> "$OUTPUT_FILE"
fi

# Swift
echo -e "${YELLOW}=== Running Swift GA ===${NC}"
if command -v swiftc &> /dev/null; then
    echo "Compiling Swift..."
    cd implementations/swift
    if swiftc -O -whole-module-optimization -cross-module-optimization -o RunTests OneMaxGA.swift RunTests.swift 2>/dev/null; then
        cd - > /dev/null
        run_language_test "Swift" "implementations/swift" "./RunTests"
    else
        echo -e "${RED}✗ Swift compilation failed${NC}"
        echo "swift,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR" >> "$OUTPUT_FILE"
        cd - > /dev/null
    fi
else
    echo -e "${RED}✗ Swift compiler not found${NC}"
    echo "swift,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR" >> "$OUTPUT_FILE"
fi
cd - > /dev/null

echo
echo -e "${GREEN}=== Benchmark Complete! ===${NC}"
echo "Results saved to: $OUTPUT_FILE"
echo
echo "Next steps:"
echo "1. Run: python3 scripts/analyze_results.py"
echo "2. Check results/analysis/ for plots and summary"