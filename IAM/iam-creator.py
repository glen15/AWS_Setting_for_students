from aws_cdk import App, Stack
from aws_cdk import aws_iam as iam
from aws_cdk import CfnOutput
from constructs import Construct
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
    def __init__(self, scope: Construct, id: str, school_code: str, student_list: list, **kwargs) -> None:
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
        
        # 권한 경계 정책 ARN
        permission_boundary_arn = "arn:aws:iam::730335373015:policy/PermissionBoundarySeoul"
        
        create_date = datetime.now().strftime("%Y-%m-%d")
        
        iam_users = []
        cfn_users = []  # CfnUser 객체를 저장할 리스트
        for index, student in enumerate(student_list, start=1):
            user_name = f"{school_code}-{index:03}"
            password = f"12345678aA"
            
            # null이 아닌 태그 목록 생성
            tags = [
                {"key": "Name", "value": student['name'] or "N/A"},
                {"key": "University", "value": student['univ'] or "N/A"},
                {"key": "Email", "value": student['email'] or "N/A"},
                {"key": "Number", "value": student['number'] or "N/A"},
                {"key": "CreateDate", "value": create_date or "N/A"}
            ]
            
            # null 값을 가진 태그 필터링
            valid_tags = [tag for tag in tags if tag["value"] is not None]
            
            cfn_user = iam.CfnUser(self, f"CfnUser{index}",
                user_name=user_name,
                login_profile=iam.CfnUser.LoginProfileProperty(
                    password=password,
                    password_reset_required=True
                ),
                managed_policy_arns=[policy.managed_policy_arn for policy in managed_policies],
                permissions_boundary=permission_boundary_arn,
                tags=valid_tags
            )
            
            cfn_users.append(cfn_user)  # CfnUser 객체 저장
            
            iam_users.append({
                'Name': student['name'] or "N/A",
                'Email': student['email'] or "N/A",
                'IAM UserName': user_name,
                'Password': password
            })
        
        # 사용자들을 그룹에 추가
        for index, cfn_user in enumerate(cfn_users):
            iam.CfnUserToGroupAddition(self, f"UserToGroupAddition{index}",
                group_name=group.group_name,
                users=[cfn_user.ref]
            ).add_dependency(cfn_user)  # 사용자 생성 후 그룹에 추가되도록 의존성 추가
        
        # 결과를 CloudFormation 출력으로 추가
        for index, user_info in enumerate(iam_users):
            CfnOutput(self, f"UserInfo{index}", 
                      value=f"Name: {user_info['Name']}, IAM UserName: {user_info['IAM UserName']}",
                      description=f"User {index+1} Information")
        
        # 결과를 markdown 파일로 저장
        with open('result.md', 'w') as md_file:
            md_file.write("# IAM 사용자 정보\n")
            md_file.write("# 로그인 콘솔주소: https://nxtcloud.signin.aws.amazon.com/console\n")
            
            md_file.write("| Name | IAM User Name |\n")
            md_file.write("|------|---------------|\n")
            for user_info in iam_users:
                md_file.write(f"| {user_info['Name']} | {user_info['IAM UserName']} |\n")

app = App()
IamStack(app, f"{SchoolCode}-IamStack", school_code=SchoolCode, student_list=student_list)
app.synth()
