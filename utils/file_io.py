"""
Helps to write Villanelle poems to text files and creating
VillanellePoem objects from existing text files
"""

from src.poem import VillanellePoem
import pyttsx3
from typing import List

tts = pyttsx3.init()
tts.setProperty('rate', 150)


def speak_lines(poem_lines: List[str]) -> None:
    for line in poem_lines:
        tts.say(line)
        tts.runAndWait()


def write_to_file(poem_object: VillanellePoem, poem_num: str) -> None:
    with open(f"outputs/poem_{poem_num}.txt", "w") as file:
        file.write(str(poem_object))


def read_from_file(file_path: str) -> None:
    with open(file_path, "r") as file:
        poem_lines = file.readlines()
    for line in poem_lines:
        print(line)
    speak_lines(poem_lines)


def read_from_object(poem: VillanellePoem):
    lines = []
    for stanza in poem.stanzas:
        lines.extend(stanza.get_all_lines())
    speak_lines(lines)
