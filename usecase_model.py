import tensorflow as tf

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.model_selection import train_test_split

import re
import numpy as np
import os
import io
import time

path_to_file = "usecase_data/train.csv"


class Model():
    def __init__(self):
        en, pu = self.create_dataset(path_to_file, None)
        print(en[-1])
        print(pu[-1])

        # Limit the size of the dataset to experiment faster (optional)
        # Try experimenting with the size of that dataset
        num_examples = 30000
        input_tensor, target_tensor, self.inp_lang, self.targ_lang = self.load_dataset(path_to_file, num_examples)

        # Calculate max_length of the target tensors
        self.max_length_targ, self.max_length_inp = target_tensor.shape[1], input_tensor.shape[1]

        # Creating training and validation sets using an 80-20 split
        input_tensor_train, input_tensor_val, target_tensor_train, target_tensor_val = train_test_split(input_tensor,
                                                                                                        target_tensor,
                                                                                                        test_size=0.2)

        # Show length
        print(len(input_tensor_train), len(target_tensor_train), len(input_tensor_val), len(target_tensor_val))

        print("Input Language; index to word mapping")
        self.convert(self.inp_lang, input_tensor_train[0])
        print()
        print("Target Language; index to word mapping")
        self.convert(self.targ_lang, target_tensor_train[0])

        # Create a tf.data dataset
        BUFFER_SIZE = len(input_tensor_train)
        self.BATCH_SIZE = 64
        self.steps_per_epoch = len(input_tensor_train) // self.BATCH_SIZE
        self.embedding_dim = 256
        self.units = 1024
        self.vocab_inp_size = len(self.inp_lang.word_index) + 1
        self.vocab_tar_size = len(self.targ_lang.word_index) + 1

        self.dataset = tf.data.Dataset.from_tensor_slices((input_tensor_train, target_tensor_train)).shuffle(
            BUFFER_SIZE)
        self.dataset = self.dataset.batch(self.BATCH_SIZE, drop_remainder=True)

        example_input_batch, example_target_batch = next(iter(self.dataset))
        print(example_input_batch.shape, example_target_batch.shape)

        self.encoder = Encoder(self.vocab_inp_size, self.embedding_dim, self.units, self.BATCH_SIZE)

        # sample input
        # Create encoder
        sample_hidden = self.encoder.initialize_hidden_state()
        sample_output, sample_hidden = self.encoder(example_input_batch, sample_hidden)
        print('Encoder output shape: (batch size, sequence length, units) {}'.format(sample_output.shape))
        print('Encoder Hidden state shape: (batch size, units) {}'.format(sample_hidden.shape))

        attention_layer = BahdanauAttention(10)
        attention_result, attention_weights = attention_layer(sample_hidden, sample_output)

        print("Attention result shape: (batch size, units) {}".format(attention_result.shape))
        print("Attention weights shape: (batch_size, sequence_length, 1) {}".format(attention_weights.shape))

        # Create decoder
        self.decoder = Decoder(self.vocab_tar_size, self.embedding_dim, self.units, self.BATCH_SIZE)

        sample_decoder_output, _, _ = self.decoder(tf.random.uniform((self.BATCH_SIZE, 1)),
                                                   sample_hidden, sample_output)

        print('Decoder output shape: (batch_size, vocab size) {}'.format(sample_decoder_output.shape))

        # Define the optimizer and the loss function
        self.optimizer = tf.keras.optimizers.Adam()
        self.loss_object = tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=True, reduction='none')

        # Checkpoints (Object-based saving)
        self.checkpoint_dir = './training_checkpoints'
        self.checkpoint_prefix = os.path.join(self.checkpoint_dir, "ckpt")
        self.checkpoint = tf.train.Checkpoint(optimizer=self.optimizer,
                                              encoder=self.encoder,
                                              decoder=self.decoder)

    def preprocess_sentence(self, w, split_on_special_chars=False):
        # creating a space between a word and the punctuation following it
        # eg: "he is a boy." => "he is a boy ."
        # Reference:- https://stackoverflow.com/questions/3645931/python-padding-punctuation-with-white-spaces-keeping-punctuation
        if split_on_special_chars:
            w = re.sub(r"([?.!,¿])", r" \1 ", w)
            w = re.sub(r'[" "]+', " ", w)

            # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
            w = re.sub(r"[^a-zA-Z?.!,¿]+", " ", w)

        w = w.strip()

        #   # adding a start and an end token to the sentence
        #   # so that the model know when to start and stop predicting.
        w = '<start> ' + w + ' <end>'
        return w

    # 1. Remove the accents
    # 2. Clean the sentences
    # 3. Return word pairs in the format: [ENGLISH, SPANISH]
    def create_dataset(self, path, num_examples):
        # Split each line by '\n'
        # Skip first line
        lines = io.open(path, encoding='UTF-8').read().strip().split('\n')[1:]

        # Generate input and output layers
        word_pairs = []
        for l in lines[:num_examples]:
            sentences = l.split(',')
            input_data = self.preprocess_sentence(sentences[0], split_on_special_chars=True)
            output_data = self.preprocess_sentence(sentences[1], split_on_special_chars=False)
            word_pairs.append([input_data, output_data])

        return zip(*word_pairs)

    def tokenize(self, lang):
        lang_tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='')
        lang_tokenizer.fit_on_texts(lang)

        tensor = lang_tokenizer.texts_to_sequences(lang)

        tensor = tf.keras.preprocessing.sequence.pad_sequences(tensor, padding='post')

        return tensor, lang_tokenizer

    def load_dataset(self, path, num_examples=None):
        # creating cleaned input, output pairs
        inp_lang, targ_lang = self.create_dataset(path, num_examples)

        input_tensor, inp_lang_tokenizer = self.tokenize(inp_lang)
        target_tensor, targ_lang_tokenizer = self.tokenize(targ_lang)

        return input_tensor, target_tensor, inp_lang_tokenizer, targ_lang_tokenizer

    def convert(self, lang, tensor):
        for t in tensor:
            if t != 0:
                print("%d ----> %s" % (t, lang.index_word[t]))

    def loss_function(self, real, pred):
        mask = tf.math.logical_not(tf.math.equal(real, 0))
        loss_ = self.loss_object(real, pred)

        mask = tf.cast(mask, dtype=loss_.dtype)
        loss_ *= mask

        return tf.reduce_mean(loss_)

    @tf.function
    def train_step(self, inp, targ, enc_hidden):
        loss = 0

        with tf.GradientTape() as tape:
            enc_output, enc_hidden = self.encoder(inp, enc_hidden)

            dec_hidden = enc_hidden

            dec_input = tf.expand_dims([self.targ_lang.word_index['<start>']] * self.BATCH_SIZE, 1)

            # Teacher forcing - feeding the target as the next input
            for t in range(1, targ.shape[1]):
                # passing enc_output to the decoder
                predictions, dec_hidden, _ = self.decoder(dec_input, dec_hidden, enc_output)

                loss += self.loss_function(targ[:, t], predictions)

                # using teacher forcing
                dec_input = tf.expand_dims(targ[:, t], 1)

        batch_loss = (loss / int(targ.shape[1]))

        variables = self.encoder.trainable_variables + self.decoder.trainable_variables

        gradients = tape.gradient(loss, variables)

        self.optimizer.apply_gradients(zip(gradients, variables))

        return batch_loss

    # Training
    # 1. Pass the input through the encoder which return encoder output and the encoder hidden state.
    # 2. The encoder output, encoder hidden state and the decoder input (which is the start token) is passed to the decoder.
    # 3. The decoder returns the predictions and the decoder hidden state.
    # 4. The decoder hidden state is then passed back into the model and the predictions are used to calculate the loss.
    # 5. Use teacher forcing to decide the next input to the decoder.
    # 6. Teacher forcing is the technique where the target word is passed as the next input to the decoder.
    # 7. The final step is to calculate the gradients and apply it to the optimizer and backpropagate.
    def train(self, epoch):
        EPOCHS = epoch

        for epoch in range(EPOCHS):
            start = time.time()

            enc_hidden = self.encoder.initialize_hidden_state()
            total_loss = 0

            for (batch, (inp, targ)) in enumerate(self.dataset.take(self.steps_per_epoch)):
                batch_loss = self.train_step(inp, targ, enc_hidden)
                total_loss += batch_loss

                if batch % 100 == 0:
                    print('Epoch {} Batch {} Loss {:.4f}'.format(epoch + 1,
                                                                 batch,
                                                                 batch_loss.numpy()))
            # saving (checkpoint) the model every 2 epochs
            if (epoch + 1) % 2 == 0:
                self.checkpoint.save(file_prefix=self.checkpoint_prefix)

            print('Epoch {} Loss {:.4f}'.format(epoch + 1,
                                                total_loss / self.steps_per_epoch))
            print('Time taken for 1 epoch {} sec\n'.format(time.time() - start))

    # Translate
    # - The evaluate function is similar to the training loop, except we don't use teacher forcing here. The input to the decoder at each time step is its previous predictions along with the hidden state and the encoder output.
    # - Stop predicting when the model predicts the end token.
    # - And store the attention weights for every time step.

    def evaluate(self, sentence):
        attention_plot = np.zeros((self.max_length_targ, self.max_length_inp))

        sentence = self.preprocess_sentence(sentence)

        inputs = [self.inp_lang.word_index[i] for i in sentence.split(' ')]
        inputs = tf.keras.preprocessing.sequence.pad_sequences([inputs],
                                                               maxlen=self.max_length_inp,
                                                               padding='post')
        inputs = tf.convert_to_tensor(inputs)

        result = ''

        hidden = [tf.zeros((1, self.units))]
        enc_out, enc_hidden = self.encoder(inputs, hidden)

        dec_hidden = enc_hidden
        dec_input = tf.expand_dims([self.targ_lang.word_index['<start>']], 0)

        for t in range(self.max_length_targ):
            predictions, dec_hidden, attention_weights = self.decoder(dec_input,
                                                                      dec_hidden,
                                                                      enc_out)

            # storing the attention weights to plot later on
            attention_weights = tf.reshape(attention_weights, (-1,))
            attention_plot[t] = attention_weights.numpy()

            predicted_id = tf.argmax(predictions[0]).numpy()

            result += self.targ_lang.index_word[predicted_id] + ' '

            if self.targ_lang.index_word[predicted_id] == '<end>':
                return result, sentence, attention_plot

            # the predicted ID is fed back into the model
            dec_input = tf.expand_dims([predicted_id], 0)

        return result, sentence, attention_plot

    # function for plotting the attention weights
    def plot_attention(self, attention, sentence, predicted_sentence):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(1, 1, 1)
        ax.matshow(attention, cmap='viridis')

        fontdict = {'fontsize': 14}

        ax.set_xticklabels([''] + sentence, fontdict=fontdict, rotation=90)
        ax.set_yticklabels([''] + predicted_sentence, fontdict=fontdict)

        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

        plt.show()

    def translate(self, sentence):
        result, sentence, attention_plot = self.evaluate(sentence)

        print('Input: %s' % (sentence))
        print('Predicted translation: {}'.format(result))

        attention_plot = attention_plot[:len(result.split(' ')), :len(sentence.split(' '))]
        self.plot_attention(attention_plot, sentence.split(' '), result.split(' '))

    # Restore the latest checkpoint and test
    # restoring the latest checkpoint in checkpoint_dir
    def restore_checkpoint(self):
        self.checkpoint.restore(tf.train.latest_checkpoint(self.checkpoint_dir))


