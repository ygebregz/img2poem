"""
This utility script file is responsible for preparing the Frank Ocean 
lyrics to be embedded by our model. 
"""
import re


def remove_duplicates(corpus):
    "Removes duplicate lines"
    unique_lines = set(corpus)
    return list(unique_lines)


def get_lyrics(file_path="data/frank_ocean_lyrics_clean.txt"):
    "Opens the clean file by default"
    with open(file_path, "r") as file:
        lyrics = file.readlines()
    return lyrics


def prep_data(k, corpus):
    "Keeps at least k length lines without parenthesis as part of dataset"
    clean_corpus = remove_duplicates(corpus)
    min_k_length_lines = []
    count = 0
    for line in clean_corpus:
        if len(line.split()) >= k:
            clean_text = re.sub(r'\([^)]*\)', '', line)
            min_k_length_lines.append(clean_text)
            print(f"Line {count} of {len(clean_corpus)}")
            count += 1

    with open("data/frank_ocean_lyrics_clean.txt", "w") as file:
        file.write("".join(min_k_length_lines))


lyrics = get_lyrics("data/frank_ocean_lyrics.txt")

#prep_data(4, lyrics)
