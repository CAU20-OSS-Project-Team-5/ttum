# Text-to-UML: TTUM
<p align="center">
<img width="300" alt="ttum_logo" src="https://user-images.githubusercontent.com/42485462/84795485-8554c500-b032-11ea-80b8-1d882ea9cc3c.png">
</p>

## What It Does
<p align="center">
<img width="600" alt="ttum_logo_sketch" src="https://user-images.githubusercontent.com/42485462/84044589-bdc92300-a9e2-11ea-8b79-85bcd7e3c76b.png">
</p>

자연어 처리 및 딥러닝을 이용하여 자연어 문단을 UML 다이어그램으로 변환시켜주는 프로그램

## Installation
```shell
$ python -m venv .venv                  # Create virtual environment
$ .venv/bin/activate                    # or '.venv\Scripts\activate' on Windows
$ pip install --upgrade pip             # Update pip - or 'python -m pip install --upgrade pip' on Windows
$ pip install -r requirements.txt       # Get packages using requirements.txt
```

## Initial Setups
### Download NLTK Data
- You need to download **NLTK data** to use the `nlp` module.
1. You need to *uncomment* `nltk.download('all')` in `NLPHandler.__init__` in `nlp.py` when you run for the first time.
2. When you run the program with the uncommented line, the program will download NLTK data from the NLTK server.
3. Then, you can *comment* the line again.

### Create Training Checkpoints
- In order to use the model to translate natural language to PlantUML text, you need to train the model with the `train.csv`.
- Give `epoch` parameter of `UMLHandler` an **integer more than 0** at least **once**, to train the model and create checkpoints in `training_checkpoints/`.
- Then, you can set `epoch=0` again, so that the program can just restore the checkpoints to translate next time you run it.
- If there is any change in `train.csv`, you need to train the model again.


## 파일 및 폴더 설명
### jupyter 폴더
- Jupyter notebook 파일들이 담겨있는 폴더
- Model test 및 학습 용도로 사용하면 됨

Django의 view.py 의 taskCreate(request)에서 입력된 문장을 이미지파일의 url 주소로 변환하여 주면 됨.


### usecase_model.py
- RNN의 파생 모델인 LSTM 모델이 적용된 Tensorflow model
- seq2seq 기법 및 교사 강요 사용
- 현재 생성자를 통해 동작하며, `main.py`에서 호출
- 입력으로 train.csv를 받아서 LSTM 모델을 학습시킴

### packagelist.txt
- 아나콘다의 conda install을 위한 패키지 정보들

### 데이터 파일 (.csv)
#### train.csv
- Tensorflow를 이용해 학습시킬 데이터가 담긴 csv 파일
- 이 파일에 영어-PlantUML 데이터를 추가해야 함
- 오픈소스의 의의가 됨

#### test.csv
- 학습되지 않은 영어-PlantUML 데이터
- 정확도 측정을 위해 사용
#### 인용한 오픈소스
- https://github.com/SamuelMarks/python-plantuml
- Opensource plantuml api for python
