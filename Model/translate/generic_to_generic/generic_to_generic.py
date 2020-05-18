import numpy as np
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input
import os
from Model.translate import AbstractModel
import json


SOS = "<SOS>"
EOS = "<EOS>"
UNK = "<UNK>"
batch_size = 64  # Batch size for training.
epochs = 200  # Number of epochs to train for.
latent_dim = 1024  # Latent dimensionality of the encoding space.


class Gen2GenModel(AbstractModel):
    """
    class for translation model from generic pseudo code to generic python code
    """
    def __init__(self, model, source_word_to_index, target_word_to_index, max_encoder_seq_length,
                 max_decoder_seq_length, num_encoder_tokens=None, num_decoder_tokens=None, accuracy=None, version=None):
        super().__init__(accuracy, version)
        self.model = model
        encoder_inputs = model.input[0]  # input_1
        encoder_outputs, state_h_enc, state_c_enc = model.layers[2].output  # lstm_1
        encoder_states = [state_h_enc, state_c_enc]
        self.encoder_model = Model(encoder_inputs, encoder_states)

        decoder_inputs = model.input[1]  # input_2
        decoder_state_input_h = Input(shape=(latent_dim,), name='input_3')
        decoder_state_input_c = Input(shape=(latent_dim,), name='input_4')
        decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
        decoder_lstm = model.layers[3]
        decoder_outputs, state_h_dec, state_c_dec = decoder_lstm(
            decoder_inputs, initial_state=decoder_states_inputs)
        decoder_states = [state_h_dec, state_c_dec]
        decoder_dense = model.layers[4]
        decoder_outputs = decoder_dense(decoder_outputs)
        self.decoder_model = Model(
            [decoder_inputs] + decoder_states_inputs,
            [decoder_outputs] + decoder_states)

        self.source_word_to_index = source_word_to_index
        self.target_word_to_index = target_word_to_index
        self.num_encoder_tokens = num_encoder_tokens if num_encoder_tokens else len(source_word_to_index)
        self.num_decoder_tokens = num_decoder_tokens if num_decoder_tokens else len(target_word_to_index)
        self.max_encoder_seq_length = max_encoder_seq_length
        self.max_decoder_seq_length = max_decoder_seq_length

    def evaluate(self, input_data):
        """
        translate from the generic pseudo code to a generic python code
        :param input_data: generic pseudo command
        :return: generic python command
        """
        input_vec = np.zeros((1, self.max_encoder_seq_length, self.num_encoder_tokens), dtype='float32')
        if len(input_data) > self.max_encoder_seq_length:
            # data is too long and need to be shorten
            input_data = input_data[:self.max_encoder_seq_length]
        for t, word in enumerate(input_data):
            input_vec[0, t, self.source_word_to_index[word if word in self.source_word_to_index.keys() else UNK]] = 1.
        # Encode the input as state vectors.
        states_value = self.encoder_model.predict(input_vec)

        # Generate empty target sequence of length 1.
        target_seq = np.zeros((1, 1, self.num_decoder_tokens))
        # Populate the first character of target sequence with the start character.
        target_seq[0, 0, self.target_word_to_index[SOS]] = 1.

        # Sampling loop for a batch of sequences
        # (to simplify, here we assume a batch of size 1).
        stop_condition = False
        decoded_sentence = []
        while not stop_condition:
            output_tokens, h, c = self.decoder_model.predict(
                [target_seq] + states_value)

            # Sample a token
            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            sampled_word = self.target_word_to_index.inverse[sampled_token_index]

            if sampled_word == EOS:
                return decoded_sentence

            decoded_sentence.append(sampled_word)

            # Update the target sequence (of length 1).
            target_seq = np.zeros((1, 1, self.num_decoder_tokens))
            target_seq[0, 0, sampled_token_index] = 1.

            # Update states
            states_value = [h, c]

        return decoded_sentence

    def save(self, file_name):
        """
        saves to files the model
        :param file_name: directory name
        """
        os.mkdir(file_name)
        self.model.save(os.path.join(file_name, "s2s.h5"))
        f = open(os.path.join(file_name, "objects.json"), "w")
        json.dump((dict(self.source_word_to_index), dict(self.target_word_to_index), self.max_encoder_seq_length,
                   self.max_decoder_seq_length, self.num_encoder_tokens, self.num_decoder_tokens), f)
        f.close()
