"""
@author: Yonas Gebregziabher, CSCI 3725, M6: Poetry Slam

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

PRE_TRAINED_MODEL_URL = "https://tfhub.dev/google/universal-sentence-encoder/4"


class SemanticSearchModel:

    def __init__(self, model_path="model/encoder/universal_sentence_encoder",
                 embeddings_path="model/encoder/frank_ocean_lyrics_embeddings.pkl") -> None:
        self.model_path = model_path
        self.embeddings_path = embeddings_path
        if os.path.exists(model_path):
            self.model = hub.load(model_path)
            print("Model loaded from file")
        else:
            self.model = hub.load(PRE_TRAINED_MODEL_URL)
            tf.saved_model.save(self.model, model_path)
            print(
                "Model downloaded from net and downloaded to model folder")
        if os.path.exists(embeddings_path):
            with open(embeddings_path, "rb") as embedding:
                self.embeddings = pickle.load(embedding)
            print("Embedding loaded from file")
        else:
            self.embeddings = None
        self.lyrics = get_lyrics()

    def embed_lyrics(self, lyrics: List[str]):
        self.lyrics = lyrics
        if self.embeddings is None:
            self.embeddings = self.model(lyrics)
        else:
            self.embeddings = np.concatenate(
                [self.embeddings, self.model(lyrics)])
        with open(self.embeddings_path, "wb") as embedding:
            pickle.dump(self.embeddings, embedding)
        print("Embedded and saved to file")

    def search(self, query: str, k: int = 25, target_len: int = 0):
        query_embedding = self.model([query])
        similarities = cosine_similarity(query_embedding, self.embeddings)
        most_similar_lines = np.argsort(similarities[0])[-k:][::-1]
        sim_lyrics = [self.lyrics[i] for i in most_similar_lines]
        if target_len == 0:
            return sim_lyrics
        desired_lengths = []
        max_length_index = 0
        closest_distance = 999999999
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
