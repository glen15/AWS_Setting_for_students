import boto3

keyword = "cicd"

def list_target_codedeploy_apps():
    session = boto3.Session()
    codedeploy = session.client('codedeploy')
    response = codedeploy.list_applications()
    
    # 키워드를 포함하는 애플리케이션만 필터링
    target_apps = [app for app in response.get('applications', [])
                   if keyword in app.lower()]
    return target_apps

def delete_codedeploy_apps(applications):
    session = boto3.Session()
    codedeploy = session.client('codedeploy')
    
    for app in applications:
        print(f"Deleting CodeDeploy Application: {app}")
        codedeploy.delete_application(applicationName=app)

def main():
    target_apps = list_target_codedeploy_apps()
    
    if target_apps:
        print("다음 애플리케이션들이 삭제될 것입니다:")
        for app in target_apps:
            print(app)
        
        confirm = input("위 애플리케이션들을 삭제하시겠습니까? (y/n): ")
        if confirm.lower() == 'y':
            delete_codedeploy_apps(target_apps)
            print("애플리케이션 삭제가 완료되었습니다.")
        else:
            print("삭제가 취소되었습니다.")
    else:
        print("삭제할 애플리케이션을 찾지 못했습니다.")

if __name__ == '__main__':
    main()
