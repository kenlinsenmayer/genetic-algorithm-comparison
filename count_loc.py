#!/usr/bin/env python3
"""
Lines of Code Counter for Genetic Algorithm Implementations

This script counts executable lines of code for each language implementation,
excluding comments, documentation, and blank lines. The methodology is 
transparent and repeatable for validation purposes.

Usage: python3 count_loc.py
"""

import os
import re
from pathlib import Path


def count_executable_lines(file_path, language):
    """
    Count executable lines of code for a given file and language.
    
    Args:
        file_path (str): Path to the source file
        language (str): Programming language identifier
        
    Returns:
        int: Number of executable lines of code
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0
    
    executable_lines = 0
    in_multiline_comment = False
    in_docstring = False
    
    for line in lines:
        stripped = line.strip()
        
        # Skip completely blank lines
        if not stripped:
            continue
            
        # Handle multiline comments and docstrings by language
        if language in ['java', 'csharp', 'typescript', 'swift', 'go']:
            # Handle /* ... */ style comments
            if '/*' in stripped and '*/' in stripped:
                # Single line multiline comment
                before_comment = stripped.split('/*')[0].strip()
                if before_comment and not before_comment.startswith('//'):
                    executable_lines += 1
                continue
            elif '/*' in stripped:
                in_multiline_comment = True
                before_comment = stripped.split('/*')[0].strip()
                if before_comment and not before_comment.startswith('//'):
                    executable_lines += 1
                continue
            elif '*/' in stripped:
                in_multiline_comment = False
                continue
            elif in_multiline_comment:
                continue
            # Handle // style comments
            elif stripped.startswith('//') or stripped.startswith('*'):
                continue
                
        elif language in ['python', 'pypy']:
            # Handle Python docstrings and comments
            if '"""' in stripped:
                # Count occurrences of """
                count = stripped.count('"""')
                if count == 1:
                    if in_docstring:
                        in_docstring = False
                        continue
                    else:
                        in_docstring = True
                        # Check if there's code before the docstring
                        before_docstring = stripped.split('"""')[0].strip()
                        if before_docstring and not before_docstring.startswith('#'):
                            executable_lines += 1
                        continue
                elif count == 2:
                    # Single line docstring
                    before_docstring = stripped.split('"""')[0].strip()
                    if before_docstring and not before_docstring.startswith('#'):
                        executable_lines += 1
                    continue
            elif in_docstring:
                continue
            elif stripped.startswith('#'):
                continue
                
        elif language == 'julia':
            # Handle Julia comments
            if stripped.startswith('#'):
                continue
                
        elif language == 'clojure':
            # Handle Clojure comments
            if stripped.startswith(';;') or stripped.startswith(';'):
                continue
                
        elif language == 'fsharp':
            # Handle F# comments
            if stripped.startswith('//') or (in_multiline_comment and not '*/' in stripped):
                continue
            elif '(*' in stripped and '*)' in stripped:
                # Single line multiline comment
                before_comment = stripped.split('(*')[0].strip()
                if before_comment:
                    executable_lines += 1
                continue
            elif '(*' in stripped:
                in_multiline_comment = True
                before_comment = stripped.split('(*')[0].strip()
                if before_comment:
                    executable_lines += 1
                continue
            elif '*)' in stripped:
                in_multiline_comment = False
                continue
                
        elif language == 'elixir':
            # Handle Elixir comments and documentation
            if stripped.startswith('#') or stripped.startswith('@doc') or stripped.startswith('@moduledoc'):
                continue
            # Handle standalone """ lines (part of @doc/@moduledoc blocks)
            if stripped == '"""':
                continue
            # Handle multiline strings for other cases
            if '"""' in stripped and not (stripped.startswith('@doc') or stripped.startswith('@moduledoc')):
                count = stripped.count('"""')
                if count == 1:
                    if in_docstring:
                        in_docstring = False
                        continue
                    else:
                        in_docstring = True
                        before_docstring = stripped.split('"""')[0].strip()
                        if before_docstring and not before_docstring.startswith('#'):
                            executable_lines += 1
                        continue
                elif count == 2:
                    before_docstring = stripped.split('"""')[0].strip()
                    if before_docstring and not before_docstring.startswith('#'):
                        executable_lines += 1
                    continue
            elif in_docstring:
                continue
        
        # If we get here, it's an executable line
        executable_lines += 1
    
    return executable_lines


