# img2poem

Embeddings are all you need!

M7: Poetry Generation

### Sample Poem

Prompt Image:
![frank_ocean_bike](https://github.com/ygebregz/img2poem/assets/86376122/e17f6f0f-7cf0-4e87-9e51-429f8c01494f)

Generated poem:

```
New truck same boy
Another concept from a boy mind
This notion from this boy roy

Everyone has there toy
Everyone grows since this kind
New truck same boy

Hit this route like road soy
We come down this blind
This notion from this boy roy

Dim this lamps and rise out you joy
Mesmerized why this strobes rind
New truck same boy

But you have been dreaming of their coy
But you gorgeous to bind
This notion from this boy roy

Super rich youngsters while anything but loose troy
Regardless of winning rather of hind
New truck same boy
This notion from this boy roy
```

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
