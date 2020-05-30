import nltk
import spacy


class NLPHandler:
    def __init__(self):
        # Download all nltk data
        # nltk.download('all')
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
            token_list = [nltk.pos_tag(nltk.word_tokenize(t)) for t in tokenized_sentences]

        return token_list

    def get_nouns(self, pos_tagged_sentence):
        noun_list = [item for item in pos_tagged_sentence if item[1] == 'NN' or item[1] == 'NNS']
        return noun_list

    def get_nouns_from_paragraph(self, paragraph):
        # Get only nouns from paragraph and flatten the 2D tuple list to 1D tuple list
        # Result: [(<word_1>, 'NN'), (<word_2>, 'NNS'), (<word_3>, 'NN'), ..., (<word_n>, 'NN')]
        noun_list = sum([nlp_handler.get_nouns(t) for t in nlp_handler.get_tokens(paragraph)], [])
        return noun_list

    def get_subjects_from_paragraph_except_pronouns(self, paragraph):
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

    def get_pos_removed_list(self, list):
        pos_removed_list = [li[0] for li in list]
        return pos_removed_list

    def preprocess_actor(self, actor_list):
        actor_appended_list = ['actor ' + item for item in actor_list]
        return actor_appended_list

    def convert_list_to_lines(self, list):
        return """{}""".format("\n".join(list[0:]))


if __name__ == '__main__':
    example_paragraph = u"""A customer arrives at a checkout with items to purchase. The 
    cashier uses the POS system to record each purchased item. The system 
    presents a running total and line-item details. The customer enters payment 
    information, which the system validates and records. The system updates 
    inventory. The customer receives a receipt from the system and then leaves 
    with the items. Now they don't want it."""

    nlp_handler = NLPHandler()

    # Get POS-tagged subjects from paragraph
    pos_subjects = nlp_handler.get_subjects_from_paragraph_except_pronouns(example_paragraph)
    print("POS-tagged subjects: ", pos_subjects)

    # Remove POS-tags from subject list
    subjects = nlp_handler.get_pos_removed_list(pos_subjects)
    print("subjects: ", subjects)

    # Remove redundant words
    actors = sorted(set(subjects), key=lambda x: subjects.index(x))
    print("actors: ", actors)

    # Finally, get PlantUML-ready actor text
    actor_text_list = nlp_handler.preprocess_actor(actors)
    plantuml_ready_actor_text = nlp_handler.convert_list_to_lines(actor_text_list)
    print("PlantUML-ready actor text: ")
    print(plantuml_ready_actor_text)
