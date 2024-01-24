클론 이후
students.csv에 학생 데이터 입력
이후 아래 명령어 순차적 실행

`npm install -g aws-cdk --force`

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip install aws-cdk-lib constructs`

`cdk deploy --app "python iam-creater.py" -y`

삭제 시 실행 명령어
`cdk destroy --all`
