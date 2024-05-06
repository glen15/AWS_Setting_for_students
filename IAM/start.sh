npm install -g aws-cdk --force
python3 -m venv .venv
source .venv/bin/activate
pip install aws-cdk-lib constructs
cdk bootstrap 
cdk deploy --app "python iam-creator.py"
# cdk destroy --app "python iam-creater.py"
