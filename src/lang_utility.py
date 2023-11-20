"""
@author: Yonas Gebregziabher, CSCI 3725, M7: Poetry Slam

This class provides functionalities to do operations
at a sentence/word level. It enables searching for similar words
related to a word as well as finding rhymes, generating quality 
queries from detected objects and more.
"""

from typing import List
from language_tool_python import LanguageTool
import numpy as np
from nltk import pos_tag
import random
from Phyme import Phyme
import nltk
import re

PROXIMITY_DISTANCE = 3


class LanguageUtility:
    def __init__(self, glove_file_path: str =
                 "model/glove.6B.300d.txt") -> None:
        "Initializes the LanguageUtility class"
        self.lang_tool = LanguageTool("en-US")
        print("Grammar checker is loaded!")
        self.glove_model = self.load_glove_model(glove_file_path)
        self.ph = Phyme()

    def load_glove_model(self,
                         glove_file_path: str) -> dict[str, List[float]]:
        """
        Loads the GloVe word embedding model and returns a dict with
        each word and their embeddings
        """
        print("Loading GloVe model!")
        f = open(glove_file_path, "r")
        glove_model = {}
        for line in f:
            split_line = line.split(" ")
            word = split_line[0]
            embedding = np.array([float(val) for val in split_line[1:]])
            glove_model[word] = embedding
        print(f"Glove mode loaded with {len(glove_model)} words!")
        return glove_model

    def find_closest_embeddings(self, word_embedding, k: int) -> List[str]:
        """
        Finds the closest K words that are semantically related to the
        given word embedding
        """
        if word_embedding is None:
            return []

        embedding_dot_product = np.dot(
            list(self.glove_model.values()), word_embedding)
        normalized = np.linalg.norm(
            list(self.glove_model.values()), axis=1) * \
            np.linalg.norm(word_embedding)
        similarities = embedding_dot_product / normalized
        top_k_similar_indices = np.argpartition(similarities, -k)[-k:]
        most_similar_k_words = [list(self.glove_model.keys())[
            i] for i in top_k_similar_indices]
        return most_similar_k_words

    def calculate_similarity(self, word1, word2):
        "Calculates the semantic similarity score between two words"
        if word1 in self.glove_model and word2 in self.glove_model:
            vector1 = self.glove_model[word1]
            vector2 = self.glove_model[word2]
            return np.dot(vector1, vector2) / (np.linalg.norm(vector1) *
                                               np.linalg.norm(vector2))
        else:
            return 0.0

    def find_rhyming_word(self, word, pos_tag_last, replacement_word: str,
                          used_rhymes: set[str]):
        """
        Finds a rhyming word that matches the POS tag and
        is semantically related to the word it is replacing that 
        has not yet been used. 
        """
        complete_rhymes = []
        try:
            complete_rhymes = self.ph.get_perfect_rhymes(
                word)
        except:
            return word
        perfect_rhymes = complete_rhymes.get(1)
        if perfect_rhymes is None:
            perfect_rhymes = []
            for key in complete_rhymes.keys():
                # in case no rhymes get alternative
                perfect_rhymes.extend(complete_rhymes[key])
        match_pos_unused = [rhyme for rhyme in perfect_rhymes if pos_tag([rhyme])[
            0][1] == pos_tag_last and word != rhyme and rhyme != replacement_word
            and rhyme not in used_rhymes]  # same pos thats a different word

        similarity_scores = [(similar_word, self.calculate_similarity(
            replacement_word, similar_word)) for similar_word in match_pos_unused]

        # Sort based on similarity scores
        sorted_words = sorted(
            similarity_scores, key=lambda x: x[1], reverse=True)
        if len(sorted_words) >= 1:
            random_top_5 = min(3, len(sorted_words))
            return random.choice(sorted_words[:random_top_5])[0]
        return word if len(perfect_rhymes) == 0 else random.choice(perfect_rhymes)

    def correct_grammar(self, sentence: str) -> str:
        "Corrects simple grammatical errors"
        return self.lang_tool.correct(sentence)

    def clean_word(self, word: str) -> str:
        "Removes the non alphabetical characters from a word"
        return re.sub('[^a-zA-Z]', '', word)

    def does_rhyme(self, word_1: str, word_2: str) -> bool:
        "Checks whether two words rhyme with each other"
        rhymes = self.ph.get_perfect_rhymes(word_1)
        result_list = set([rhyme for perfect_rhymes in rhymes.values()
                           for rhyme in perfect_rhymes])
        return word_2 in result_list

    def gen_quality_queries(self, detected_objects: List[str]) -> List[str]:
        """
        This sentences generates queries to fetch the highest
        quality lines possible through semantic search from pre-trained
        the universal basic encoder model
        """
        detected_objects_new = []
        for d in detected_objects:
            objc = d.split(" ")
            # non singular word objects, e.g "traffic lights"
            detected_objects_new.extend(objc)
        complete_queries = []
        for obj in detected_objects_new:
            word_embedding = self.glove_model.get(obj)
            synonyms = self.find_closest_embeddings(
                word_embedding, 5)
            complete_queries.append(" ".join(synonyms))
        return complete_queries

    def get_best_replacement(self, words_list: List[str], word: str) -> str:
        "Gets a random valid replacement for all words in a list"
        random.shuffle(words_list)
        for w in words_list:
            if w.isalpha() and w.lower() in self.glove_model and w != word:
                return w
        return word

    def modify_sentence(self, poem_line: str, rhyme_pattern: str, used_rhymes: set[str] = set()) -> str:
        """
        Modifies each word in the sentence by replacing each
        word in the line by a semantically related word
        that is the same POS and rhyme
        """
        if poem_line == "":
            return ""
        line_pos_tags = pos_tag(nltk.word_tokenize(poem_line))
        last_word = line_pos_tags[-1][0]

        if rhyme_pattern:
            line_pos_tags = line_pos_tags[:-1]

        modified_line = []
        for word in line_pos_tags:
            if not word[0].isalpha():
                continue
            clean_word = self.clean_word(word[0])
            word_embedding = self.glove_model.get(clean_word)
            word_pos_tag = word[1]
            if word_embedding is None:
                modified_line.append(clean_word)   # re-use the word
                continue
            sim_words = self.find_closest_embeddings(
                word_embedding, PROXIMITY_DISTANCE)
            matching_pos = [match for match in sim_words
                            if word_pos_tag == pos_tag([match])[
                                0][1]]  # replacement that matches same POS
            if len(matching_pos) >= 1:
                best_choice = self.get_best_replacement(
                    matching_pos, clean_word)
                modified_line.append(best_choice)
            else:
                modified_line.append(clean_word)

        changed_line = self.correct_grammar(" ".join(modified_line))

        # rhyme pattern
        if rhyme_pattern is not None:
            rhyme_pattern_pos_tag = pos_tag([rhyme_pattern])[0][1]
            rhyme_match = self.find_rhyming_word(
                rhyme_pattern, rhyme_pattern_pos_tag, last_word, used_rhymes)
            changed_line += f" {rhyme_match}"
        return changed_line
