import nltk


class NLPHandler:
    def __init__(self):
        # Download all nltk data
        nltk.download('all')
        return

    def get_sentences(self, paragraph):
        sentences = [t for t in nltk.sent_tokenize(paragraph)]
        sentences = [x.replace('\n', '') for x in sentences]
        return sentences

    def get_words_of_sentences(self, paragraph):
        sentences = self.get_sentences(paragraph)
        words_of_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        return words_of_sentences

    def get_tokens(self, paragraph):
        # Splits the paragraph into sentences
        tokenized_sentences = self.get_sentences(paragraph)

        # Splits the sentences into tokenized words
        for i in range(0, len(tokenized_sentences)):
            tokens = [nltk.pos_tag(nltk.word_tokenize(t)) for t in tokenized_sentences]

        return tokens
