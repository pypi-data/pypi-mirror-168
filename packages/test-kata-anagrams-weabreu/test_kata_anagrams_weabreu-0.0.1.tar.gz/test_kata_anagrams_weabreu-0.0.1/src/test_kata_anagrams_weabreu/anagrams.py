
def get_words_char_count(words_list: list[str]) -> dict[str, dict[str, int]]:
    
    words_char_count = { word: {char: word.count(char) for char in word} for word in words_list }

    return words_char_count

def search_anagrams(words_list: list[str]) -> tuple[str, int]:
    words_char_count = get_words_char_count( words_list )

    anagrams_list = []
    words_count = 0
    anagrams = ""

    for word in list(words_char_count):
        if not words_char_count.__contains__(word):
            continue

        current_word_chars = words_char_count[word]
        words_char_count.pop(word)
        
        anagrams = word
        current_words_count = 1

        for other_word in list(words_char_count):
            if current_word_chars == words_char_count[other_word]:
                anagrams += f" {other_word}"
                words_char_count.pop(other_word)
                current_words_count += 1
        
        if (anagrams != word):
            anagrams_list.append(anagrams)
            words_count += current_words_count

        anagrams = ""
    
    return (anagrams_list, words_count)

# Does not word
def search_anagrams_v2(words_list: list[str]) -> tuple[str, int]:

    anagrams_list = []
    anagrams_finded = 0
    anagrams = ""
    
    for word in words_list:
        anagrams = word
        current_anagrams_finded = 1
        word_chars = {char: word.count(char) for char in word}

        for other_word_index in range(0, len(words_list)):
            other_word = words_list[other_word_index]
            other_word_chars = {char: other_word.count(char) for char in other_word}

            if word_chars == other_word_chars:
                anagrams += f" {other_word}"
                current_anagrams_finded += 1
                words_list.pop(other_word_index)

        if (current_anagrams_finded > 1):
            anagrams_list.append( anagrams )
            anagrams_finded += current_anagrams_finded
        
        words_list.pop(0)

    return (anagrams_list, anagrams_finded)

# Does not word
def search_anagrams_v3(words_list: list[str]) -> tuple[str, int]:

    anagrams_dict: dict[dict[str, int], str] = {}

    for word in words_list:
        word_chars = {char: word.count(char) for char in word}

        if anagrams_dict[word_chars]:
            anagrams_dict[word_chars] += f" {word}"
        else:
            anagrams_dict[word_chars] = word

    return anagrams_dict

# def search_anagrams_v4(words_list: list[str]) -> tuple[str, int]:

#     anagrams_dict: dict = {}

#     for word in words_list:
#         word_chars = {char: word.count(char) for char in word}
#         key = tuple(sorted(frozenset(word_chars.items())))

#         if anagrams_dict.__contains__(key):
#             anagrams_dict[key] += f" {word}"
#         else:
#             anagrams_dict[key] = word

#     return [val for val in anagrams_dict.values() if val.__contains__(" ")]

def search_anagrams_v4(words_list: list[str]) -> tuple[str, int]:

    anagrams_dict: dict = {}

    for word in words_list:
        word_chars = {char: word.count(char) for char in word}
        key = tuple(sorted(frozenset(word_chars.items())))

        if anagrams_dict.__contains__(key):
            anagrams_dict[key]["set"] += f" {word}"
            anagrams_dict[key]["count"] += 1
        else:
            anagrams_dict[key] = {"set": word, "count": 1}

    return [val["set"] for val in anagrams_dict.values() if val["count"] > 1]

def search_anagrams_v5(words_list: list[str]) -> tuple[str, int]:

    anagrams_dict: dict[str, list] = {}

    for word in words_list:
        word_chars = "".join(sorted(list(word)))

        if not anagrams_dict.__contains__(word_chars):
            anagrams_dict[word_chars] = []
        
        anagrams_dict[word_chars].append(word)

    count = 0
    for k, v in anagrams_dict.items():
        if len(v) > 1:
            count += 1
    
    return count

