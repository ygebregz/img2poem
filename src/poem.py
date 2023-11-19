"""
@author: Yonas Gebregziabher, CSCI 3725, M6: Poetry Slam

This represents a Villanelle Poem object as well
the functionalities to generate stanzas and lines for
each stanzas
"""
from typing import List
from .model import SemanticSearchModel
from .lang_utility import LanguageUtility
from .stanza import Stanza
from utils.data_cleaner import get_lyrics
import random

SLCT_FRM_TOP_K = 2  # top k lyric matches to pick from


class VillanellePoem:

    def __init__(self, inspiring_object_queries: List[str], lang_utility: LanguageUtility,
                 smtic_model: SemanticSearchModel) -> None:
        self.inspiring_object_queries = inspiring_object_queries
        self.lang_utility = lang_utility
        self.smtic_model = smtic_model
        self.stanzas: List[Stanza] = []
        self.A_PATTERN = None
        self.B_PATTERN = None
        self.inspiration_lyrics = []  # TODO: rename other vars to make sense
        self.used_rhymes = set()

    def get_inspiring_object_queries(self) -> List[str]:
        return self.inspiring_object_queries

    def get_inspiration_lyrics(self) -> List[str]:
        return self.inspiration_lyrics

    def add_stanza(self, stanza: Stanza) -> bool:
        if not stanza.is_valid_stanza():
            return False
        self.stanzas.append(stanza)

    def validate_poem(self) -> bool:
        "Mainly checks for rhyme scheme "
        if len(self.stanzas) != 6:
            return False
        return True

    def clean_sentence(self, sentence: str) -> str:
        "This slices a sentence from its last valid word"
        words = sentence.split(" ")
        last_idx = len(words) - 1
        while last_idx >= 0:
            if words[last_idx] == "" or words[last_idx] == "\n" \
                    or words[last_idx] == " ":
                last_idx -= 1
            else:
                return " ".join(words[:last_idx+1])
        return sentence  # already clean

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
        self.inspiration_lyrics = []
        self.stanzas = []  # TODO: find way to select one to replay

    def search_inspired_match(self, inspiring_line: str, rhyme_pattern: str,
                              k: int = 25) -> str:
        "Searches and modifies a line"
        line_length = len(inspiring_line.split(" "))
        target_length = random.randint(max(3, line_length), line_length + 1)
        matches = self.smtic_model.search(
            query=inspiring_line, k=k, target_len=target_length)
        replacement_match = self.select_kth_modifier(matches, SLCT_FRM_TOP_K)
        modified_sentence = self.lang_utility.modify_sentence(
            poem_line=replacement_match, rhyme_pattern=rhyme_pattern, used_rhymes=self.used_rhymes)
        clean_modified_sentence = self.clean_sentence(modified_sentence)
        self.inspiration_lyrics.append(
            (replacement_match, clean_modified_sentence))  # for evaluation
        used_rhyme = clean_modified_sentence.split(" ")[-1]
        self.used_rhymes.add(used_rhyme)
        return clean_modified_sentence

    def gen_first_stanza(self, inspiring_q: str, k: int = 25) -> bool:
        stanza = Stanza(1)
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

    def generate_stanzas(self) -> None:
        num_of_inspiring_object_queries = len(self.inspiring_object_queries)
        curr_inspo_obj_idx = 1

        for i in range(2, 7):  # stanzas 1 - 6
            stanza = Stanza(i)
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

    def complete_villanelle(self) -> None:
        "This goes through and completes the villanelle poem"
        line_1 = self.stanzas[0].get_line(0)
        line_3 = self.stanzas[0].get_line(2)
        self.stanzas[1].add_line(line_1)  # second_stanza
        self.stanzas[2].add_line(line_3)  # third_stanza
        self.stanzas[3].add_line(line_1)  # fourth_stanza
        self.stanzas[4].add_line(line_3)  # fifth stanza
        self.stanzas[5].add_line(line_1)  # sixth a
        self.stanzas[5].add_line(line_3)  # sixth b

    def gen_full_poem(self) -> None:
        self.reset()
        self.gen_first_stanza(self.inspiring_object_queries[0])
        self.generate_stanzas()
        self.complete_villanelle()

    def __str__(self) -> str:
        str_rep = ""
        for stanza in self.stanzas:
            str_rep += str(stanza) + "\n"
        return str_rep
