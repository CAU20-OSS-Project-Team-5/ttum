import usecase_model
import nlp
import uml

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
            translated_sentence = model.translate(sentence)
            translated_sentence = nlp_handler.remove_start_end_tags(translated_sentence)
            print("Translated after removal:", translated_sentence)
            translated_sentences.append(translated_sentence)
            # print("Original: ", sentence)
            # print("Translated: ", translated_sentence)

        # Get actor definition texts and translated texts
        actor_text = nlp_handler.get_actor_text(translated_sentences)
        translated_text = nlp_handler.convert_list_to_lines(translated_sentences)

        # Print them
        print("Actor text: ")
        print(actor_text)
        print()
        print("Translated text: ")
        print(translated_text)

        # Create PlantUML text and image file for usecase diagram
        uml.cleanup_result_files() # Clean up previous result files in the result folder
        is_successful = uml.create_usecase_diagram_image(actor_text, translated_text)
        if is_successful is True:
            print("Done creating usecase diagram image and text file.")
        else:
            print("There was an error with the file.")

    except (AttributeError, TypeError) as e:
        pass
