# To read CSV files
import pandas as pd

# To add paddings to the samples
from tensorflow.keras.preprocessing.sequence import pad_sequences

# To one-hot encode
from tensorflow.keras.utils import to_categorical

# To train the model
from tensorflow.keras.layers import Input, LSTM, Embedding, Dense
from tensorflow.keras.models import Model

# To manipulate data
import numpy as np


class UsecaseModel():
    def __init__(self):
        TRAIN_CSV_PATH = 'train.csv'  # Train data location
        TEST_CSV_PATH = 'test.csv'  # Test data location

        # Reads from CSV file for training
        lines = pd.read_csv(self.TRAIN_CSV_PATH, names=['src', 'tar'], sep=',', skiprows=[0])

        # Determines how many samples to read
        lines = lines[0:5000]

        # Changes the start and end symbol of target data
        # \t : start symbol
        # \n : end symbol
        lines.tar = lines.tar.apply(lambda x: '\t ' + x + ' \n')

        # Creates a set of letters for source language - Englsih
        src_vocab = set()
        # Reads line by line, character by character
        for line in lines.src:
            for char in line:
                src_vocab.add(char)

        # Creates a set of letters for target language - PlantUML
        tar_vocab = set()
        for line in lines.tar:
            for char in line:
                tar_vocab.add(char)

        src_vocab_size = len(src_vocab) + 1
        tar_vocab_size = len(tar_vocab) + 1

        # Gives an index for each letter in the set
        src_to_index = dict([(word, i + 1) for i, word in enumerate(src_vocab)])
        tar_to_index = dict([(word, i + 1) for i, word in enumerate(tar_vocab)])

        # Integer-encodes for English sentence samples, which will become the input of encoder
        encoder_input = []
        # Read line by line, character by character from input data
        for line in lines.src:
            temp_X = []
            for w in line:
                temp_X.append(src_to_index[w])  # Encode letter to corresponding integer
            encoder_input.append(temp_X)

        # Integer-encodes for PlantUML sentence samples, which will become the input of decoder
        decoder_input = []
        for line in lines.tar:
            temp_X = []
            for w in line:
                temp_X.append(tar_to_index[w])
            decoder_input.append(temp_X)
        print(decoder_input[:5])

        # Removes '\t' from the very first of true data
        # to compare them with the predicted data from the decoder later
        decoder_target = []
        for line in lines.tar:
            t = 0
            temp_X = []
            for w in line:
                if t > 0:
                    temp_X.append(tar_to_index[w])
                t = t + 1
            decoder_target.append(temp_X)
        print(decoder_target[:5])

        # In order to add 'paddings' to English and PlantUML sentences,
        # let's get the length of the sample with the maximum length from source and target
        max_src_len = max([len(line) for line in lines.src])
        max_tar_len = max([len(line) for line in lines.tar])

        encoder_input = pad_sequences(encoder_input, maxlen=max_src_len, padding='post')
        decoder_input = pad_sequences(decoder_input, maxlen=max_tar_len, padding='post')
        decoder_target = pad_sequences(decoder_target, maxlen=max_tar_len, padding='post')

        # One-hot-encodes for every data, including true data and input data
        encoder_input = to_categorical(encoder_input)
        decoder_input = to_categorical(decoder_input)
        decoder_target = to_categorical(decoder_target)

        # END OF DATA PREPROCESSING

        # Now use seq2seq for training translator using 'teacher forcing'
        # Uses LSTM (hidden and cell status each)
        # Defines the inputs and outputs for the encoder
        encoder_inputs = Input(shape=(None, src_vocab_size))
        encoder_lstm = LSTM(units=256, return_state=True)

        encoder_outputs, state_h, state_c = encoder_lstm(encoder_inputs)
        encoder_states = [state_h, state_c]

        # Defines the inputs and outputs of the decoder
        decoder_inputs = Input(shape=(None, tar_vocab_size))
        decoder_lstm = LSTM(units=256, return_sequences=True, return_state=True)
        decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)

        # Makes the decoder's first status - hidden status and cell status of the encoder
        decoder_softmax_layer = Dense(tar_vocab_size, activation='softmax')
        decoder_outputs = decoder_softmax_layer(decoder_outputs)

        # Finishes creating the model by compiling the model
        model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
        model.compile(optimizer="rmsprop", loss="categorical_crossentropy")

        # Trains for 50 epochs
        model.fit(x=[encoder_input, decoder_input], y=decoder_target, batch_size=64, epochs=50, validation_split=0.2)

        # Defines the encoder model
        encoder_model = Model(inputs=encoder_inputs, outputs=encoder_states)

        # Constructs the decoder
        # These are the tensors that store previous status
        # state_h: hidden state
        # state_c: cell state
        decoder_state_input_h = Input(shape=(256,))
        decoder_state_input_c = Input(shape=(256,))
        decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
        decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)

        # In order to predict the next word in the sentence,
        # uses initial_state as the previous status
        # This is implemented in decode_sequence() later
        decoder_states = [state_h, state_c]

        # state_h and state_c don't get discarded, which is different from when training
        decoder_outputs = decoder_softmax_layer(decoder_outputs)
        decoder_model = Model(inputs=[decoder_inputs] + decoder_states_inputs,
                              outputs=[decoder_outputs] + decoder_states)

        # Creates index_to_src와 index_to_tar dictionaries
        # which allows getting a word from an index, instead of an index from a word
        index_to_src = dict((i, char) for char, i in src_to_index.items())
        index_to_tar = dict((i, char) for char, i in tar_to_index.items())

        def decode_sequence(input_seq):
            # 입력으로부터 인코더의 상태를 얻음
            states_value = encoder_model.predict(input_seq)

            # <SOS>에 해당하는 원-핫 벡터 생성
            target_seq = np.zeros((1, 1, tar_vocab_size))
            target_seq[0, 0, tar_to_index['\t']] = 1.

            stop_condition = False
            decoded_sentence = ""

            # stop_condition이 True가 될 때까지 루프 반복
            while not stop_condition:
                # 이점 시점의 상태 states_value를 현 시점의 초기 상태로 사용
                output_tokens, h, c = decoder_model.predict([target_seq] + states_value)

                # 예측 결과를 문자로 변환
                sampled_token_index = np.argmax(output_tokens[0, -1, :])
                sampled_char = index_to_tar[sampled_token_index]

                # 현재 시점의 예측 문자를 예측 문장에 추가
                decoded_sentence += sampled_char

                # <eos>에 도달하거나 최대 길이를 넘으면 중단.
                if (sampled_char == '\n' or
                        len(decoded_sentence) > max_tar_len - 10):  # TODO: This needs work here - why - 10?
                    stop_condition = True

                # 현재 시점의 예측 결과를 다음 시점의 입력으로 사용하기 위해 저장
                target_seq = np.zeros((1, 1, tar_vocab_size))
                target_seq[0, 0, sampled_token_index] = 1.

                # 현재 시점의 상태를 다음 시점의 상태로 사용하기 위해 저장
                states_value = [h, c]

            return decoded_sentence

        for seq_index in [3, 50, 100, 300, 1001]:  # 입력 문장의 인덱스
            input_seq = encoder_input[seq_index: seq_index + 1]
            decoded_sentence = decode_sequence(input_seq)
            print(35 * "-")
            print('Input sentence:', lines.src[seq_index])
            print('Correct sentence:',
                  lines.tar[seq_index][1:len(lines.tar[seq_index]) - 1])  # Prints without '\t' and '\n'
            print('Translated sentence using the machine:',
                  decoded_sentence[:len(decoded_sentence) - 1])  # Prints without '\n'
