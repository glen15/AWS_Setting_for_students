import boto3

def delete_gcu_codebuild_projects():
    # Boto3 세션 생성
    session = boto3.Session()
    
    # CodeBuild 클라이언트 생성
    codebuild = session.client('codebuild')
    
    # 프로젝트 목록 가져오기
    response = codebuild.list_projects()
    
    # 이름에 "gcu"가 포함된 프로젝트 찾기 및 삭제
    for project_name in response.get('projects', []):
        if 'gcu' in project_name.lower():  # 소문자로 변환하여 비교
            print(f"Deleting CodeBuild Project: {project_name}")
            codebuild.delete_project(name=project_name)

if __name__ == '__main__':
    delete_gcu_codebuild_projects()
