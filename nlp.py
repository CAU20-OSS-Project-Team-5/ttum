import nltk
import spacy
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

    def get_nouns_from_pos_sentence(self, pos_tagged_sentence):
        """Get nouns from a POS-tagged sentence.

        :param pos_tagged_sentence: the POS-tagged sentence to extract nouns from
        :return: a list of nouns from the POS-tagged sentence
        """
        noun_list = [item for item in pos_tagged_sentence if item[1] == 'NN' or item[1] == 'NNS']
        return noun_list

    def get_nouns_from_paragraph(self, paragraph):
        """Get a list of nouns from a paragraph.

        :param paragraph: the paragraph to extract nouns from
        :return: a list of nouns from the paragraph
        """
        # Get only nouns from paragraph and flatten the 2D tuple list to 1D tuple list
        # Result: [(<word_1>, 'NN'), (<word_2>, 'NNS'), (<word_3>, 'NN'), ..., (<word_n>, 'NN')]
        noun_list = sum([self.get_nouns_from_pos_sentence(t) for t in self.get_tokens(paragraph)], [])
        return noun_list

    def get_subjects_from_paragraph_except_pronouns(self, paragraph):
        """Get a list of nouns from a paragraph, except for pronouns.

        Run `python -m spacy download en_core_web_sm` if this throws error.

        :param paragraph: the paragraph to extract nouns from
        :return: a list of nouns from the paragraph, except for pronouns
        """
        # Run `python -m spacy download en_core_web_sm` for this to run
        spacy_nlp = spacy.load('en_core_web_sm')  # Load NLP for spaCy for English
        doc = spacy_nlp(paragraph)

        # Take out subjects from paragraph
        sub_toks = [tok for tok in doc if (tok.dep_ == 'nsubj' or tok.dep == 'iobj' or tok.dep == 'dobj')]
        subjects = [token.orth_ for token in sub_toks]  # Change spaCy vectors to string

        # Remove pronouns
        # Create a temporary text of subjectss
        subject_text = ""
        for s in subjects:
            subject_text += s + " "

        return self.get_nouns_from_paragraph(subject_text)

    def get_pos_removed_word_list(self, pos_tagged_word_list):
        """Remove POS tags from a POS-tagged word list

        :param pos_tagged_word_list: the POS-tagged word list to remove POS tags from
        :return: the POS-tags-removed word list
        """
        pos_removed_word_list = [li[0] for li in pos_tagged_word_list]
        return pos_removed_word_list

    def convert_list_to_lines(self, list_of_string):
        """Convert a list of string into a line-separated text

        :param list_of_string: the list of string to convert into a single text
        :return: a single text that is converted from the given list of string
        """
        return """{}""".format("\n".join(list_of_string[0:]))

    def get_plantuml_actor_sentence_list(self, paragraph):
        """Get a PlantUML-ready text to be inserted into actor definitions in PlantUML usecase diagram file.

        This means extracting subjects from the given paragraph, appending "actor " to each subject,
        and creating a single text that is ready to be inserted into a PlantUML text file for usecase diagram.

        :param paragraph: the original paragraph to be converted into a PlantUML-ready actor definition text
        :return: a PlantUML-usecase-diagram text to be inserted into actor definitions
        """
        # Get POS-tagged subjects from paragraph
        pos_subjects = self.get_subjects_from_paragraph_except_pronouns(example_paragraph)

        # Remove POS-tags from subject list
        subjects = self.get_pos_removed_word_list(pos_subjects)

        # Remove redundant words
        actors = sorted(set(subjects), key=lambda x: subjects.index(x))

        # Finally, get PlantUML-ready actor text
        actor_appended_list = ['actor ' + item for item in actors]  # Append "actor " to each actor texts
        plantuml_ready_actor_text = self.convert_list_to_lines(actor_appended_list)  # Convert to a whole paragraph
        return plantuml_ready_actor_text

    def remove_punctuations(self, s):
        """Remove punctuations including ',', '.', ... from string s

        :param s: the string to remove punctuations from
        :return: the punctuation-removed string
        """
        text = s.translate(str.maketrans('', '', string.punctuation))
        return text

    def remove_start_end_from_translated_text(self, s):
        """Remove "<start> " and " <end>" from start and end of translated text s

        :param s: the translated text that may contain "<start> " and " <end>"
        :return: the translated text where "<start> " and " <end>" are removed
        """
        if s.endswith(" <end>"):
            s = s[:-6]

        if s.startswith("<start> "):
            s = s[8:]

        return s


if __name__ == '__main__':
    example_paragraph = u"""A customer arrives at a checkout with items to purchase. The 
    cashier uses the POS system to record each purchased item. The system 
    presents a running total and line-item details. The customer enters payment 
    information, which the system validates and records. The system updates 
    inventory. The customer receives a receipt from the system and then leaves 
    with the items. Now they don't want it."""

    nlp_handler = NLPHandler()
    plantuml_ready_actor_text = nlp_handler.get_plantuml_actor_sentence_list(example_paragraph)
    print("PlantUML-ready actor text: ")
    print(plantuml_ready_actor_text)
