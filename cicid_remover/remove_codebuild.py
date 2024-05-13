import boto3

keyword = "cicd"

def list_target_codebuild_projects():
    session = boto3.Session()
    codebuild = session.client('codebuild')
    response = codebuild.list_projects()
    
    # 키워드를 포함하는 프로젝트만 필터링
    target_projects = [project for project in response.get('projects', [])
                       if keyword in project.lower()]
    return target_projects

def delete_codebuild_projects(projects):
    session = boto3.Session()
    codebuild = session.client('codebuild')
    
    for project in projects:
        print(f"Deleting CodeBuild Project: {project}")
        codebuild.delete_project(name=project)

def main():
    target_projects = list_target_codebuild_projects()
    
    if target_projects:
        print("다음 프로젝트들이 삭제될 것입니다:")
        for project in target_projects:
            print(project)
        
        confirm = input("위 프로젝트들을 삭제하시겠습니까? (y/n): ")
        if confirm.lower() == 'y':
            delete_codebuild_projects(target_projects)
            print("프로젝트 삭제가 완료되었습니다.")
        else:
            print("삭제가 취소되었습니다.")
    else:
        print("삭제할 프로젝트를 찾지 못했습니다.")

if __name__ == '__main__':
    main()
