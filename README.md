# Opensource_PlantUml
Opensource_PlantUml team_project

## 파일 및 폴더 설명
### jupyter 폴더
- Jupyter notebook 파일들이 담겨있는 폴더
- Model test 및 학습 용도로 사용하면 됨

### main.py
- 메인 함수가 담겨있음
- 현재 비어있는 상태

### nlp.py
- nltk 패키지를 불러와서 NLPHandler 클래스를 불러와 자연어 처리 관련 함수를 사용할 수 있음
- 생성자가 nltk.download('all')을 실행하여 nltk data를 다운받음
    - 다운받은 상태면 다운받지는 않지만 확인 메세지들이 콘솔창에 출력됨
    - 추후에 미리 체크해서 다운 받을 필요가 없으면 출력하지 않도록 할 예정

### usecase_model.py
- RNN의 파생 모델인 LSTM 모델이 적용된 Tensorflow model
- seq2seq 기법 및 교사 강요 사용
- 현재 생성자를 통해 동작함 (추후 함수 추가 예정)
- 입력으로 train.csv를 받아서 LSTM 모델을 학습시킴
- 현재 사용자 입력을 받아서 번역하는 함수가 부재 상태
- 현재 입력에선 오류가 없어보이나 출력에서 오류가 있음
    - usecase_model.py의 마지막 부분인 decode_sequence 함수에서
        ```python
        if (sampled_char == '\n' or
                len(decoded_sentence) > max_tar_len - 10):  # TODO: This needs work here - why - 10?
            stop_condition = True
        ```
        - 현재 max_tar_len에서 -10을 해줘야 동작하는데, 원래는 -10을 하면 출력 언어가 잘려서 나옴.
        - 이 부분은 버그 픽스를 통한 해결 요망

### packagelist.txt
- 아나콘다의 conda install을 위한 패키지 정보들

### requirements.txt
- pip install을 이용한 패키지 정보들
- 현재 우리 프로젝트는 아나콘다를 사용하므로 이 파일은 사용하지 말 것

### 데이터 파일 (.csv)
#### train.csv
- Tensorflow를 이용해 학습시킬 데이터가 담긴 csv 파일
- 이 파일에 영어-PlantUML 데이터를 추가해야 함
- 오픈소스의 의의가 됨

#### test.csv
- 학습되지 않은 영어-PlantUML 데이터
- 정확도 측정을 위해 사용
