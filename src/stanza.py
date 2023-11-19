"""
@author: Yonas Gebregziabher, CSCI 3725, M7: Poetry Slam

Represents a Villanelle poem's stanza.
"""

from typing import List


class Stanza:

    def __init__(self, order: int) -> None:
        "Initializes the Stanza object"
        self.lines: List[str] = []
        self.order = order

    def add_line(self, line: str) -> None:
        "Adds a line to the stanza"
        self.lines.append(line)

    def get_line(self, line_num: int) -> str:
        "Return the given from the stanza"
        return self.lines[line_num]

    def get_all_lines(self) -> List[str]:
        "Return all of the stanza's lines"
        return self.lines

    def is_valid_stanza(self) -> bool:
        "Checks if it contains the required number of lines"
        if self.order != 6 and len(self.lines) != 3:
            return False
        if self.order == 6 and len(self.lines) != 4:
            return False

    def __str__(self) -> str:
        "Get a string representation of the stanza"
        stanza_lines = ""
        for line in self.lines:
            stanza_lines += line + "\n"
        return stanza_lines
