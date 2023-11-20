# img2poem

Embeddings are all you need! M7: Poetry Generation

| Prompt Image:                                                                                                                            | Generated poem                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <img src="https://github.com/ygebregz/img2poem/assets/86376122/e17f6f0f-7cf0-4e87-9e51-429f8c01494f" width="400" alt="frank_ocean_bike"> | New truck same boy<br>Another concept from a boy mind<br>This notion from this boy roy<br><br>Everyone has there toy<br>Everyone grows since this kind<br>New truck same boy<br><br>Hit this route like road soy<br>We come down this blind<br>This notion from this boy roy<br><br>Dim this lamps and rise out you joy<br>Mesmerized why this strobes rind<br>New truck same boy<br><br>But you have been dreaming of their coy<br>But you gorgeous to bind<br>This notion from this boy roy<br><br>Super rich youngsters while anything but loose troy<br>Regardless of winning rather of hind<br>New truck same boy<br>This notion from this boy roy |

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