# Write the encoder and decoder model
class Encoder(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, enc_units, batch_sz):
        super(Encoder, self).__init__()
        self.batch_sz = batch_sz
        self.enc_units = enc_units
        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.gru = tf.keras.layers.GRU(self.enc_units,
                                       return_sequences=True,
                                       return_state=True,
                                       recurrent_initializer='glorot_uniform')

    def call(self, x, hidden):
        x = self.embedding(x)
        output, state = self.gru(x, initial_state=hidden)
        return output, state

    def initialize_hidden_state(self):
        return tf.zeros((self.batch_sz, self.enc_units))


class BahdanauAttention(tf.keras.layers.Layer):
    def __init__(self, units):
        super(BahdanauAttention, self).__init__()
        self.W1 = tf.keras.layers.Dense(units)
        self.W2 = tf.keras.layers.Dense(units)
        self.V = tf.keras.layers.Dense(1)

    def call(self, query, values):
        # query hidden state shape == (batch_size, hidden size)
        # query_with_time_axis shape == (batch_size, 1, hidden size)
        # values shape == (batch_size, max_len, hidden size)
        # we are doing this to broadcast addition along the time axis to calculate the score
        query_with_time_axis = tf.expand_dims(query, 1)

        # score shape == (batch_size, max_length, 1)
        # we get 1 at the last axis because we are applying score to self.V
        # the shape of the tensor before applying self.V is (batch_size, max_length, units)
        score = self.V(tf.nn.tanh(
            self.W1(query_with_time_axis) + self.W2(values)))

        # attention_weights shape == (batch_size, max_length, 1)
        attention_weights = tf.nn.softmax(score, axis=1)

        # context_vector shape after sum == (batch_size, hidden_size)
        context_vector = attention_weights * values
        context_vector = tf.reduce_sum(context_vector, axis=1)

        return context_vector, attention_weights


class Decoder(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, dec_units, batch_sz):
        super(Decoder, self).__init__()
        self.batch_sz = batch_sz
        self.dec_units = dec_units
        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.gru = tf.keras.layers.GRU(self.dec_units,
                                       return_sequences=True,
                                       return_state=True,
                                       recurrent_initializer='glorot_uniform')
        self.fc = tf.keras.layers.Dense(vocab_size)

        # used for attention
        self.attention = BahdanauAttention(self.dec_units)

    def call(self, x, hidden, enc_output):
        # enc_output shape == (batch_size, max_length, hidden_size)
        context_vector, attention_weights = self.attention(hidden, enc_output)

        # x shape after passing through embedding == (batch_size, 1, embedding_dim)
        x = self.embedding(x)

        # x shape after concatenation == (batch_size, 1, embedding_dim + hidden_size)
        x = tf.concat([tf.expand_dims(context_vector, 1), x], axis=-1)

        # passing the concatenated vector to the GRU
        output, state = self.gru(x)

        # output shape == (batch_size * 1, hidden_size)
        output = tf.reshape(output, (-1, output.shape[2]))

        # output shape == (batch_size, vocab)
        x = self.fc(output)

        return x, state, attention_weights