def analyze_implementations():
    """
    Analyze all language implementations and count lines of code.
    
    Returns:
        dict: Dictionary mapping language names to LOC counts
    """
    base_path = Path(__file__).parent / 'implementations'
    results = {}
    
    # Language configurations: (directory, file_patterns, language_key)
    language_configs = [
        ('julia', ['*.jl'], 'julia'),
        ('python', ['onemax_ga.py'], 'python'),
        ('python', ['onemax_ga_pypy.py'], 'pypy'),
        ('fsharp', ['*.fs'], 'fsharp'),
        ('java', ['*.java'], 'java'),
        ('clojure', ['*.clj'], 'clojure'),
        ('csharp', ['*.cs'], 'csharp'),
        ('typescript', ['*.ts'], 'typescript'),
        ('swift', ['*.swift'], 'swift'),
        ('elixir', ['*.ex'], 'elixir'),
        ('go', ['*.go'], 'go'),
    ]
    
    for directory, patterns, lang_key in language_configs:
        lang_path = base_path / directory
        if not lang_path.exists():
            print(f"Warning: Directory {lang_path} not found")
            continue
            
        total_loc = 0
        files_found = []
        
        for pattern in patterns:
            files = list(lang_path.glob(pattern))
            for file_path in files:
                # Skip test files and generated files
                if any(skip in file_path.name.lower() for skip in ['test', 'spec', '.js']):
                    if not (lang_key == 'typescript' and file_path.name == 'run_tests.js'):
                        continue
                
                loc = count_executable_lines(file_path, lang_key)
                total_loc += loc
                files_found.append((file_path.name, loc))
                
        if files_found:
            results[lang_key] = {
                'total_loc': total_loc,
                'files': files_found,
                'directory': directory
            }
            
    return results


def print_results(results):
    """Print the LOC analysis results in a formatted table."""
    print("=" * 70)
    print("LINES OF CODE ANALYSIS - GENETIC ALGORITHM IMPLEMENTATIONS")
    print("=" * 70)
    print("Methodology: Count only executable lines, excluding:")
    print("  • Blank lines")
    print("  • Comments (// /* */ # ;; (* *) etc.)")
    print("  • Documentation strings and blocks")
    print("  • Pure whitespace")
    print("=" * 70)
    
    # Sort by total LOC for consistent output
    sorted_results = sorted(results.items(), key=lambda x: x[1]['total_loc'])
    
    print(f"{'Language':<12} {'LOC':<6} {'Files':<30}")
    print("-" * 70)
    
    for lang, data in sorted_results:
        files_info = ', '.join([f"{name}({loc})" for name, loc in data['files']])
        print(f"{lang.capitalize():<12} {data['total_loc']:<6} {files_info}")
    
    print("-" * 70)
    print(f"Total languages analyzed: {len(results)}")
    print(f"Total lines of executable code: {sum(data['total_loc'] for data in results.values())}")


def generate_csv_output(results):
    """Generate CSV output for integration with other analyses."""
    print("\n" + "=" * 50)
    print("CSV FORMAT OUTPUT:")
    print("=" * 50)
    print("language,lines_of_code")
    
    # Sort by language name for consistent output
    for lang in sorted(results.keys()):
        print(f"{lang},{results[lang]['total_loc']}")


def main():
    """Main execution function."""
    print("Lines of Code Counter for Genetic Algorithm Implementations")
    print("Analyzing implementations directory...\n")
    
    results = analyze_implementations()
    
    if not results:
        print("No implementations found. Make sure you're running this from the project root.")
        return
    
    print_results(results)
    generate_csv_output(results)
    
    print(f"\n{'='*50}")
    print("Analysis complete. Results show only executable code lines.")
    print("This script provides a reproducible methodology for LOC counting.")


if __name__ == '__main__':
    main()