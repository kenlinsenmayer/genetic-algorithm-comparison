# Lines of Code vs Performance Analysis

## Methodology

Lines of code counted using automated script `count_loc.py` which:
- Excludes blank lines and whitespace-only lines
- Excludes all comment styles (`//`, `/* */`, `#`, `;;`, `(* *)`)
- Excludes documentation strings and blocks (`"""`, `@doc`, etc.)
- Counts only executable code lines
- Provides reproducible, language-aware parsing

Run `python3 count_loc.py` to verify these counts.

## Language Comparison Table

| Rank | Language   | Lines of Code | Mean Time (ms) | Relative Speed | Paradigm | Runtime/VM |
|------|------------|---------------|----------------|----------------|----------|------------|
| 1    | Julia      | 102           | 2.01          | 1.00x         | Scientific/Dynamic | JIT Native |
| 2    | Go         | 148           | 3.62          | 1.80x         | Systems/Imperative | Native GC |
| 3    | Java       | 125           | 3.67          | 1.83x         | OOP | JVM |
| 4    | F#         | 136           | 3.87          | 1.93x         | Functional | .NET |
| 5    | PyPy       | 73            | 4.68          | 2.33x         | Dynamic/Scripting | JIT Python |
| 6    | TypeScript | 91            | 5.49          | 2.73x         | Web/Scripting | V8 JavaScript |
| 7    | C#         | 126           | 9.00          | 4.48x         | OOP | .NET |
| 8    | Clojure    | 95            | 12.43         | 6.18x         | Functional Lisp | JVM |
| 9    | Swift      | 81            | 14.84         | 7.39x         | Systems/OOP | Native |
| 10   | Python     | 67            | 19.17         | 9.54x         | Dynamic/Scripting | Interpreted |
| 11   | Elixir     | 47            | 21.84         | 10.87x        | Functional/Concurrent | BEAM VM |