"""
Represents a Villanelle poem's stanza
"""

from typing import List


class Stanza:

    def __init__(self, order: int) -> None:
        "Docstring this well"
        self.lines: List[str] = []
        self.order = order

    def add_line(self, line: str) -> None:
        self.lines.append(line)

    def get_line(self, line_num: int) -> str:
        return self.lines[line_num]

    def get_all_lines(self) -> List[str]:
        return self.lines

    def is_valid_stanza(self) -> None:
        # TODO: Implement this
        if self.order != 6 and len(self.lines) != 3:
            return False
        if self.order == 6 and len(self.lines) != 4:
            return False

    def __str__(self) -> str:
        stanza_lines = ""
        for line in self.lines:
            stanza_lines += line + "\n"
        return stanza_lines
