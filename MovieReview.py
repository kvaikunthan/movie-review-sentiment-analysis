"""
Takes a movie review from text.txt and outputs its predicted positivity out of 1 using a natural language processing model
provided by Keras
"""

from tensorflow import keras

data = keras.datasets.imdb # IMDb dataset

word_index = data.get_word_index() # Word index mapping

# Modifying the word index mapping to have 4 special indices at the beginning
word_index = {k: (v + 3) for k, v in word_index.items()}
word_index["<PAD>"] = 0 # Padding which will be added to the end of a movie review during preprocessing if needed
word_index["<START>"] = 1
word_index["<UNK>"] = 2 # Token for unknown words
word_index["UNUSED>"] = 3

def review_encode(s):
    encoded = [1]

    for word in s:
        if word.lower() in word_index:  
            encoded.append(word_index[word.lower()])
        else:
            encoded.append(2)

    return encoded

model = keras.models.load_model('model.h5')

# text.txt contains movie review
with open("text.txt", encoding="utf-8") as f:
    for line in f.readlines():
        nline = line.replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(":", "").replace("?",
                                                                                                                  "").strip().split(
            " ")
        encode = review_encode(nline)
        encode = keras.preprocessing.sequence.pad_sequences([encode], value=word_index["<PAD>"], padding="post",
                                                            maxlen=250)
        predict = model.predict(encode)
        print("Overall positivity out of 1:", predict[0])
