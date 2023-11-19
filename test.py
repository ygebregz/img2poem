import re


def clean_sentence_with_regex(sentence: str) -> str:
    cleaned_sentence = re.sub(r'\s*([^a-zA-Z\s]+)?$', '', sentence)
    return cleaned_sentence


sentence = "how how are you doing today -1-"
print(sentence)
print(clean_sentence_with_regex(sentence))
