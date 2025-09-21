"""
String Search Algorithms Comparison
Compares Boyer-Moore, KMP, and Rabin-Karp algorithms performance
"""

import timeit
import os


def boyer_moore_search(text, pattern):
    """Boyer-Moore algorithm (bad character heuristic only)"""
    def bad_char_table(pattern):
        table = {}
        for i in range(len(pattern)):
            table[pattern[i]] = i
        return table
    
    bad_char = bad_char_table(pattern)
    text_len = len(text)
    pattern_len = len(pattern)
    
    positions = []
    shift = 0
    
    while shift <= text_len - pattern_len:
        j = pattern_len - 1
        
        # Match pattern from right to left
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1
        
        if j < 0:
            # Pattern found
            positions.append(shift)
            # Shift for next search
            shift += pattern_len if shift + pattern_len < text_len else 1
        else:
            # Calculate shift using bad character heuristic
            bad_char_shift = j - bad_char.get(text[shift + j], -1)
            shift += max(1, bad_char_shift)
    
    return positions


def kmp_search(text, pattern):
    """Knuth-Morris-Pratt algorithm"""
    def compute_lps(pattern):
        """Compute longest proper prefix which is also suffix"""
        lps = [0] * len(pattern)
        length = 0
        i = 1
        
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    lps = compute_lps(pattern)
    positions = []
    i = j = 0
    
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == len(pattern):
            positions.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return positions


def rabin_karp_search(text, pattern):
    """Rabin-Karp algorithm"""
    BASE = 256
    PRIME = 101
    
    text_len = len(text)
    pattern_len = len(pattern)
    pattern_hash = 0
    text_hash = 0
    h = 1
    positions = []
    
    # Calculate h = pow(BASE, pattern_len-1) % PRIME
    for i in range(pattern_len - 1):
        h = (h * BASE) % PRIME
    
    # Calculate hash of pattern and first window of text
    for i in range(pattern_len):
        pattern_hash = (BASE * pattern_hash + ord(pattern[i])) % PRIME
        text_hash = (BASE * text_hash + ord(text[i])) % PRIME
    
    # Slide the pattern over text
    for i in range(text_len - pattern_len + 1):
        # Check if hash values match
        if pattern_hash == text_hash:
            # Check characters one by one (spurious hit verification)
            if text[i:i + pattern_len] == pattern:
                positions.append(i)
        
        # Calculate hash for next window
        if i < text_len - pattern_len:
            text_hash = (BASE * (text_hash - ord(text[i]) * h) + ord(text[i + pattern_len])) % PRIME
            if text_hash < 0:
                text_hash += PRIME
    
    return positions


def read_file(filename):
    """Read text file and return content"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {filename} not found")
        return ""


def measure_time(algorithm, text, pattern, number=1000):
    """Measure execution time of algorithm using timeit"""
    def wrapper():
        algorithm(text, pattern)
    
    time_taken = timeit.timeit(wrapper, number=number)
    return time_taken / number  # Average time per execution


def run_performance_test():
    """Run performance comparison of all three algorithms"""
    # Read article files
    article1_path = os.path.join("data", "article-1.txt")
    article2_path = os.path.join("data", "article-2.txt")
    
    article1 = read_file(article1_path)
    article2 = read_file(article2_path)
    
    if not article1 or not article2:
        return
    
    # Define test patterns
    # Existing patterns (found in texts)
    existing_patterns = [
        "алгоритм",           # Ukrainian: algorithm
        "структури даних",    # Ukrainian: data structures
        "пошук"              # Ukrainian: search
    ]
    
    # Non-existing patterns
    non_existing_patterns = [
        "quantum computing",
        "neural networks",
        "blockchain"
    ]
    
    algorithms = {
        "Boyer-Moore": boyer_moore_search,
        "KMP": kmp_search,
        "Rabin-Karp": rabin_karp_search
    }
    
    texts = {
        "Article 1": article1,
        "Article 2": article2
    }
    
    print("String Search Algorithms Performance Comparison")
    print("=" * 60)
    
    # Test with existing patterns
    print("\nTesting with EXISTING patterns:")
    for pattern in existing_patterns:
        print(f"\nPattern: '{pattern}'")
        print("-" * 40)
        
        for text_name, text in texts.items():
            print(f"\n{text_name}:")
            times = {}
            
            for alg_name, algorithm in algorithms.items():
                # First verify the pattern exists
                positions = algorithm(text, pattern)
                time_taken = measure_time(algorithm, text, pattern, 100)
                times[alg_name] = time_taken
                
                print(f"  {alg_name:12}: {time_taken*1000:.4f} ms (found {len(positions)} times)")
            
            # Find fastest algorithm for this text and pattern
            fastest = min(times.keys(), key=lambda x: times[x])
            print(f"  → Fastest: {fastest}")
    
    # Test with non-existing patterns
    print(f"\nTesting with NON-EXISTING patterns:")
    for pattern in non_existing_patterns:
        print(f"\nPattern: '{pattern}'")
        print("-" * 40)
        
        for text_name, text in texts.items():
            print(f"\n{text_name}:")
            times = {}
            
            for alg_name, algorithm in algorithms.items():
                time_taken = measure_time(algorithm, text, pattern, 100)
                times[alg_name] = time_taken
                
                print(f"  {alg_name:12}: {time_taken*1000:.4f} ms")
            
            # Find fastest algorithm for this text and pattern
            fastest = min(times.keys(), key=lambda x: times[x])
            print(f"  → Fastest: {fastest}")
    
    # Overall analysis
    print(f"\nOVERALL ANALYSIS:")
    print("-" * 40)
    
    # Test all patterns on both texts to get overall performance
    all_times = {alg: [] for alg in algorithms.keys()}
    
    for text in texts.values():
        for pattern in existing_patterns + non_existing_patterns:
            for alg_name, algorithm in algorithms.items():
                time_taken = measure_time(algorithm, text, pattern, 50)
                all_times[alg_name].append(time_taken)
    
    # Calculate average times
    avg_times = {}
    for alg_name, times_list in all_times.items():
        avg_times[alg_name] = sum(times_list) / len(times_list)
        print(f"{alg_name:12}: {avg_times[alg_name]*1000:.4f} ms average")
    
    overall_fastest = min(avg_times.keys(), key=lambda x: avg_times[x])
    print(f"\nOverall fastest algorithm: {overall_fastest}")


if __name__ == "__main__":
    run_performance_test()