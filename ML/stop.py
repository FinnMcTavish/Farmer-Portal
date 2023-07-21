import boto3
import time


def stop_model(model_arn):

    client=boto3.client('rekognition')

    print('Stopping model:' + model_arn)

    #Stop the model
    try:
        response=client.stop_project_version(ProjectVersionArn=model_arn)
        status=response['Status']
        print ('Status: ' + status)
    except Exception as e:  
        print(e)  

    print('Done...')
    
def main():
    
    model_arn='arn:aws:rekognition:ap-south-1:829135113306:project/msimgcup/version/msimgcup.2022-12-22T14.43.20/1671700399935'
    stop_model(model_arn)

if __name__ == "__main__":
    main() 