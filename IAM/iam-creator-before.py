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
            'univ': row['univ'],
            'email': row['email'],
            'number': row['number'],
        })

SchoolCode = "TEST"
SchoolFullName = "권한경계테스트"

class IamStack(Stack):
    def __init__(self, scope: App, id: str, school_code: str, student_list: list, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
    
        group = iam.Group(self, "Group", group_name=f"{school_code}")
        
        managed_policy_arns = [
            "arn:aws:iam::730335373015:policy/AllowNonOverkill",
            "arn:aws:iam::730335373015:policy/IAMBasicAccess",
            "arn:aws:iam::730335373015:policy/SafePowerUser",
            "arn:aws:iam::730335373015:policy/DenyDestruct",
            "arn:aws:iam::730335373015:policy/RestrictRegionSeoul",
            "arn:aws:iam::730335373015:policy/ForcePermissionBoundaryRoleSeoul",
        ]
        
        managed_policies = [iam.ManagedPolicy.from_managed_policy_arn(self, f"ManagedPolicy{i}", managed_policy_arn=arn) for i, arn in enumerate(managed_policy_arns, start=1)]
        
        for policy in managed_policies:
            group.add_managed_policy(policy)
        
        create_date = datetime.now().strftime("%Y-%m-%d")
        
        iam_users = []
        for index, student in enumerate(student_list, start=1):
            user_name = f"{school_code}-{index:03}"
            password = f"12345678aA"
            
            # null이 아닌 태그 목록 생성
            tags = [
                {"key": "Name", "value": student['name'] or "N/A"},
                {"key": "University", "value": student['univ'] or "N/A"},
                # {"key": "University", "value": studentSchoolFullName or "N/A"},
                # {"key": "Subject", "value": student['subject'] or "N/A"},
                {"key": "Email", "value": student['email'] or "N/A"},
                {"key": "Number", "value": student['number'] or "N/A"},
                {"key": "CreateDate", "value": create_date or "N/A"}
            ]
            
            # null 값을 가진 태그 필터링
            valid_tags = [tag for tag in tags if tag["value"] is not None]
            
            user = iam.CfnUser(self, f"CfnUser{index}",
                user_name=user_name,
                login_profile=iam.CfnUser.LoginProfileProperty(
                    password=password,
                    password_reset_required=True
                ),
                tags=valid_tags
            )
            
            group.add_user(iam.User.from_user_name(self, f"ImportedUser{index}", user_name))
            
            iam_users.append({
                'Name': student['name'] or "N/A",
                'Email': student['email'] or "N/A",
                'IAM UserName': user_name,
                'Password': password
            })
        
        with open('result.md', 'a') as md_file:
            md_file.write("# IAM 사용자 정보\n")
            md_file.write("# 로그인 콘솔주소: https://nxtcloud.signin.aws.amazon.com/console\n")
            
            md_file.write("| Name | IAM User Name |\n")
            md_file.write("|------|---------------|\n")
            for user_info in iam_users:
                md_file.write(f"| {user_info['Name']} | {user_info['IAM UserName']} |\n")
app = App()
IamStack(app, f"{SchoolCode}-IamStack", school_code=SchoolCode, student_list=student_list)
app.synth()
