import requests
import re
import matplotlib.pyplot as plt
from collections import Counter
from multiprocessing import Pool, cpu_count


def fetch_text_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def map_function(text_chunk):
    words = re.findall(r'\b\w+\b', text_chunk.lower())
    return Counter(words)


def reduce_function(counters):
    total = Counter()
    for counter in counters:
        total.update(counter)
    return total


def split_text(text, num_chunks):
    length = len(text)
    chunk_size = length // num_chunks
    return [text[i*chunk_size: (i+1)*chunk_size] for i in range(num_chunks)]


def visualize_top_words(word_counts, top_n=10):
    most_common = word_counts.most_common(top_n)
    words, counts = zip(*most_common)
    plt.figure(figsize=(10, 6))
    plt.barh(words[::-1], counts[::-1], color='blue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(f"Top {top_n} Most Frequent Words")
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    url = "https://www.gutenberg.org/files/84/84-0.txt"
    text = fetch_text_from_url(url)

    num_cores = cpu_count()
    chunks = split_text(text, num_cores)

    with Pool(num_cores) as pool:
        mapped = pool.map(map_function, chunks)

    word_counts = reduce_function(mapped)

    visualize_top_words(word_counts, top_n=10)
