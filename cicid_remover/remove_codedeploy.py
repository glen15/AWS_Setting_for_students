import boto3

def delete_gcu_codedeploy_apps():
    # Boto3 세션 생성
    session = boto3.Session()
    
    # CodeDeploy 클라이언트 생성
    codedeploy = session.client('codedeploy')
    
    # 애플리케이션 목록 가져오기
    response = codedeploy.list_applications()
    
    # 이름에 "gcu"가 포함된 애플리케이션 찾기 및 삭제
    for app_name in response.get('applications', []):
        if 'gcu' in app_name.lower():  # 소문자로 변환하여 비교
            print(f"Deleting CodeDeploy Application: {app_name}")
            codedeploy.delete_application(applicationName=app_name)

if __name__ == '__main__':
    delete_gcu_codedeploy_apps()
