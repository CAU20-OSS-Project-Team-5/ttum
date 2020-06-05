import usecase_model
import nlp
import uml


class UMLHandler():
    def __init__(self, train_epoch=10):
        """Initialize UMLHandler by reloading the trained model

        :param train_epoch: the number of epoch to train (if 0, there will be no training)
        """
        self.model = usecase_model.Model()

        # Train only if the given epoch is bigger than 0
        if train_epoch > 0:
            self.model.train(train_epoch)

        # Restore checkpoints
        self.model.restore_checkpoint()

    def convert_into_usecase_uml(self, paragraph):
        """Convert paragraph into usecase diagram image and save the image in the server

        :param paragraph: the paragraph to translate into PlantUML usecase diagram image
        :return: boolean value of whether the converting process has been successful
        """
        is_successful = False
        try:
            # Translate each sentence in paragraph
            nlp_handler = nlp.NLPHandler()
            sentences = nlp_handler.get_sentences(paragraph)

            translated_sentences = []
            for sentence in sentences:
                sentence = nlp_handler.remove_punctuations(sentence).lower()
                translated_sentence = self.model.translate(sentence)
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
            uml.cleanup_result_files()  # Clean up previous result files in the result folder
            is_successful = uml.create_usecase_diagram_image(actor_text, translated_text)
            if is_successful is True:
                print("Done creating usecase diagram image and text file.")
            else:
                print("There was an error with the file.")

        except (AttributeError, TypeError) as e:
            pass

        return is_successful

    def update_usecase_uml(self):
        """Update the usecase UML diagram image with the user-updated PlantUML text

        @return: boolean value of whether the converting process has been successful
        """
        is_successful = uml.update_uml_diargram_image(uml.usecase_file_name)

        return is_successful
