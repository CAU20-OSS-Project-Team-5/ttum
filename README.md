# Deact
Frontend로 React, Backend로 Django를 사용한 로컬 서버.

## 현재 구현 기능
React 프론트앤드서버가 localhost:3000, Django 백앤드서버가 127.0.0.1:8020 에서 열림
React page에서 Textarea에 Text를 입력하고 Convert 버튼을 누르면 백앤드 서버의 sqlite3 db에 저장이 됨.
그 후 저장된 데이터를 React page 에서 다시 받아와 page에 나타냄.

Django의 view.py 의 taskCreate(request)에서 입력된 문장을 이미지파일의 url 주소로 변환하여 주면 됨.

