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

### main.py
- 메인 함수가 담겨있음
- usecase_model의 Model 클래스 생성자를 호출
- Model 클래스의 train 함수에 매개변수로 epoch 값을 넘기고, 해당 횟수만큼 학습
- Model 클래스의 translate 함수로 사용자 입력을 번역함

### nlp.py
- nltk 패키지를 불러와서 NLPHandler 클래스를 불러와 자연어 처리 관련 함수를 사용할 수 있음
- 생성자가 nltk.download('all')을 실행하여 nltk data를 다운받음
    - 다운받은 상태면 다운받지는 않지만 확인 메세지들이 콘솔창에 출력됨
    - 추후에 미리 체크해서 다운 받을 필요가 없으면 출력하지 않도록 할 예정

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
