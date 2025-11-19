#!/usr/bin/env python3
"""
Results Analysis Script for Genetic Algorithm Performance Comparison
Author: Genetic Algorithm Performance Comparison Project
Date: November 19, 2025

This script processes the benchmark results and creates visualizations and statistical summaries.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
from scipy import stats

# Set up paths
PROJECT_ROOT = Path(__file__).parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"
RAW_DATA_DIR = RESULTS_DIR / "raw_data"
ANALYSIS_DIR = RESULTS_DIR / "analysis"

# Create analysis directory if it doesn't exist
ANALYSIS_DIR.mkdir(exist_ok=True)

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_and_clean_data():
    """Load the CSV data and clean it."""
    csv_file = RAW_DATA_DIR / "benchmark_results.csv"
    
    if not csv_file.exists():
        print(f"Error: Results file not found at {csv_file}")
        print("Please run the benchmark first: ./scripts/run_all_tests.sh")
        sys.exit(1)
    
    # Load data
    df = pd.read_csv(csv_file)
    
    # Convert run columns to numeric, replacing 'ERROR' with NaN
    run_columns = [f'run{i}' for i in range(1, 26)]
    for col in run_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove languages with all errors
    df_clean = df.dropna(subset=run_columns, how='all').copy()
    
    if df_clean.empty:
        print("Error: No valid data found in results file.")
        sys.exit(1)
    
    return df_clean, run_columns

def calculate_statistics(df, run_columns):
    """Calculate statistical summaries for each language."""
    stats_data = []
    
    for _, row in df.iterrows():
        language = row['language']
        times = row[run_columns].dropna().values
        
        if len(times) == 0:
            continue
            
        stats_dict = {
            'Language': language,
            'Mean (ms)': np.mean(times),
            'Std Dev (ms)': np.std(times, ddof=1),
            'Median (ms)': np.median(times),
            'Min (ms)': np.min(times),
            'Max (ms)': np.max(times),
            'Valid Runs': len(times),
            'CV (%)': (np.std(times, ddof=1) / np.mean(times)) * 100
        }
        
        # Calculate 95% confidence interval
        if len(times) > 1:
            ci = stats.t.interval(0.95, len(times)-1, loc=np.mean(times), 
                                scale=stats.sem(times))
            stats_dict['CI Lower (ms)'] = ci[0]
            stats_dict['CI Upper (ms)'] = ci[1]
            stats_dict['CI Width (ms)'] = ci[1] - ci[0]
        else:
            stats_dict['CI Lower (ms)'] = stats_dict['Mean (ms)']
            stats_dict['CI Upper (ms)'] = stats_dict['Mean (ms)']
            stats_dict['CI Width (ms)'] = 0
        
        stats_data.append(stats_dict)
    
    return pd.DataFrame(stats_data)

def create_performance_plot(df, run_columns, stats_df):
    """Create a performance comparison plot."""
    # Prepare data for plotting
    plot_data = []
    for _, row in df.iterrows():
        language = row['language']
        times = row[run_columns].dropna().values
        for time in times:
            plot_data.append({'Language': language, 'Time (ms)': time})
    
    plot_df = pd.DataFrame(plot_data)
    
    if plot_df.empty:
        print("Warning: No data available for plotting")
        return
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Subplot 1: Box plot with individual points
    sns.boxplot(data=plot_df, x='Language', y='Time (ms)', ax=ax1)
    sns.stripplot(data=plot_df, x='Language', y='Time (ms)', 
                  alpha=0.6, size=4, ax=ax1)
    ax1.set_title('Execution Time Distribution by Language', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Programming Language', fontsize=12)
    ax1.set_ylabel('Execution Time (milliseconds)', fontsize=12)
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3)
    
    # Subplot 2: Bar plot with error bars (mean ± 95% CI)
    means = stats_df['Mean (ms)'].values
    ci_widths = stats_df['CI Width (ms)'].values / 2  # Half width for ± error bars
    languages = stats_df['Language'].values
    
    bars = ax2.bar(languages, means, yerr=ci_widths, capsize=5, 
                   alpha=0.7, edgecolor='black', linewidth=1)
    
    # Color bars by performance (fastest = green, slowest = red)
    sorted_indices = np.argsort(means)
    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(means)))
    for i, bar in enumerate(bars):
        bar.set_color(colors[np.where(sorted_indices == i)[0][0]])
    
    ax2.set_title('Mean Execution Time with 95% Confidence Intervals', 
                  fontsize=14, fontweight='bold')
    ax2.set_xlabel('Programming Language', fontsize=12)
    ax2.set_ylabel('Mean Execution Time (milliseconds)', fontsize=12)
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, mean, ci) in enumerate(zip(bars, means, ci_widths)):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + ci + max(means)*0.02,
                f'{mean:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # Save plot
    plot_file = ANALYSIS_DIR / "performance_comparison.png"
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"Performance plot saved to: {plot_file}")
    
    return fig

def create_ranking_analysis(stats_df):
    """Create a performance ranking analysis."""
    # Sort by mean execution time
    ranking_df = stats_df.sort_values('Mean (ms)').reset_index(drop=True)
    ranking_df['Rank'] = range(1, len(ranking_df) + 1)
    
    # Calculate relative performance (fastest = 1.0x)
    fastest_time = ranking_df['Mean (ms)'].iloc[0]
    ranking_df['Relative Speed'] = ranking_df['Mean (ms)'] / fastest_time
    ranking_df['Speed Factor'] = ranking_df['Relative Speed'].apply(lambda x: f"{x:.2f}x")
    
    return ranking_df

def generate_summary_report(stats_df, ranking_df):
    """Generate a comprehensive text summary."""
    report = []
    report.append("GENETIC ALGORITHM PERFORMANCE COMPARISON SUMMARY")
    report.append("=" * 60)
    report.append("")
    
    # Overview
    report.append("OVERVIEW:")
    report.append(f"• Languages tested: {len(stats_df)}")
    report.append(f"• Runs per language: 25 (target)")
    report.append(f"• Algorithm: One-Max Problem Genetic Algorithm")
    report.append(f"• Problem size: 100-bit binary strings")
    report.append("")
    
    # Performance ranking
    report.append("PERFORMANCE RANKING (by mean execution time):")
    report.append("-" * 50)
    for i, row in ranking_df.iterrows():
        valid_runs = row['Valid Runs']
        status = "✓" if valid_runs == 25 else f"⚠ ({valid_runs}/25)"
        report.append(f"{row['Rank']:2d}. {row['Language']:<12} "
                     f"{row['Mean (ms)']:8.2f} ms  "
                     f"({row['Speed Factor']:>6}) {status}")
    
    report.append("")
    
    # Statistical insights
    report.append("STATISTICAL INSIGHTS:")
    report.append("-" * 30)
    
    # Fastest and slowest
    fastest = ranking_df.iloc[0]
    slowest = ranking_df.iloc[-1]
    speedup = slowest['Mean (ms)'] / fastest['Mean (ms)']
    
    report.append(f"• Fastest: {fastest['Language']} ({fastest['Mean (ms)']:.2f} ms)")
    report.append(f"• Slowest: {slowest['Language']} ({slowest['Mean (ms)']:.2f} ms)")
    report.append(f"• Speed difference: {speedup:.2f}x")
    report.append("")
    
    # Variability analysis
    most_consistent = stats_df.loc[stats_df['CV (%)'].idxmin()]
    least_consistent = stats_df.loc[stats_df['CV (%)'].idxmax()]
    
    report.append(f"• Most consistent: {most_consistent['Language']} "
                 f"(CV: {most_consistent['CV (%)']:.2f}%)")
    report.append(f"• Least consistent: {least_consistent['Language']} "
                 f"(CV: {least_consistent['CV (%)']:.2f}%)")
    report.append("")
    
    # Language paradigm analysis
    report.append("LANGUAGE PARADIGM ANALYSIS:")
    report.append("-" * 35)
    
    # Categorize languages (simplified)
    categories = {
        'Compiled Systems': ['swift', 'java', 'csharp'],
        'Functional': ['fsharp', 'clojure'],
        'Scientific/Dynamic': ['julia', 'python'],
        'Web/Scripting': ['typescript']
    }
    
    for category, langs in categories.items():
        category_langs = ranking_df[ranking_df['Language'].isin(langs)]
        if not category_langs.empty:
            avg_time = category_langs['Mean (ms)'].mean()
            report.append(f"• {category}: {avg_time:.2f} ms average")
    
    report.append("")
    report.append("DETAILED STATISTICS:")
    report.append("-" * 25)
    
    # Format detailed table
    for _, row in ranking_df.iterrows():
        report.append(f"{row['Language'].upper()}:")
        report.append(f"  Mean: {row['Mean (ms)']:8.2f} ms")
        report.append(f"  Std:  {row['Std Dev (ms)']:8.2f} ms")
        report.append(f"  95% CI: [{row['CI Lower (ms)']:6.2f}, {row['CI Upper (ms)']:6.2f}] ms")
        report.append(f"  Range: [{row['Min (ms)']:6.2f}, {row['Max (ms)']:6.2f}] ms")
        report.append(f"  Runs: {row['Valid Runs']:2d}/25")
        report.append("")
    
    return "\n".join(report)

def main():
    """Main analysis function."""
    print("Starting Genetic Algorithm Performance Analysis...")
    print("-" * 50)
    
    # Load and process data
    print("Loading benchmark data...")
    df, run_columns = load_and_clean_data()
    print(f"Loaded data for {len(df)} languages")
    
    # Calculate statistics
    print("Calculating statistics...")
    stats_df = calculate_statistics(df, run_columns)
    
    if stats_df.empty:
        print("Error: No valid statistical data found.")
        sys.exit(1)
    
    # Create ranking analysis
    ranking_df = create_ranking_analysis(stats_df)
    
    # Create visualizations
    print("Creating performance plots...")
    create_performance_plot(df, run_columns, stats_df)
    
    # Generate summary report
    print("Generating summary report...")
    summary_report = generate_summary_report(stats_df, ranking_df)
    
    # Save detailed statistics
    stats_file = ANALYSIS_DIR / "detailed_statistics.csv"
    ranking_df.to_csv(stats_file, index=False)
    print(f"Detailed statistics saved to: {stats_file}")
    
    # Save summary report
    report_file = ANALYSIS_DIR / "performance_summary.txt"
    with open(report_file, 'w') as f:
        f.write(summary_report)
    print(f"Summary report saved to: {report_file}")
    
    # Display summary to console
    print("\n" + summary_report)
    
    print("\n" + "=" * 60)
    print("Analysis complete! Check the results/analysis/ directory for:")
    print("• performance_comparison.png - Visual comparison chart")
    print("• detailed_statistics.csv - Complete statistical data")
    print("• performance_summary.txt - Text summary report")

if __name__ == "__main__":
    main()