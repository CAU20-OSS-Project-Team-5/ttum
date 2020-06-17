# Text-to-UML: TTUM
<p align="center">
<img width="300" alt="ttum_logo" src="https://user-images.githubusercontent.com/42485462/84795485-8554c500-b032-11ea-80b8-1d882ea9cc3c.png">
</p>


## What It Does
<p align="center">
<img width="600" alt="ttum_logo_sketch" src="https://user-images.githubusercontent.com/42485462/84044589-bdc92300-a9e2-11ea-8b79-85bcd7e3c76b.png">
</p>

TTUM is a program that converts sentences in natural language into a UML diagram image, using deep learning.


## Installation
- Run:
```shell
$ python -m venv .venv                  # Create virtual environment
$ .venv/bin/activate                    # or '.venv\Scripts\activate' on Windows
$ pip install --upgrade pip             # or 'python -m pip install --upgrade pip' on Windows to update pip
$ pip install -r requirements.txt       # Get packages using requirements.txt
```

### Frontend (Run on frontend/)
- Install [npm](https://www.npmjs.com/).

- Run *this* to install react-scripts and axios.
```shell
$ cd frontend
$ npm install --save react-scripts # Install react-scripts
$ npm install --save axios # Install axios
```

### Backend (Run on backend/)
- Remove files other than `__init__.py` from `ttum/backend/api/migrations/`.
- Set up database
```shell
$ cd backend
$ py manage.py makemigrations
$ py manage.py migrate
$ py manage.py createsuperuser # Create superuser for the server
```
- Create and save any value to `title`, `image_name`, `_type` to a row in `Task` table in the SQLite database on `localhost:8020/admin`.

### Download [NLTK](https://www.nltk.org/) Data
You need to download **NLTK data** to use the `nlp` module.
1. You need to *uncomment* `nltk.download('all')` in `NLPHandler.__init__` in `nlp.py` when you run for the first time.
2. When you run the program with the uncommented line, the program will download NLTK data from the NLTK server.
3. Then, you can *comment* the line again.

### Create Training Checkpoints
- In order to use the model to translate natural language to PlantUML text, you need to train the model with the `train.csv`.
- Give `epoch` parameter of `UMLHandler` an **integer more than 0** at least **once**, to train the model and create checkpoints in `training_checkpoints/`.
  - We recommend assigning a number bigger than 300 to the `epoch`.
- Then, you can set `epoch=0` again, so that the program can just restore the checkpoints to translate next time you run it.
- If there is any change in `train.csv`, you need to train the model again.

## Running the Server
You need to run both the backend and frontend servers, if you wish to run TTUM on web.

### Backend
```shell
$ cd backend
$ py manage.py runserver 127.0.0.1:8020
```

### Frontend
```shell
$ cd frontend
$ npm run start
```

## Running Only the Deep Learning Model
If you wish to run without the server, just run `main.py` in the `backend/nlp/`, which is a short demo of the image creating process.

## Files and Folders
### uml_model and usecase_model.py
- A tensorflow model utilizing **seq2seq**
- Receives `train.csv` as input and trains the model.

### Training Data File (.csv)
#### train.csv
- A data file that contains the training data for the model
- This is a file where English-to-PlantUML data should be added.
- Please add more quality data!

## Note
- This project works by connecting to the [PlantUML](https://plantuml.com/) server.
- We used [SamuelMarks/python-plantuml](https://github.com/SamuelMarks/python-plantuml), which is forked from [dougn/python-plantuml](https://github.com/dougn/python-plantuml) to get access to the PlantUML server using Python!
- These are all open source projects on GitHub, so check them out!

- Currently **TTUM** only works for creating usecase diagrams, so please participate in the project.
