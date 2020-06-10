import nltk
import string


class NLPHandler:
    """Class to handle natural language processing in ttum"""

    def __init__(self):
        """Initialize the instance by downloading all NLTK data."""
        # Download all nltk data
        # nltk.download('all')
        return

    def get_sentences(self, paragraph):
        """Get newline-character-removed sentences as a list from paragraph.

        :param paragraph: the paragraph to convert to sentence list
        :return: the converted sentence list
        """
        sentences = [t for t in nltk.sent_tokenize(paragraph)]
        sentences = [x.replace('\n', '') for x in sentences]
        return sentences

    def get_words_of_sentences(self, paragraph):
        """Get a list of words in each sentence in a paragraph.

        :param paragraph: the paragraph to convert
        :return: a list of words in each sentence in the paragraph
        """
        sentences = self.get_sentences(paragraph)
        words_of_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        return words_of_sentences

    def get_tokens(self, paragraph):
        """Get POS-tagged tokens from a given paragraph.

        :param paragraph: the paragraph to convert to POS-tagged tokens
        :return: the converted token list of each sentence in the paragraph
        """
        # Splits the paragraph into sentences
        tokenized_sentences = self.get_sentences(paragraph)

        # Splits the sentences into tokenized words
        for i in range(0, len(tokenized_sentences)):
            token_list = [nltk.pos_tag(nltk.word_tokenize(t)) for t in tokenized_sentences]

        return token_list

    def convert_list_to_lines(self, list_of_string):
        """Convert a list of string into a line-separated text

        :param list_of_string: the list of string to convert into a single text
        :return: a single text that is converted from the given list of string
        """
        return """{}""".format("\n".join(list_of_string[0:]))

    def remove_punctuations(self, s):
        """Remove punctuations including ',', '.', ... from string s

        :param s: the string to remove punctuations from
        :return: the punctuation-removed string
        """
        text = s.translate(str.maketrans('', '', string.punctuation))
        return text

    def remove_start_end_tags(self, s):
        """Remove "<start> " and " <end>" from start and end of translated text s

        :param s: the translated text that may contain "<start> " and " <end>"
        :return: the translated text where "<start> " and " <end>" are removed
        """
        s.strip()

        if s.endswith(" <end>"):
            s = s[:-6]

        if s.endswith(" <end> "):
            s = s[:-7]

        if s.startswith("<start> "):
            s = s[8:]

        return s

    def get_actor_list(self, translated_sentences):
        """Get a list of from translated text, by only extracting 'actor' from translated text "actor -- (usecase)"

        :param translated_sentences: the translated text where the actor text will be extracted
        :return: the list of actor extracted from the translated text
        """
        temp_list = [t.split(' ') for t in translated_sentences]  # Split each sentence into items of words
        actor_list = []

        for s in temp_list:  # Get each sentence
            if len(s) > 2:  # Execute only when each string has 3 or more words
                for i in (0, 2):  # Check first and third item in the sentence
                    candidate = s[i]  # candidate for an actor
                    # If the item is not surrounded by '(' and ')', it is an actor
                    if candidate.startswith('(') is False and candidate.endswith(')') is False:
                        actor_list.append(candidate)

        return actor_list

    def get_actor_text(self, translated_sentences):
        """Get a PlantUML-ready actor text to be inserted into actor definitions in PlantUML usecase diagram file.

        This means extracting actors from the translated text and appending "actor " to each item in the actor list,
        and creating a single text that is ready to be inserted into a PlantUML text file for usecase diagram.

        :param translated_sentences: the list of translated sentences to be converted into an actor definition text
        :return: a PlantUML-usecase-diagram text to be inserted into actor definitions
        """
        # Remove POS-tags from subject list
        subjects = self.get_actor_list(translated_sentences)

        # Remove redundant words
        actors = sorted(set(subjects), key=lambda x: subjects.index(x))

        # Finally, get PlantUML-ready actor text
        actor_appended_list = ['actor ' + item for item in actors]  # Append "actor " to each actor texts
        actor_text = self.convert_list_to_lines(actor_appended_list)  # Convert to a whole paragraph
        return actor_text
