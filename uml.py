import plantuml.plantuml as plantuml
import time
import os
import glob

# Path to save PlantUML text and image files

#if not exist result_files folder, make folder
try:
    if not os.path.exists("result_files"):
        os.mkdir("result_files")
        os.mkdir("result_files/texts")
        os.mkdir("result_files/diagrams")
except OSError:
    print("Error: Creating Directory results_files")

result_path = os.path.join('result_files')

# Path, name, and location of the PlantUML text file to save
text_file_path = os.path.join(result_path, 'texts')

# Path to save PlantUML result image file
image_file_path = os.path.join(result_path, 'diagrams')

# File name of the usecase PlantUML text file
usecase_file_name = 'usecase_diagram.plantuml'


def create_usecase_diagram_image(actor_text, relationship_text):
    """Create usecase diagram and return whether it was successful.

    :param actor_text: the actor text to go into the PlantUML text file for usecase diagram
    :param relationship_text: the relationship text to go into the PlantUML text file for usecase diagram
    :return: True if creating the image was successful, False if it was unsuccessful
    """
    # File name and location to save the uml results
    text_file_loc = os.path.join(text_file_path, usecase_file_name)

    # The location to save the PlantUML text file
    f = open(text_file_loc, 'w')

    plantuml_usecase_text = """@startuml
left to right direction
skinparam packageStyle rectangle
""" + actor_text + """
rectangle checkout {
""" + relationship_text + """
}
@enduml
"""

    # Create PlantUML file
    f.write(plantuml_usecase_text)
    f.close()
    time.sleep(1.0)

    is_successful = create_uml_diagram_image(usecase_file_name)
    return is_successful


def update_uml_diargram_image(plantuml_file_name):
    """Update PlantUML text file and create PlantUML image again.

    This function is used when the PlantUML text has been updated and the server needs to update the image as well.

    :param plantuml_file_name: the PlantUML file name to update to create the image
    :return: True if creating the image was successful, False if it was unsuccessful
    """
    is_successful = create_uml_diagram_image(plantuml_file_name)
    return is_successful


def create_uml_diagram_image(file_name):
    """Create UML diagram image by connecting to PlantUML Server, using python-plantuml module.

    :param file_name: the name of the PlantUML text file
    :return: True if creating the image was successful, False if it was unsuccessful
    """
    # File location to save the uml results
    text_file_loc = os.path.join(text_file_path, file_name)
    files = {'filename': [text_file_loc],
             'outfile': os.path.join(image_file_path, os.path.splitext(file_name)[0] + '.png'),
             'server': 'http://www.plantuml.com/plantuml/img/'}

    # Connect to PlantUML server
    plantuml_conn = plantuml.PlantUML(files['server'])

    # Get uml diagram image file generated from the PlantUML text file
    is_successful = plantuml_conn.processes_file(text_file_loc, outfile=files['outfile'])
    return is_successful


def cleanup_result_files():
    """Remove all of the files in result_files/diagrams/ and result_files/texts"""
    files = glob.glob(os.path.join(image_file_path, '*'))
    for f in files:
        os.remove(f)

    files = glob.glob(os.path.join(text_file_path, '*'))
    for f in files:
        os.remove(f)
