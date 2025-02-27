# -*- coding: utf-8 -*-
"""Sentence_completion.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cT-egQE3Oww7FHpeAwH6Mg14udcmlP1O
"""

# Sentence Prediction using RNN

import pandas as pd
# This imports the pandas library, which is commonly used for data manipulation and analysis.
# It is likely being used to load or process the data in a structured format (like CSV, Excel, or DataFrame).
import numpy as np
from tensorflow.keras.models import Sequential
# Sequential is a Keras class used to build models layer by layer. It is a linear stack of layers that allows easy construction of models like RNNs or CNNs.
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense
# These are various layers added to the model.
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Sample training text
data = ''' Once upon a time in a land far away, there lived a young prince. The prince was brave, strong and kind. Ond day, the prince set out on an adventure to discover
           new lands and hidden treasures.'''

'''Data Preparation:
The sample text is tokenized using Keras's Tokenizer. Input sequence are created with an increasing number of tokens to predict the next wi=ord in each sequence.
tokenizer= Tokenizer(): Creates an instance of the Tokenizer, which will be used to convert the text into sequences of numbers.
tokenizer.fit_on_text([data]): Fits the tokenizer on the input text(data), creating a dictionary that maps each word to a unique integer.
total_words = len(tokenizer.word_index)+ 1: It is a dictionary that maps words to indices. We add 1 to the total number of words because indices typically start from 1,
and we need to account for a padding token(if used)'''

# Preprocess the text
tokenizer = Tokenizer()
tokenizer.fit_on_texts([data])
total_words = len(tokenizer.word_index)+1

'''
tokenizer.texts_to_sequences([line]) takes the current sentence(line) and converts it into the list of tokens(or integers).
This tokenization steps assumes you have a tokenizer object(likely a tokenizer from keras or a similar library) that maps the words to the unique integers.
Since texts_to_sequence returns a list of lists (because it processes batches of sentences), the [0] index is used to extract the token list for the current sentence.
This for loop iterates over tokeb=nization sentence, starting from the 2nd token. In each iteration it creates an n_gram sequence by taking the first i+1 tokens from the
token_list using slicing: token_list[:i+1]. This gives a subsequence of increasing length.'''

# Convert the text into sequences of tokens
input_sequences = []
for line in data.split(". "):
  token_list = tokenizer.texts_to_sequences([line])[0]
  for i in range(1, len(token_list)):
    n_gram_sequence = token_list[:i+1]
    input_sequences.append(n_gram_sequence)


'''
max_sequence_len: Finds the length of the longest sequence in input_sequences so that all the sequences can be padded to teh same length.
pad_sequences(input_sequences, maxlen = max_sequence_len, padding = 'pre'):
Pads shorter sequences with zeros at the beginning ('pre' so that all the sequences are of the same length.)'''

# Pad sequences for consistent input size
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = np.array(pad_sequences(input_sequences, maxlen = max_sequence_len, padding = 'pre'))

'''X=input_sequences[;,:-1]: Takes all but the last word of each sequence as the input(features). This is what the model will use to predict the next word.
y = input_sequences[:,-1]: The last word in the sentence is treated as a label'''


# Create predictors and label:
X,y = input_sequences[:,:-1], input_sequences[:,-1]
y = np.eye(total_words)[y]  # One-hot encodes the labels

'''
Model Architecture:
An embedding layer to represent words in vectors. A simple RNN layer to learn the sequence of words. A dense layer with softmax activation to predict the next word based on
the input sequence.'''

# Build the RNN model
model = Sequential()
model.add(Embedding(total_words,10, input_length = max_sequence_len-1))
model.add(SimpleRNN(150,return_sequences = False))
model.add(Dense(total_words, activation = 'softmax'))

# Compile the model
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics=['accuracy'])
model.summary()

# Train the model
model.fit(X,y, epochs=100, verbose=1)

'''predict_next_word: Function to predict the next num words given some seed text

tokenizer.texts_to_sequences([seed_text])[0]: Converts the seed text into a sequence of integers. pad_sequences([token list], maxlen=max sequence len-1, padding='pre'); Pads the
token list to match the input length required by the model. model predict(token list): The model predicts probabilities for each word in the vocabulary.
np.argmax(predicted): Retrieves the index of the word with the highest probability, for word, index in tokenizer.word_index.items(): Finds the word corresponding to the predicted
index. seed.text++ output word: Appends the predicted word to the seed text. return seed_text: Returns the seed text with predicted words appended. Testing the Model: python Copy
code seed_text = "The prince" next words = 5 print(predict_next_word(seed_text, next_words)) seed_text = "The prince: The seed text for which you want to generate the next few
words, next_words = 5: The number of words you want to predict.


print(predict_next_word(seed_text , next_words)): Prints the result'''

# Function to predict next word
def predict_next_word(seed_text, num_words):
    for _ in range(num_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
        predicted = np.argmax(model.predict(token_list), axis=-1)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    return seed_text

# Test the model
seed_text = "The prince"
next_words = 5
print(predict_next_word(seed_text, next_words))