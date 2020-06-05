from uml_handler import UMLHandler

example_paragraph = u"""The customer does checkout.
The checkouts require payment.
Help extends checkout.
Checkout is done by clerk."""

if __name__ == '__main__':
    uml_handler = UMLHandler(train_epoch=0)
    # Convert paragraph into usecase diagram image
    is_successful = uml_handler.convert_into_usecase_uml(example_paragraph)

    # Update the usecase diagram image with user-updated PlantUML text
    is_successful = uml_handler.update_usecase_uml()
    print("Done updating the image with the new PlantUML text file.")
