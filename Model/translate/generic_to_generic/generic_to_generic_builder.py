from Model.translate import *
from Model.translate.generic_to_generic import *
from random import shuffle
import json
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, LSTM, Dense
import numpy as np
from bidict import bidict


class Gen2GenBuilder(AbstractModelBuilder):
    """
    class of builder that builds the Gen2Gen model.
    """
    def train(self, data_set=None, save_to=None):
        """
        train the model.
        :param data_set: data set used to train
        :param save_to: location to save the model if not none
        :return: the model
        """
        shuffle(data_set)
        # Vectorize the data.
        input_texts = []
        target_texts = []
        input_words = {EOS, SOS, UNK}
        target_words = {SOS, EOS}
        samples_weight = np.zeros(len(data_set))

        for (input_text, target_text, w), i in enumerate(data_set):
            target_text = [SOS] + target_text + [EOS]
            input_texts.append(input_text)
            target_texts.append(target_text)
            for word in input_text:
                if word not in input_words:
                    input_words.add(word)
            for word in target_text:
                if word not in target_words:
                    target_words.add(word)
            samples_weight[i] = w

        input_characters = sorted(list(input_words))
        target_characters = sorted(list(target_words))
        num_encoder_tokens = len(input_characters)
        num_decoder_tokens = len(target_characters)
        max_encoder_seq_length = max([len(txt) for txt in input_texts])
        max_decoder_seq_length = max([len(txt) for txt in target_texts])

        print('Number of samples:', len(input_texts))
        print('Number of unique input tokens:', num_encoder_tokens)
        print('Number of unique output tokens:', num_decoder_tokens)
        print('Max sequence length for inputs:', max_encoder_seq_length)
        print('Max sequence length for outputs:', max_decoder_seq_length)

        source_word_to_index = bidict(dict(
            [(char, i) for i, char in enumerate(input_characters)]))
        target_word_to_index = bidict(dict(
            [(char, i) for i, char in enumerate(target_characters)]))

        encoder_input_data = np.zeros(
            (len(input_texts), max_encoder_seq_length, num_encoder_tokens),
            dtype='float32')
        decoder_input_data = np.zeros(
            (len(input_texts), max_decoder_seq_length, num_decoder_tokens),
            dtype='float32')
        decoder_target_data = np.zeros(
            (len(input_texts), max_decoder_seq_length, num_decoder_tokens),
            dtype='float32')

        for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
            for t, word in enumerate(input_text):
                encoder_input_data[i, t, source_word_to_index[word]] = 1.
            encoder_input_data[i, t + 1:, source_word_to_index[EOS]] = 1.
            for t, word in enumerate(target_text):
                # decoder_target_data is ahead of decoder_input_data by one timestep
                decoder_input_data[i, t, target_word_to_index[word]] = 1.
                if t > 0:
                    # decoder_target_data will be ahead by one timestep
                    # and will not include the start character.
                    decoder_target_data[i, t - 1, target_word_to_index[word]] = 1.
            decoder_input_data[i, t + 1:, target_word_to_index[EOS]] = 1.
            decoder_target_data[i, t:, target_word_to_index[EOS]] = 1.

        # Define an input sequence and process it.
        encoder_inputs = Input(shape=(None, num_encoder_tokens))
        #encoder = LSTM(latent_dim, return_state=True)
        encoder_lstm1 = LSTM(latent_dim, name='encoder_lstm1',
                             return_sequences=True, return_state=True)
        encoder_lstm2 = LSTM(latent_dim, name='encoder_lstm2',
                             return_sequences=True, return_state=True)
        encoder_lstm3 = LSTM(latent_dim, name='encoder_lstm3',
                             return_sequences=False, return_state=True)
        # Connect all the LSTM-layers.
        x = encoder_inputs
        x, _, _ = encoder_lstm1(x)
        x, _, _ = encoder_lstm2(x)
        encoder_outputs, state_h, state_c = encoder_lstm3(x)
        # We discard `encoder_outputs` and only keep the states.
        encoder_states = [state_h, state_c]

        # Set up the decoder, using `encoder_states` as initial state.
        decoder_initial_state_h1 = Input(shape=(latent_dim,),
                                         name='decoder_initial_state_h1')

        decoder_initial_state_c1 = Input(shape=(latent_dim,),
                                         name='decoder_initial_state_c1')

        decoder_initial_state_h2 = Input(shape=(latent_dim,),
                                         name='decoder_initial_state_h2')

        decoder_initial_state_c2 = Input(shape=(latent_dim,),
                                         name='decoder_initial_state_c2')
        decoder_inputs = Input(shape=(None, num_decoder_tokens))
        # We set up our decoder to return full output sequences,
        # and to return internal states as well. We don't use the
        # return states in the training model, but we will use them in inference.
        #decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
        decoder_lstm1 = LSTM(latent_dim, name='decoder_lstm1',
                             return_sequences=True, return_state=True)
        decoder_lstm2 = LSTM(latent_dim, name='decoder_lstm2',
                             return_sequences=True, return_state=True)

        decoder_dense = Dense(
            num_decoder_tokens, activation='softmax', name="decoder_output")
        # connect the decoder for training (initial state = encoder_state)
        # I feed the encoder_states as inital input to both decoding lstm layers
        x = decoder_inputs
        x, h1, c1 = decoder_lstm1(x, initial_state=encoder_states)
        # I tried to pass [h1, c1] as initial states in line below, but that result in rubbish
        x, _, _ = decoder_lstm2(x, initial_state=encoder_states)
        decoder_output = decoder_dense(x)

        # Define the model that will turn
        # `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
        model_train = Model([encoder_inputs, decoder_inputs], decoder_output)
        model_encoder = Model(inputs=encoder_inputs, outputs=encoder_states)

        model.compile(optimizer='rmsprop', loss='categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit([encoder_input_data, decoder_input_data], decoder_target_data,
                  batch_size=batch_size,
                  epochs=epochs,
                  validation_split=0.2,
                  samples_weight=samples_weight)
        return Gen2GenModel(model, source_word_to_index, target_word_to_index, max_encoder_seq_length,
                            max_decoder_seq_length, num_encoder_tokens, num_decoder_tokens)

    def train_and_test(self, data_set, to_save=True, save_to=None, k=5):
        raise NotImplemented

    def load(self, location):
        """
        read a model from files and returns it
        :param location: files location
        :return: the model read
        """
        model = load_model(os.path.join(location, 's2s.h5'))
        f = open(os.path.join(location, 'objects.json'), "r")
        (source_word_to_index, target_word_to_index, max_encoder_seq_length,
         max_decoder_seq_length, num_encoder_tokens, num_decoder_tokens) = json.load(f)
        f.close()
        return Gen2GenModel(model, bidict(source_word_to_index), bidict(target_word_to_index), max_encoder_seq_length,
                            max_decoder_seq_length, num_encoder_tokens, num_decoder_tokens)


