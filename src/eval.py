"""
@author: Yonas Gebregziabher, CSCI 3725, M7: Poetry Slam

This class evaluates a Villanele poem]
"""
from .poem import VillanellePoem


class VillanelleEvaluator:
    def __init__(self, poem: VillanellePoem) -> None:
        self.poem = poem

    def sim_to_insp_lyrics(self) -> float:
        "Returns % similarity to inspiring lines"
        inspiring_lyrics = self.poem.get_inspiring_lyrics()
        # TODO: calc TD-IDF here
        pass

    def check(self) -> float:
        # TODO: also check that rhymes are not repeated
        return 0.0

    def measure_rhyme_success() -> float:
        "Return % of successful rhymes"
