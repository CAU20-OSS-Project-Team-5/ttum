import usecase_model
import nlp

# excerpted from software engineering Ch.6 Use case page 3
# need to take out actor, scenario, use case
example_paragraph = u"""A customer arrives at a checkout with items to purchase. The 
cashier uses the POS system to record each purchased item. The system 
presents a running total and line-item details. The customer enters payment 
information, which the system validates and records. The system updates 
inventory. The customer receives a receipt from the system and then leaves 
with the items."""

paragraph = u"""The customer does checkout.
The checkouts require payment.
Help extends checkout.
Checkout is done by clerk."""

if __name__ == '__main__':
    try:
        model = usecase_model.Model()
        # model.train(10)
        model.restore_checkpoint()

        # Translate each sentence in paragraph
        nlp_handler = nlp.NLPHandler()
        sentences = nlp_handler.get_sentences(paragraph)

        translated_sentences = []
        for sentence in sentences:
            sentence = nlp_handler.remove_punctuations(sentence).lower()
            translated = nlp_handler.remove_start_end_from_translated_text(model.translate(sentence))
            translated_sentences.append(translated)
            print("Original: ", sentence)
            print("Translated: ", translated)

        # Get actor definition texts and translated texts
        actor_text = nlp_handler.get_plantuml_actor_sentence_list(paragraph)
        translated_text = nlp_handler.convert_list_to_lines(translated_sentences)

        # Print them
        print("Actor text: ")
        print(actor_text)
        print()
        print("Translated text: ")
        print(translated_text)
    except (AttributeError, TypeError) as e:
        pass
