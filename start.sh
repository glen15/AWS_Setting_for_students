npm install -g aws-cdk --force
python3 -m venv .venv
source .venv/bin/activate
pip install aws-cdk-lib constructs
cdk deploy --app "python iam-creater.py"