import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont
import time
from botocore.config import Config

my_config = Config(region_name = 'us-east-2')

def start_model(project_arn, model_arn, version_name, min_inference_units):

    client=boto3.client('rekognition',config=my_config)

    try:
        # Start the model
        print('Starting model: ' + model_arn)
        response=client.start_project_version(ProjectVersionArn=model_arn, MinInferenceUnits=min_inference_units)
        # Wait for the model to be in the running state
        project_version_running_waiter = client.get_waiter('project_version_running')
        project_version_running_waiter.wait(ProjectArn=project_arn, VersionNames=[version_name])

        #Get the running status
        describe_response=client.describe_project_versions(ProjectArn=project_arn,
            VersionNames=[version_name])
        for model in describe_response['ProjectVersionDescriptions']:
            print("Status: " + model['Status'])
            print("Message: " + model['StatusMessage']) 
    except Exception as e:
        print(e)
        
    print('Done...')

def upload_fileTto_s3():
    s3 = boto3.client("s3",config=my_config)

    s3.upload_file(
    Filename="C:\\#Dev\\ImagineCup\\ImagesML\\test.jpg",
    Bucket="ms-val-data",
    Key="test.jpg",
)

def display_image(bucket,photo,response):
    # Load image from S3 bucket
    s3_connection = boto3.resource('s3')

    s3_object = s3_connection.Object(bucket,photo)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image=Image.open(stream)

    # Ready image to draw bounding boxes on it.
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    identified_label="nil"
    maxim=0
    # calculate and display bounding boxes for each detected custom label
    print('Detected custom labels for ' + photo)
    for customLabel in response['CustomLabels']:
        print('Label ' + str(customLabel['Name']))
        print('Confidence ' + str(customLabel['Confidence']))
        if(float(customLabel['Confidence'])>maxim):
            maxim=float(customLabel['Confidence'])
            identified_label=str(customLabel['Name'])

    return identified_label

    #identified_label is the final label
        
def show_custom_labels(model,bucket,photo, min_confidence):
    client=boto3.client('rekognition')

    #Call DetectCustomLabels
    response = client.detect_custom_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        MinConfidence=min_confidence,
        ProjectVersionArn=model)

    # For object detection use case, uncomment below code to display image.
    identified_label=display_image(bucket,photo,response)

    return identified_label      

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

def img_classification_call():

    #start model
    project_arn='arn:aws:rekognition:ap-south-1:829135113306:project/msimgcup/1671700155017'
    model_arn='arn:aws:rekognition:ap-south-1:829135113306:project/msimgcup/version/msimgcup.2022-12-22T14.43.20/1671700399935'
    min_inference_units=1 
    version_name='msimgcup.2022-12-22T14.43.20'
    start_model(project_arn, model_arn, version_name, min_inference_units)

    #upload file to s3
    upload_fileTto_s3()

    #recognize category of object
    bucket='ms-val-data'
    photo='test.jpg' #s3 image file name
    model='arn:aws:rekognition:ap-south-1:829135113306:project/msimgcup/version/msimgcup.2022-12-22T14.43.20/1671700399935'
    min_confidence=30
    identified_label=show_custom_labels(model,bucket,photo, min_confidence)
    print("identified_label is: " + str(identified_label))

    #stop
    model_arn='arn:aws:rekognition:ap-south-1:829135113306:project/msimgcup/version/msimgcup.2022-12-22T14.43.20/1671700399935'
    stop_model(model_arn)

if __name__ == "__main__":
    img_classification_call()