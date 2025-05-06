import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# 1. Prepare the dataset
english_sentences = ["I am happy", "You are beautiful", "She is reading", "We are learning", "They are working",
                     "I love you", "He is playing", "She loves me", "I am studying", "We are talking"]

french_sentences = ["Je suis heureux", "Tu es belle", "Elle lit", "Nous apprenons", "Ils travaillent",
                    "Je t'aime", "Il joue", "Elle m'aime", "Je suis en train d'étudier", "Nous parlons"]

# 2. Preprocess the data
# Tokenize English
english_tokenizer = Tokenizer()
english_tokenizer.fit_on_texts(english_sentences)
english_sequences = english_tokenizer.texts_to_sequences(english_sentences)
english_vocab_size = len(english_tokenizer.word_index) + 1  # +1 for padding

# Tokenize French
french_tokenizer = Tokenizer()
french_tokenizer.fit_on_texts(french_sentences)
french_sequences = french_tokenizer.texts_to_sequences(french_sentences)
french_vocab_size = len(french_tokenizer.word_index) + 1  # +1 for padding

# Pad the sequences
max_input_length = max([len(seq) for seq in english_sequences])
max_output_length = max([len(seq) for seq in french_sequences])

english_sequences = pad_sequences(english_sequences, maxlen=max_input_length, padding='post')
french_sequences = pad_sequences(french_sequences, maxlen=max_output_length, padding='post')

# Prepare decoder input and output
french_input = french_sequences[:, :-1]  # remove last token
french_output = french_sequences[:, 1:]  # remove first token

# 3. Define the Encoder-Decoder model
# Encoder
encoder_inputs = Input(shape=(max_input_length,))
encoder_embedding = Dense(256, activation='relu')(encoder_inputs)
encoder_lstm = LSTM(256, return_state=True)
encoder_outputs, state_h, state_c = encoder_lstm(encoder_embedding)
encoder_states = [state_h, state_c]

# Decoder
decoder_inputs = Input(shape=(max_output_length - 1,))
decoder_embedding = Dense(256, activation='relu')(decoder_inputs)
decoder_lstm = LSTM(256, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)
decoder_dense = Dense(french_vocab_size, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Define the model
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 4. Train the model
model.fit([english_sequences, french_input], np.expand_dims(french_output, -1), epochs=100, batch_size=16)

# 5. Translate an English sentence
def translate_sentence(input_sentence):
    input_sequence = english_tokenizer.texts_to_sequences([input_sentence])
    input_sequence = pad_sequences(input_sequence, maxlen=max_input_length, padding='post')

    # Encode the input sentence
    encoder_output, state_h, state_c = encoder_lstm(input_sequence)

    # Prepare the first token for decoding
    target_sequence = np.zeros((1, 1))
    target_sequence[0, 0] = french_tokenizer.word_index['starttoken']  # Special token for start

    translated_sentence = ""
    
    while True:
        # Predict the next token
        decoder_output, _, _ = decoder_lstm(target_sequence, initial_state=[state_h, state_c])
        decoder_probs = decoder_dense(decoder_output)
        
        # Get the token with the highest probability
        sampled_token_index = np.argmax(decoder_probs[0, -1, :])
        sampled_token = french_tokenizer.index_word[sampled_token_index]

        # Stop if end token or sentence is complete
        if sampled_token == 'endtoken' or len(translated_sentence.split()) >= max_output_length:
            break

        # Append the token to the translated sentence
        translated_sentence += " " + sampled_token

        # Update target sequence
        target_sequence = np.zeros((1, 1))
        target_sequence[0, 0] = sampled_token_index

    return translated_sentence

# Translate a sample sentence
sample_sentence = "I am happy"
print(f"English: {sample_sentence}")
print(f"French: {translate_sentence(sample_sentence)}")
