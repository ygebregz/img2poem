# poetry

M7: Poetry Generation

### Ideas

- Test smaller ube model so i can lower load up times
- since the image classifier is returning a set of objects as a list, can provide additional functionality where users can provide idea of what they want by a list of objects represnting that idea
- Fully implement evaluation
- Fix requirements .txt file

### Installation Guide

- tldr, running the program will install pretrained weights locally on your machine
- download GloVe model embedding of your choice. and provide the path
  to the `LanguageUtility` during construction of the object.
  Link to download. [Download](https://nlp.stanford.edu/projects/glove/)
  I recommend installing the _Common Crawl (42B tokens, 1.9M vocab, uncased, 300d vectors, 1.75 GB download)_ for best results
- install requirements.txt for all the required modules
