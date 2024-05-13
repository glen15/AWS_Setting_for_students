import boto3

keyword = "cicd"

def list_target_pipelines():
    session = boto3.Session()
    codepipeline = session.client('codepipeline')
    response = codepipeline.list_pipelines()
    
    # 키워드를 포함하는 파이프라인만 필터링
    target_pipelines = [pipeline for pipeline in response.get('pipelines', [])
                        if keyword in pipeline['name'].lower()]
    return target_pipelines

def delete_pipelines(pipelines):
    session = boto3.Session()
    codepipeline = session.client('codepipeline')
    
    for pipeline in pipelines:
        print(f"Deleting Pipeline: {pipeline['name']}")
        codepipeline.delete_pipeline(name=pipeline['name'])

def main():
    target_pipelines = list_target_pipelines()
    
    if target_pipelines:
        print("다음 파이프라인들이 삭제될 것입니다:")
        for pipeline in target_pipelines:
            print(pipeline['name'])
        
        confirm = input("위 파이프라인들을 삭제하시겠습니까? (y/n): ")
        if confirm.lower() == 'y':
            delete_pipelines(target_pipelines)
            print("파이프라인 삭제가 완료되었습니다.")
        else:
            print("삭제가 취소되었습니다.")
    else:
        print("삭제할 파이프라인을 찾지 못했습니다.")

if __name__ == '__main__':
    main()
