"""
@author: Yonas Gebregziabher, CSCI 3725, M7: Poetry Slam

This class uses the Google Universal Sentence Encoder to perform
Semantic search so that we're able to retrieve the most semantically related
sentences from Frank Ocean's discography. 
"""

import tensorflow as tf
import tensorflow_hub as hub
from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle
from utils.data_cleaner import get_lyrics
import random
import sys

PRE_TRAINED_MODEL_URL = "https://tfhub.dev/google/universal-sentence-encoder-large/5"


class SemanticSearchModel:

    def __init__(self, model_path="model/encoder/universal_sentence_encoder",
                 embeddings_path="model/encoder/frank_ocean_lyrics_embeddings.pkl") -> None:
        "Initializes the SemanticSearchModel class"
        self.model_path = model_path
        self.embeddings_path = embeddings_path
        if os.path.exists(model_path):
            self.model = hub.load(model_path)
            print(f"Model loaded from {model_path}")
        else:
            self.model = hub.load(PRE_TRAINED_MODEL_URL)
            tf.saved_model.save(self.model, model_path)
            print(
                f"Model downloaded from net and downloaded to {model_path}")
        if os.path.exists(embeddings_path):
            with open(embeddings_path, "rb") as embedding:
                self.embeddings = pickle.load(embedding)
            print(f"Embedding loaded from {embeddings_path}")
        else:
            self.embeddings = None
        self.lyrics = get_lyrics()

    def embed_lyrics(self, lyrics: List[str]):
        "Embeds given set of line into the model"
        self.lyrics = lyrics
        if self.embeddings is None:
            self.embeddings = self.model(lyrics)
        else:
            self.embeddings = np.concatenate(
                [self.embeddings, self.model(lyrics)])
        with open(self.embeddings_path, "wb") as embedding:
            pickle.dump(self.embeddings, embedding)
        print(f"Embedded and saved to {self.embeddings_path} ")

    def search(self, query: str, k: int = 25, target_len: int = 0,
               already_used_lines: set[str] = set()):
        """
        Searches for a semantically related word that by finding k similar
        lyrics and selecting a random lyric that is the closest
        to the desired target length. It also ensures that we do not re-use
        a line that we've already used as inspiration. 
        """
        query_embedding = self.model([query])
        similarities = cosine_similarity(query_embedding, self.embeddings)
        most_similar_lines = np.argsort(similarities[0])[-k:][::-1]
        sim_lyrics = [self.lyrics[i]
                      for i in most_similar_lines if self.lyrics[i] not in already_used_lines]
        if target_len == 0:
            return sim_lyrics
        desired_lengths = []
        max_length_index = 0
        closest_distance = sys.maxsize
        for i in range(len(sim_lyrics)):
            line = sim_lyrics[i].split(" ")
            if abs(len(line) - target_len) < closest_distance:
                max_length_index = i
                closest_distance = len(line)
            if len(line) == target_len:
                desired_lengths.append(sim_lyrics[i])
        if len(desired_lengths) == 0:
            return [sim_lyrics[max_length_index].strip("\n")]
        return [random.choice(desired_lengths).strip("\n")]
