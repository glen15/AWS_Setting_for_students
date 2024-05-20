import boto3

# 대학코드를 입력하세요
univ = "wsu"

# Cloud9 환경 이름에 대학코드로 시작하는 모든 환경을 찾습니다.
def find_cloud9_environments():
    cloud9 = boto3.client("cloud9")
    environments = cloud9.describe_environments()["environments"]
    test_environments = []
    for env in environments:
        if env["name"].startswith(univ):
            test_environments.append(env)
    return test_environments

# 모든 환경을 삭제합니다.
def delete_environments(environments):
    cloud9 = boto3.client("cloud9")
    for env in environments:
        cloud9.delete_environment(environmentId=env["id"])

# 메인 함수: 대학코드로 시작하는 모든 Cloud9 환경을 찾아서 삭제합니다.
def main():
    test_environments = find_cloud9_environments()
    if test_environments:
        print("다음 Cloud9 환경이 삭제될 것입니다:")
        for env in test_environments:
            print(env["name"])
        confirm = input("위 환경들을 삭제하시겠습니까? (y/n): ")
        if confirm.lower() == "y":
            delete_environments(test_environments)
            print("Cloud9 환경 삭제가 완료되었습니다.")
        else:
            print("삭제가 취소되었습니다.")
    else:
        print("삭제할 Cloud9 환경을 찾지 못했습니다.")

if __name__ == "__main__":
    main()