# def search_anagrams_v6(words_list: list[str]) -> tuple[str, int]:

#     anagrams_dict: dict[str, dict] = {}
#     anagrams_count: int = 0

#     for word in words_list:
#         anagram_letters: str = "".join(sorted(list(word)))

#         if anagrams_dict.__contains__(anagram_letters):
#             anagrams_dict[anagram_letters] += f" {word}"
            
#             if anagrams_dict[anagram_letters].count(" ") == 1:
#                 anagrams_count += 2
#             else: anagrams_count += 1
#         else:
#             anagrams_dict[anagram_letters] = word

#     return ([val for val in anagrams_dict.values() if val.__contains__(" ")], anagrams_count)

def search_anagrams_v6(words_list: list[str]) -> tuple[str, int]:

    anagrams_dict: dict[str, dict] = {}

    for word in words_list:
        anagram_letters: str = "".join(sorted(word))

        if anagrams_dict.__contains__(anagram_letters):
            anagrams_dict[anagram_letters]["set"] += f" {word}"
            anagrams_dict[anagram_letters]["count"] += 1
        else:
            anagrams_dict[anagram_letters] = { "set": word, "count": 1 }

    return (
        [val["set"] for val in anagrams_dict.values() if val["count"] > 1], 
        sum([val["count"] for val in anagrams_dict.values() if val["count"] > 1])
    )

def search_anagrams_v7(words_list: list[str]) -> tuple[list[str], int, str, str]:

    anagrams_dict: dict[str, dict] = {}
    longest_word = ""
    most_words = ""

    for word in words_list:
        anagram_letters: str = "".join(sorted(word))

        if anagrams_dict.__contains__(anagram_letters):
            anagrams_dict[anagram_letters]["set"] += f" {word}"
            anagrams_dict[anagram_letters]["count"] += 1

            if len(anagram_letters) > len(longest_word):
                longest_word = anagram_letters
        else:
            anagrams_dict[anagram_letters] = { "set": word, "count": 1 }

    anagrams = [val for val in anagrams_dict.values() if val["count"] > 1]

    if (len(anagrams) > 0):
        most_words = max(anagrams, key=lambda dct: dct["count"])["set"]
        longest_word = anagrams_dict[longest_word]["set"]

    return (
        [val["set"] for val in anagrams], 
        sum([val["count"] for val in anagrams]),
        longest_word,
        most_words
    )

class AnagramsAnalyzer:
    def __init__(self, words_list: list[str]):
        self.anagrams: list[dict] = []
        self._longest_word_letters = ""
        self._anagrams_dict: dict[str, dict] = {}

        self.__search_anagrams( words_list )

    def __search_anagrams(self, words_list: list[str]) -> list[str]:
        for word in words_list:
            anagram_letters: str = "".join(sorted(word))

            if self._anagrams_dict.__contains__(anagram_letters):
                self._anagrams_dict[anagram_letters]["set"] += f" {word}"
                self._anagrams_dict[anagram_letters]["count"] += 1

                if len(anagram_letters) > len(self._longest_word_letters):
                    self._longest_word_letters = anagram_letters
            else:
                self._anagrams_dict[anagram_letters] = { "set": word, "count": 1 }

        self.anagrams = [val for val in self._anagrams_dict.values() if val["count"] > 1]

    def get_anagrams(self) -> list[str]:
        return [val["set"] for val in self.anagrams]
    
    def get_words_count(self) -> int:
        return sum([val["count"] for val in self.anagrams])

    def get_longest_word_set(self) -> str:
        if self._longest_word_letters == "":
            return ""

        return self._anagrams_dict[self._longest_word_letters]["set"]

    def get_most_words_set(self) -> str:
        if len(self.anagrams) <= 0:
            return ""
        
        return max(self.anagrams, key=lambda dct: dct["count"])["set"]
