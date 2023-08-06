from sys import argv
from time import time
from src.test_kata_anagrams_weabreu.anagrams import (
    search_anagrams_v5, search_anagrams_v4, search_anagrams_v6, search_anagrams_v7
)

def main():
    file_path = argv[1]
    words = []
    
    with open(file_path, "r", encoding = "utf8") as fp:
        # words = fp.read().lower().splitlines()
        words = fp.read().splitlines()

    start_time = time()
    result, count, longest_word, most_words = search_anagrams_v7( words )
    end_time = time()

    for res in result:
        print(res)
    
    print(f"Set Counts: {len(result)}")
    print(f"Word Counts: {count}")
    print(f"Longest Word Set: {longest_word}")
    print(f"Most Words: {most_words}")
    print(f"Time: {end_time - start_time}")

    # finded_anagrams, word_counts = search_anagrams_v2( words )
    # for anagram_set in finded_anagrams:
    #     print(anagram_set)
    # print(f"Set Counts: {len(finded_anagrams)}")
    # print(f"Word Counts: {word_counts}")

if (__name__ == "__main__"):
    main()