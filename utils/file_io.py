"""
@author: Yonas Gebregziabher, CSCI 3725, M7: Poetry Slam

Helper functions to write/read poems from file. It also 
provides wrappers to read poem lines out-loud using TTS. 
"""

from src.poem import VillanellePoem
import pyttsx3
from typing import List

tts = pyttsx3.init()
tts.setProperty('rate', 150)


def speak_lines(poem_lines: List[str]) -> None:
    "TTS method to speak the poems in the terminal"
    for line in poem_lines:
        tts.say(line)
        tts.runAndWait()


def write_to_file(poem_object: VillanellePoem, poem_name: str) -> None:
    "Saves the poem to file"
    with open(f"outputs/poem_{poem_name.strip()}.txt", "w") as file:
        file.write(str(poem_object))


def read_from_file(file_path: str) -> None:
    "Speaks a poem out from file"
    with open(file_path, "r") as file:
        poem_lines = file.readlines()
    for line in poem_lines:
        print(line)
    speak_lines(poem_lines[:-3])  # we don't want it to read the scores


def read_from_object(poem: VillanellePoem):
    "Speaks a poem out from the VillanellePoem object itself"
    lines = poem.get_all_poem_lines()
    speak_lines(lines)
