from uml_handler import UMLHandler
import uuid


example_paragraph = u"""The customer does checkout.
The checkouts require payment.
Help extends checkout.
Checkout is done by clerk."""

if __name__ == '__main__':
    # Create hash code
    hash = uuid.uuid4().hex
    hashed_plantuml_file_name = str(hash) + '.plantuml'
    print("Hashed file name: " + hashed_plantuml_file_name)

    uml_handler = UMLHandler(train_epoch=0)
    # Convert paragraph into usecase diagram image
    is_successful = uml_handler.convert_into_usecase_uml(example_paragraph, usecase_file_name=hashed_plantuml_file_name)

    # Update the usecase diagram image with user-updated PlantUML text
    is_successful = uml_handler.update_usecase_uml(usecase_file_name=hashed_plantuml_file_name)

    # Cleanup usecase diagram images and texts from 'result_files/'
    uml_handler.cleanup_plantuml_files(plantuml_text_file_name=hashed_plantuml_file_name)
    print("Done updating the image with the new PlantUML text file.")
