import requests

from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

import matplotlib.pyplot as plt


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(e)
        return None

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

def map_reduce(text):
    words = text.split()

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

def visualize_top_words(words_dict, n = 10):
    sorted_words = sorted(words_dict.items(), key=lambda x: x[1], reverse=True)[:n]

    words, frequencies = zip(*sorted_words)

    plt.figure(figsize=(10, 6))
    plt.barh(words, frequencies, color="skyblue")

    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title(f"Top {n} Most Frequent Words")
    plt.gca().invert_yaxis()

    plt.show()


if __name__ == '__main__':
    # Вхідний текст для обробки
    url = "https://gutenberg.net.au/ebooks03/0301261.txt"
    text = get_text(url)
    if text:
        result = map_reduce(text)
        visualize_top_words(result)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")