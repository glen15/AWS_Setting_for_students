from aws_cdk import App, Stack
from aws_cdk import aws_iam as iam
from datetime import datetime
import csv

# CSV 파일에서 학생 목록 읽기
student_list = []
with open('students.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        student_list.append({
            'name': row['name'],
            'subject': row['subject'],
            'email': row['email']
        })

SchoolCode = "YOUR SCHOOL CODE"
SchoolFullName = "YOUR SCHOOL FULL NAME"

class IamStack(Stack):

    def __init__(self, scope: App, id: str, school_code: str, student_list: list, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # IAM 그룹 생성
        group = iam.Group(self, "Group", group_name=f"{school_code}")
                # 정책 생성
        managed_policy_arns = [
            "arn:aws:iam::aws:policy/AmazonBedrockFullAccess",
            "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
            "arn:aws:iam::aws:policy/AmazonEC2FullAccess",
            "arn:aws:iam::aws:policy/AmazonRDSFullAccess",
            "arn:aws:iam::aws:policy/AmazonS3FullAccess",
            "arn:aws:iam::aws:policy/AWSCloud9Administrator",
            "arn:aws:iam::aws:policy/AWSLambda_FullAccess",
            "arn:aws:iam::aws:policy/AWSMarketplaceFullAccess",
            "arn:aws:iam::aws:policy/CloudWatchFullAccess",
            "arn:aws:iam::aws:policy/IAMFullAccess"
        ]
        
        managed_policies = [iam.ManagedPolicy.from_managed_policy_arn(self, f"ManagedPolicy{i}", managed_policy_arn=arn) for i, arn in enumerate(managed_policy_arns, start=1)]

        # 그룹에 정책 연결
        for policy in managed_policies:
            group.add_managed_policy(policy)


        # 현재 날짜 설정
        create_date = datetime.now().strftime("%Y-%m-%d")

        # 학생별로 IAM 사용자 생성 및 그룹에 추가
        iam_users = []  # IAM 사용자 정보를 저장할 리스트

        for index, student in enumerate(student_list, start=1):
            # 이름의 첫 글자를 대문자 이니셜로 추출
            initials = ''.join([word[0].upper() for word in student['name'].split()])
            user_name = f"{school_code}-{initials}-{index:03}"
            password = user_name

            user = iam.CfnUser(self, f"CfnUser{index}",
                user_name=user_name,
                login_profile=iam.CfnUser.LoginProfileProperty(
                    password=password,
                    password_reset_required=False
                ),
                managed_policy_arns=["arn:aws:iam::aws:policy/AmazonBedrockFullAccess", "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess", "arn:aws:iam::aws:policy/AmazonEC2FullAccess", "arn:aws:iam::aws:policy/AmazonRDSFullAccess", "arn:aws:iam::aws:policy/AmazonS3FullAccess", "arn:aws:iam::aws:policy/AWSCloud9Administrator", "arn:aws:iam::aws:policy/AWSLambda_FullAccess", "arn:aws:iam::aws:policy/AWSMarketplaceFullAccess", "arn:aws:iam::aws:policy/CloudWatchFullAccess", "arn:aws:iam::aws:policy/IAMFullAccess"],
                tags=[
                    {"key": "Name", "value": student['name']},
                    {"key": "University", "value": SchoolFullName},
                    {"key": "Subject", "value": student['subject']},
                    {"key": "Email", "value": student['email']},
                    {"key": "CreateDate", "value": create_date}
                ]
            )

            group.add_user(iam.User.from_user_name(self, f"ImportedUser{index}", user_name))

            # IAM 사용자 정보를 저장
            iam_users.append({
                'Name': student['name'],
                'Email': student['email'],
                'IAM UserName': user_name,
                'Password': password
            })

        # IAM 사용자 정보를 Markdown 파일로 저장
        with open('result.md', 'w') as md_file:
            md_file.write("# IAM 사용자 정보\n")
            md_file.write("# 로그인 콘솔주소: https://smu-inha-cloud.signin.aws.amazon.com/console\n")
            
            md_file.write("| Name | Email | IAM User Name | Password |\n")
            md_file.write("|------|-------|---------------|----------|\n")
            for user_info in iam_users:
                md_file.write(f"| {user_info['Name']} | {user_info['Email']} | {user_info['IAM UserName']} | {user_info['Password']} |\n")

app = App()
IamStack(app, f"{SchoolCode}-IamStack", school_code=SchoolCode, student_list=student_list)
app.synth()