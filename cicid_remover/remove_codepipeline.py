import boto3

def delete_gcu_codepipelines():
    # Boto3 세션 생성
    session = boto3.Session()
    
    # CodePipeline 클라이언트 생성
    codepipeline = session.client('codepipeline')
    
    # 파이프라인 목록 가져오기
    response = codepipeline.list_pipelines()
    
    # 이름에 "gcu"가 포함된 파이프라인 찾기 및 삭제
    for pipeline in response.get('pipelines', []):
        if 'gcu' in pipeline['name'].lower():  # 소문자로 변환하여 비교
            print(f"Deleting Pipeline: {pipeline['name']}")
            codepipeline.delete_pipeline(name=pipeline['name'])

if __name__ == '__main__':
    delete_gcu_codepipelines()
