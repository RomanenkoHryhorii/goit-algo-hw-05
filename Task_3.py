import timeit
import re
from typing import Callable


# Реалізація алгоритму Боєра-Мура
def boyer_moore(text: str, pattern: str) -> int:
    m, n = len(pattern), len(text)
    if m == 0: return 0
    last_occurrence = {c: -1 for c in set(text)}
    for i in range(m):
        last_occurrence[pattern[i]] = i

    s = 0  # Поточний зсув
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s  # Знайдено
        else:
            s += max(1, j - last_occurrence.get(text[s + j], -1))
    return -1  # Не знайдено


# Реалізація алгоритму Кнута-Морріса-Пратта
def kmp(text: str, pattern: str) -> int:
    def compute_lps(pattern: str):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
        return lps

    lps = compute_lps(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j  # Знайдено
        elif i < len(text) and pattern[j] != text[i]:
            j = lps[j - 1] if j != 0 else 0
    return -1  # Не знайдено


# Реалізація алгоритму Рабіна-Карпа
def rabin_karp(text: str, pattern: str, q=101) -> int:
    d = 256
    m, n = len(pattern), len(text)
    if m > n:
        return -1

    p = t = 0
    h = 1
    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i  # Знайдено
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q
    return -1  # Не знайдено


# Завантаження текстових файлів
with open("стаття 1.txt", encoding="utf-8") as f1:
    text1 = f1.read()
with open("стаття 2 (1).txt", encoding="utf-8") as f2:
    text2 = f2.read()

# Вибір підрядків
existing_substring = "алгоритм"  # Є в текстах
nonexistent_substring = "вигаданий_підрядок"  # Вигаданий

# Замір часу виконання
def measure_time(func: Callable, text: str, pattern: str) -> float:
    return timeit.timeit(lambda: func(text, pattern), number=1)

algorithms = {
    "Boyer-Moore": boyer_moore,
    "Knuth-Morris-Pratt": kmp,
    "Rabin-Karp": rabin_karp,
}

results = {alg: {} for alg in algorithms}

for alg_name, alg_func in algorithms.items():
    results[alg_name]["text1_existing"] = measure_time(alg_func, text1, existing_substring)
    results[alg_name]["text1_nonexistent"] = measure_time(alg_func, text1, nonexistent_substring)
    results[alg_name]["text2_existing"] = measure_time(alg_func, text2, existing_substring)
    results[alg_name]["text2_nonexistent"] = measure_time(alg_func, text2, nonexistent_substring)

# Аналіз результатів
overall_fastest = min(results, key=lambda alg: sum(results[alg].values()))
fastest_per_text = {
    "text1": min(algorithms, key=lambda alg: results[alg]["text1_existing"] + results[alg]["text1_nonexistent"]),
    "text2": min(algorithms, key=lambda alg: results[alg]["text2_existing"] + results[alg]["text2_nonexistent"]),
}

