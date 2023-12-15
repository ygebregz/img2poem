# img2poem

embeddings are all you need! villanelle poem generator

| Prompt Image:                                                                                                                            | Generated poem                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <img src="https://github.com/ygebregz/img2poem/assets/86376122/c91a9e1e-3b5b-4495-9662-ad7d3d3aad95" width="400" alt="frank_ocean_bike"> | New truck same boy<br>Another concept from a boy mind<br>This notion from this boy roy<br><br>Everyone has there toy<br>Everyone grows since this kind<br>New truck same boy<br><br>Hit this route like road soy<br>We come down this blind<br>This notion from this boy roy<br><br>Dim this lamps and rise out you joy<br>Mesmerized why this strobes rind<br>New truck same boy<br><br>But you have been dreaming of their coy<br>But you gorgeous to bind<br>This notion from this boy roy<br><br>Super rich youngsters while anything but loose troy<br>Regardless of winning rather of hind<br>New truck same boy<br>This notion from this boy roy |

### Installation Guide

1. If you want to curate an inspiration set of lyrics from a different author/artist,
   feel free to run `prep_data` in `utils/data_cleaner.py` and call the `embed` function
   in `src/model.py`
2. Running `main.py`, will install `yolov3.weights` and the `universal-sentence-encoder` models
   into the `model` folder.
3. You must also [install](https://nlp.stanford.edu/projects/glove/) the GloVe word embedding model
   and provide the path during the construction of the `LanguageUtility` object. By default, it
   expects the model to be stored in the `model/glove.6B.300d.txt` path. I recommend installing the
   _Common Crawl (42B tokens, 1.9M vocab, uncased, 300d vectors, 1.75 GB download)_ version for best results.
4. Install the rest of the dependencies through `pip install -r requirements.txt`

When running `main.py`, these are the commands it expects.

- `gen` - generates and reads a poem out loud
- `save` - saves a poem to the `outputs` folder with your desired name.
- `read`- reads a poem that you previously saved to a file

Wait until the TTS is over before putting in another command!

### Brief Summary
The intuition behind this is that to create novel creative text that was inspired by an artist, we can simply replace their words at random with a semantically related word. Therefore, this program first identifies the objects on the image using a pre-trained model, builds queries from those objects, and retrieves semantically related lines from an embedding database. Once we have the line, we can iterate through each word and use a word embedding model (word2vec or gloVe in this case) to replace it. 
