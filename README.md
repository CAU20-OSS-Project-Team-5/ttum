# django 를 이용한 program backend
## django 설치 후 가상환경 위에 django, python 설치
- cmd 해당 폴더로 이동 후 myvenv\Scripts\activate 명령어로 가상환경 실행
- cd mysite -> py manage.py runserver 127.0.0.1:8080 으로 로컬 서버 사용
- 현재 127.0.0.1:8080/imports가 초기 화면이며 이후 수정 계획
- 현재 프론트앤드 작업은 되지 않았으며, 단순히 텍스트를 입력하고 Convert 버튼을 누르면 입력한 text가 서버에 .txt파일 형태로 저장됨. 전달된 txt는 Catch에서 GET하여 
- NL -> PlantUML -> ImgFile 로의 변환을 거치고 입력한 txt(nl)와 이미지를 출력하면 됨 
- 현재 Catch함수에서 변환 과정을 생략하고 임의의 이미지 파일을 가져와 출력하는데 Pillow 패키지를 사용함.
- 이건 바꾸다보면 바뀔수도
- 현재 Catch함수에서 임의의 이미지파일의 url을 저장하여 전달함
- 결과물을 보여주는 화면에서 이미지파일의 url을 이용하여 img 출력
