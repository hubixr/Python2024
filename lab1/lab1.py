import rich
from rich.progress import track
import rich.traceback
#Progress bar
import tqdm
import time
import random
#do zliczania
import re
from collections import Counter

# Wczytywanie argumentów 
import sys
import argparse

# Wykres w konsoli
from ascii_graph import Pyasciigraph
from ascii_graph import colors

import collections
from _collections_abc import Iterable 
collections.Iterable = Iterable

#import pliku
import os


rich.traceback.install()

#Loading txt file
def load_text(file_name):
    text = []
    try:
        # Otwórz plik i wczytaj zawartość
        with open(file_name, 'r', encoding='utf-8') as file:
            text.append(file.read())
            #print(text)
    except FileNotFoundError:
        print(f"Plik '{file_name}' nie został znaleziony.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    return text

# Wczytywanie argumentów z konsoli
def parser_arguments():
    parser = argparse.ArgumentParser(description='Generate histogram from txt file')
    parser.add_argument('filename', help='Filename to analyze')
    parser.add_argument('--limit', '-l', type=int, default=10, help='Limit the number of words to display')
    parser.add_argument('--min', '-m',type=int, help='Minimum word length')
    parser.add_argument('--ignore', '-i', nargs='*', type=str, help='List of ingrored words')
    parser.add_argument("--must-include", '-mi', nargs="*", help="Words must include these characters.")
    parser.add_argument("--must-exclude", '-me', nargs="*", help="Words must not include these characters.")
    args = parser.parse_args()
    return args

#wyświetlanie argumentów
def display_parser_arguments(args):
    print(args)
    print("nazwa pliku: ",args.filename)

#Zliczanie słów
def count_words(texts, min_length, ignore_words, must_include, must_exclude):
    words = []
    # Pasek postępu dla przetwarzania tekstów
    for text in tqdm.tqdm(texts, desc="Processing texts", unit="text"):
        for word in re.findall(r'\b\w+\b', text.lower()):
            if len(word) >= min_length and \
               (ignore_words is None or word not in ignore_words) and \
               (must_include is None or any(c in word for c in must_include)) and \
               (must_exclude is None or all(c not in word for c in must_exclude)):
                words.append(word)

    return Counter(words)

# Kolory do histogramu
def get_word_color(count, max_count):
    if count == max_count:
        return colors.BCya  # Najczęściej występujące słowo - kolor niebieski
    elif count > max_count * 0.75:
        return colors.BBlu  # Prawie najczęściej występujące słowo - kolor niebieski
    elif count > max_count * 0.5:
        return colors.BYel  # Średnia liczba wystąpień - kolor żółty
    elif count > max_count * 0.25:
        return colors.Gre  # Mniej popularne słowo - kolor zielony
    else:
        return colors.BRed  # Rzadkie słowo - kolor czerwony

# Histogram
def draw_histogram(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    # Maksymalna liczba słów w histogramie do generowania gradientu
    max_count = max(count for word, count in top_words)
    
    # Tworzenie danych z kolorami
    colored_data = [(word, count, get_word_color(count, max_count)) for word, count in top_words]

    # Tworzenie histogramu z kolorami
    graph = Pyasciigraph(line_length=75, separator_length=4)
    
    # Rysowanie histogramu z gradientem
    for line in graph.graph('Word Frequency', colored_data):
        print(line)


# Main
def main():
    args = parser_arguments()
    display_parser_arguments(args)
    text = load_text(args.filename)
    word_counts = count_words(text, args.min, args.ignore, args.must_include, args.must_exclude)
    draw_histogram(word_counts, args.limit)

if __name__ == "__main__":
    main()


# Komenda do konsoli : poetry run python lab1.py xd.txt -l 20 -m 5 -i myśli -mi o -me w