"""
@author: Yonas Gebregziabher, CSCI 3725, M7: Poetry Slam

This represents a Villanelle Poem object as well
the functionalities to generate stanzas and lines for
each stanzas.
"""
from typing import List
from .model import SemanticSearchModel
from .lang_utility import LanguageUtility
from .stanza import Stanza
from utils.data_cleaner import get_lyrics
import random
import re

SELECT_FROM_TOP_K = 2  # top k lyric matches to pick from


class VillanellePoem:

    def __init__(self, inspiring_object_queries: List[str], lang_utility: LanguageUtility,
                 smtic_model: SemanticSearchModel) -> None:
        "Initializes the VillanellePoem object"
        self.inspiring_object_queries = inspiring_object_queries
        self.lang_utility = lang_utility
        self.smtic_model = smtic_model
        self.stanzas: List[Stanza] = []
        self.A_PATTERN = None
        self.B_PATTERN = None
        self.inspiration_lyrics = set()
        self.used_rhymes = set()

    def get_inspiring_object_queries(self) -> List[str]:
        "Return the list of queries used to generate stanzas"
        return self.inspiring_object_queries

    def get_inspiration_lyrics(self) -> List[str]:
        "Return the list of lyrics used to generate lines"
        return self.inspiration_lyrics

    def add_stanza(self, stanza: Stanza) -> bool:
        "Adds a stanza to the list of stanzas"
        self.stanzas.append(stanza)

    def validate_rhyme_scheme(self) -> bool:
        "Validates that the poem follows the required rhyme scheme"
        pass
        # TODO: do this soon

    def clean_sentence(self, sentence: str) -> str:
        "Removes unwanted characters/spaces from end of line"
        cleaned_sentence = re.sub(r'\s*([^a-zA-Z\s]+)?$', '', sentence)
        return cleaned_sentence

    def select_kth_modifier(self, lyric_matches: str, k: int) -> str:
        """
        Selects a random replacement from top k element this increases
        variations in poems from the same image
        """
        slice_idx = min(k, len(lyric_matches))
        return random.choice(lyric_matches[:slice_idx])

    def reset(self):
        """
        Resets the poem object without destroying the class so we don't have
        to reload the models.
        """
        self.A_PATTERN = None
        self.B_PATTERN = None
        self.used_rhymes = set()
        self.inspiration_lyrics = set()
        self.stanzas = []

    def search_inspired_match(self, inspiring_line: str, rhyme_pattern: str,
                              k: int = 25) -> str:
        """
        Searches for a lyrics that are similar to the inspiration and
        modifies the sentences to fit the desired rhyme pattern. It also
        adds the inspiration lyrics to the set and update the used_rhymes set 
        as well.
        """
        line_length = len(inspiring_line.split(" "))
        target_length = random.randint(max(3, line_length), line_length + 1)
        matches = self.smtic_model.search(
            query=inspiring_line, k=k, target_len=target_length,
            already_used_lines=self.inspiration_lyrics)
        replacement_match = self.select_kth_modifier(
            matches, SELECT_FROM_TOP_K)
        if replacement_match in self.inspiration_lyrics:
            replacement_match = random.choice(get_lyrics())
        modified_sentence = self.lang_utility.modify_sentence(
            poem_line=replacement_match, rhyme_pattern=rhyme_pattern, used_rhymes=self.used_rhymes)
        clean_modified_sentence = self.clean_sentence(modified_sentence)
        # inspiration for evaluation
        self.inspiration_lyrics.add(replacement_match)
        used_rhyme = clean_modified_sentence.split(" ")[-1]
        self.used_rhymes.add(used_rhyme)
        return clean_modified_sentence

    def gen_first_stanza(self, inspiring_q: str, k: int = 25) -> bool:
        "Generates the first stanza of the poem"
        stanza = Stanza(1)
        print("Generating stanza 1")
        # first line
        matching_a_line = self.search_inspired_match(
            inspiring_q, None, k)
        self.A_PATTERN = matching_a_line.split(" ")[-1]
        stanza.add_line(matching_a_line)
        # second line
        b_matching_line = self.search_inspired_match(
            matching_a_line, None, k)
        self.B_PATTERN = b_matching_line.split(" ")[-1]
        stanza.add_line(b_matching_line)
        # third line
        a_match_3 = self.search_inspired_match(
            b_matching_line, self.A_PATTERN, k)
        stanza.add_line(a_match_3)
        self.stanzas.append(stanza)
        return True

    def generate_stanzas(self) -> bool:
        "Generates the remaining A-B pairs"
        num_of_inspiring_object_queries = len(self.inspiring_object_queries)
        curr_inspo_obj_idx = 1

        for i in range(2, 7):  # stanzas 2 - 6
            stanza = Stanza(i)
            print(f"Generating stanza {i}")
            query = None
            if curr_inspo_obj_idx < num_of_inspiring_object_queries:
                query = self.inspiring_object_queries[curr_inspo_obj_idx]
                curr_inspo_obj_idx += 1
            else:
                query = random.choice(get_lyrics())
            curr_inspo_obj_idx += 1
            a_line = self.search_inspired_match(
                inspiring_line=query, rhyme_pattern=self.A_PATTERN, k=25)
            stanza.add_line(a_line)
            b_line = self.search_inspired_match(
                inspiring_line=a_line, rhyme_pattern=self.B_PATTERN, k=25)
            stanza.add_line(b_line)
            self.stanzas.append(stanza)
        return True

    def complete_villanelle(self) -> None:
        "Adds the duplicate lines to the stanzas"
        line_1 = self.stanzas[0].get_line(0)
        line_3 = self.stanzas[0].get_line(2)
        self.stanzas[1].add_line(line_1)  # second_stanza
        self.stanzas[2].add_line(line_3)  # third_stanza
        self.stanzas[3].add_line(line_1)  # fourth_stanza
        self.stanzas[4].add_line(line_3)  # fifth stanza
        self.stanzas[5].add_line(line_1)  # sixth a
        self.stanzas[5].add_line(line_3)  # sixth b

    def gen_full_poem(self) -> None:
        "Generate an entire poem"
        self.reset()
        self.gen_first_stanza(self.inspiring_object_queries[0])
        self.generate_stanzas()
        self.complete_villanelle()

    def __str__(self) -> str:
        "Get a string representation of the poem"
        str_rep = ""
        for stanza in self.stanzas:
            str_rep += str(stanza) + "\n"
        return str_rep
