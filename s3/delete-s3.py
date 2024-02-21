import boto3
# 대학코드를 입력하세요
univ="ljhu"

# 버킷 이름에 대학코드로 시작하는 모든 버킷을 찾습니다.
def find_test_buckets():
    s3 = boto3.resource("s3")
    test_buckets = []
    for bucket in s3.buckets.all():
        if bucket.name.startswith(univ):
            test_buckets.append(bucket)
    return test_buckets

# 모든 객체를 삭제하고 버킷을 삭제합니다.
def delete_buckets(buckets):
    for bucket in buckets:
        # 객체 삭제
        bucket.object_versions.delete()
        # 버킷 삭제
        bucket.delete()

# 메인 함수: 대학코드로 시작하는 모든 버킷을 찾아서 삭제합니다.
def main():
    test_buckets = find_test_buckets()
    if test_buckets:
        print("다음 버킷이 삭제될 것입니다:")
        for bucket in test_buckets:
            print(bucket.name)
        confirm = input("위 버킷들을 삭제하시겠습니까? (y/n): ")
        if confirm.lower() == "y":
            delete_buckets(test_buckets)
            print("버킷 삭제가 완료되었습니다.")
        else:
            print("삭제가 취소되었습니다.")
    else:
        print("삭제할 버킷을 찾지 못했습니다.")

if __name__ == "__main__":
    main()

# python3 delete-s3.py