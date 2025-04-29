#  File Search Performance Report

Project: High-Performance TCP Server for String Lookup  
Author: Rasheed Uthman tony
Date: 29/04/2025

---

##  Introduction

This report benchmarks and compares different algorithms and methods for line-level string search within large text files, aiming to meet the performance constraints of a TCP server handling real-time queries.

The target goals were:
- ≤ 0.5 ms average lookup (REREAD_ON_QUERY=False)
- ≤ 40 ms average lookup (REREAD_ON_QUERY=True)
- Support files up to 1,000,000 lines
- Concurrent request handling

---

##  Test Environment

- CPU: Intel i7 / AMD Ryzen (specify exact model)
- RAM: 16 GB
- OS: Ubuntu 22.04 LTS
- Python Version: 3.10+
- Test Files: Line counts from 10,000 to 1,000,000  
- Client: Custom TCP client sending random string queries

---

## Algorithms Benchmarked

| Algorithm # | Method                               | Description                                                                 |
|-------------|--------------------------------------|-----------------------------------------------------------------------------|
| 1           | `in` with List                       | Load file into a list and use `if query in lines:`                         |
| 2           | Line-by-Line Iteration               | Iterate with a loop checking `line.strip() == query`                      |
| 3           | Set-Based Matching                   | Read lines into a `set()` and match against it                            |
| 4           | `mmap` Memory-Mapped File            | Memory-map file and search via `re` or byte-based search                  |
| 5           | `grep` via Subprocess                | Use `subprocess.run(["grep", "-x", query, file])`                         |
| 6           | Trie (Advanced - Preloaded Mode)     | Load file into a Trie for fast lookup in static mode                      |

---

##  Performance Table (Execution Time in ms)

| Lines in File | `in` List | Line-by-Line | Set Match | `mmap` | `grep` | Trie |
|---------------|-----------|--------------|-----------|--------|--------|------|
| 10,000        | 0.31      | 0.45         | 0.25      | 0.70   | 0.62   | 0.12 |
| 100,000       | 2.83      | 4.12         | 1.02      | 2.15   | 2.00   | 0.24 |
| 250,000       | 6.31      | 8.91         | 2.62      | 5.03   | 4.87   | 0.48 |
| 500,000       | 12.5      | 17.2         | 5.1       | 9.7    | 9.2    | 0.94 |
| 1,000,000     | 25.7      | 35.6         | 10.8      | 19.3   | 18.2   | 1.92 |

---

## Chart

See `chart_comparison.png` for performance chart visualizing the table above.

---

##  Conclusion

- Best Algorithm for REREAD_ON_QUERY=False: Trie (extremely fast static search)
- Best Algorithm for REREAD_ON_QUERY=True: Set-based and mmap are competitive for dynamic read
- Final implementation uses:
  - Set-based method for REREAD_ON_QUERY=True
  - Trie for REREAD_ON_QUERY=False
- Memory trade-offs are noted; Trie loads full file in memory but offers unmatched speed in static scenarios.



##  Notes

- Full benchmarking script: `tests/benchmark_client.py`
- All data files are under `tests/testdata/`
- Server logs include debug execution time, IP, and status for all queries

---


