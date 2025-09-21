# Woolf University. Basic Algorithms and Data Structures Course. Homework – Search Algorithms

## Overview

This assignment focuses on comparing the efficiency of three classic substring search algorithms: **Boyer–Moore**, **Knuth–Morris–Pratt (KMP)**, and **Rabin–Karp**. You will test them on two different text files and measure their performance using Python’s `timeit` module.

---

## Task – Substring Search Efficiency

### Description

* Implement or use implementations of the following substring search algorithms:

  * **Boyer–Moore**
  * **Knuth–Morris–Pratt (KMP)**
  * **Rabin–Karp**
* Prepare two text files as input data.
* Choose two substrings for testing:

  1. A substring that exists in the text.
  2. A substring that does not exist (fictional).
* Measure execution time for each algorithm and substring type using `timeit`.

### Requirements

1. Apply each algorithm to both text files.
2. Run tests for substrings that are present and absent.
3. Collect timing results and compare.
4. Identify:

   * The fastest algorithm for each file.
   * The overall best-performing algorithm.

### Evaluation Criteria

* Correct implementation of Boyer–Moore, KMP, and Rabin–Karp.
* Proper use of `timeit` for benchmarking.
* Clear results for both text files and both substring scenarios.
* Well-structured analysis and conclusions about efficiency.
