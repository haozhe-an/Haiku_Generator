import requests
import sys
from bs4 import BeautifulSoup

def count_word_syllables(word):
    word = word.lower()
    # Count the syllables in the word.
    syllables = 0
    for i in range(len(word)) :
    # If the first letter in the word is a vowel then it is a syllable.
        if i == 0 and word[i] in "aeiouy" :
            syllables = syllables + 1
    # Else if the previous letter is not a vowel.
        elif word[i - 1] not in "aeiouy" :
      # If it is no the last letter in the word and it is a vowel.
            if i < len(word) - 1 and word[i] in "aeiouy" :
                syllables = syllables + 1
      # Else if it is the last letter and it is a vowel that is not e.
            elif i == len(word) - 1 and word[i] in "aiouy" :
                syllables = syllables + 1
    # Adjust syllables from 0 to 1.
    if len(word) > 0 and syllables == 0 :
        syllables == 0
        syllables = 1
    return syllables


def count_syllables(sentence):
    words = sentence.split(' ')
    count = 0
    for w in words:
        count += count_word_syllables(w)
    return count

def main():
    phrase_length = len(sys.argv);
    phrase = ""
    for x in range(1,phrase_length):
        phrase += sys.argv[x]
        phrase += " "
    print(count_syllables(phrase))


if __name__ == "__main__":
    main()
