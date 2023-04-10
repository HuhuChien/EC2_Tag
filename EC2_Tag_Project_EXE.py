
import boto3
import os
from EC2_Tag_Project import resultList

os.environ['AWS_PROFILE'] = "for_EC2"

sns = boto3.client('sns',region_name='ap-northeast-1')
# Publish a simple message to the specified SNS topic

if len(resultList) == 0:
    message = '全部EC2主機已有Tag-Project'
   
else:
  
    message = ("\n\n".join(str(i) + '. ' + j for i, j in enumerate(resultList,1)))
    print(type(message))
    if ". a" in message:
        message = message.replace(". a",". ")
    if ". b" in message:
        message = message.replace(". b",". ")


    
print(message)
response = sns.publish(
    TopicArn='arn:aws:sns:ap-northeast-1:178322424346:AWS_EC2_TAG',   
    Message= message,  

)


