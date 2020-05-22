import nltk


class NLPHandler:
    def __init__(self, paragraph):
        # Download all nltk data
        nltk.download('all')

        # Initialize the paragraph
        self.paragraph = paragraph

    def get_tokens(self):
        # Splits the paragraph into sentences
        tokenized_sentences = [t for t in nltk.sent_tokenize(self.paragraph)]
        tokenized_sentences = [x.replace('\n', '') for x in tokenized_sentences]

        # Splits the sentences into tokenized words
        for i in range(0, len(tokenized_sentences)):
            tokens = [nltk.pos_tag(nltk.word_tokenize(t)) for t in tokenized_sentences]

        return tokens
