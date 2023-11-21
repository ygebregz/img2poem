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

### Technical details

I read a research [paper](https://www.microsoft.com/en-us/research/uploads/prod/2018/10/img2poem_final_camera_ready.pdf) published by Microsoft on a system that generated poems from images. The approach was
to use an image-poem pair dataset to capture meaning from both and train an RNN to generate
the text. With this in mind, I explored LSTM and Seq2seq but I did not achieve the results that I wanted.
I then came to the realization if all I wanted to generate was novel Villanelle poems in the style of
Frank Ocean, the problem is actually a lot simpler. First, I used a pre-trained model
to identify objects in an image with a 50% confidence threshold. Using this list, I could now
retrieve relevant lines from Frank Ocean's lyrics and modify the sentence to fit our needs. However,
this had some limitations. However, how do I select a line that is relevant to an object in an image
but does not use the exact choice of words the image classifier has selected? How do I modify the sentence
to keep its overall style/meaning/themes of what I hear in Frank Ocean's lyrics?

To solve the problem above, I knew that there needed to be a way that I could convert
the dataset into a dense matrix to do mathematical operations on in order to do
a semantic search for related concepts. Therefore, I read about Google's [paper](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/46808.pdf) on Universal Sentence Encoder.
Therefore, I then used this model to embed all of the Frank Ocean lyrics that I compiled
and cleaned. Now that we had an embedded model, we could retrieve semantically related
Frank Ocean lyrics to modify. This also means that we don't have to use an image.
We could also just provide an array of the objects that we want our poem to talk about :)
But now another problem persists. How do we modify the line
to keep the style/message but make it novel? That is when I then found Stanford's [paper](https://nlp.stanford.edu/pubs/glove.pdf) on their GloVe model. This is a similar idea to the sentence encoder
but it is at the word level and we don't have to supply the words. img2poem creates a dictionary
of word to embedding mappings in order to retrieve the closest embeddings to a word.
Next, we use NLTK to identify the POS tags at a sentence level for each word. It is important to run
it at a sentence level before replacing each word individually because words have different POS tags depending
on the context of the sentence. The GloVe model is not only used to modify sentences but it is also used to generate quality queries. Simply searching for a single word from our embedding model will not provide the best results; instead, we concatenate similar words to the object classified in the image to return better results.

Finally, while we still have objects to find similar lyrics for, we use that as
an inspiration for the first line. The next line in the stanza then uses the previous line
as an inspiration to find a new unused lyric. This makes it so that the stanzas individually
are cohesive. This generation process also ensures that we follow the Villanelle
poem rhyming scheme and line repetition rules. The system also evaluates the poems it generates across
three metrics.

- Success of correct rhyme pattern throughout the poem - penalizes for repeated use of the same word that didn't come from a repeated line.
- Similarity to the inspiring set of lines that inspired it -- averages around 2% similarity to original lines
- Similarity to the image/concepts -- Since poems use metaphors to refer to things and we want to encourage novelty,
  the percentage range is normalized from values 0 - 0.30

Ensuring that words rhyme, exhibiting similar themes/style of writing as our desired artist, and being intentional
about the generation process entices a surprising reaction from the audience.

### Challenge as a Computer Science Student

- Learned about deep learning concepts like LSTM/seq2seq during the research part of this project
- Learned about keras -- even though I didn't use it for my final project
- Learned a lot about how powerful dense matrix representations of things are, especially for text.
  I plan to continue exploring how else we could use embeddings to represent other data as we move further away from
  BOW and one hot encoding model.
I challenged myself to achieve similar results as the Microsoft research paper without training a model
  that does the entire process and I'm happy with the results.
- Research and independent working skills will also be valuable skills to have in industry/research.
