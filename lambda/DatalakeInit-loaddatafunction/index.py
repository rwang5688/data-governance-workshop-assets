#MIT No Attribution

#Copyright 2023 Amazon.com, Inc. or its affiliates.

#Permission is hereby granted, free of charge, to any person obtaining a copy of this
#software and associated documentation files (the "Software"), to deal in the Software
#without restriction, including without limitation the rights to use, copy, modify,
#merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#permit persons to whom the Software is furnished to do so.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import boto3
import cfnresponse
s_3 = boto3.client('s3')
stepfn = boto3.client('stepfunctions')

def lambda_handler(event, context):
    requestType = event['RequestType']
    print('The event request is: ', str(event))
    response_data = {}
    data_source_bucket = event['ResourceProperties']['data_source_bucket']
    data_source_prefix = event['ResourceProperties']['data_source_prefix']
    target_bucket_personal_raw = event['ResourceProperties']['target_bucket_personal_raw']
    target_bucket_wealth_raw = event['ResourceProperties']['target_bucket_wealth_raw']
    target_bucket_insurance_raw = event['ResourceProperties']['target_bucket_insurance_raw']
    target_bucket_personal_curated = event['ResourceProperties']['target_bucket_personal_curated']
    target_bucket_wealth_curated = event['ResourceProperties']['target_bucket_wealth_curated']
    target_bucket_insurance_curated = event['ResourceProperties']['target_bucket_insurance_curated']
    version = event['ResourceProperties']['version']
    accountID = event['ResourceProperties']['accountId']
    region = event['ResourceProperties']['region']
    try:
        if requestType in ('Create', 'Update'):
            print('Creating or updating S3 content...')
            for objname in ['appointments','claims','insurance_plans','policies','policy_holders','providers']:
                copy_source = {'Bucket': data_source_bucket,'Key':  data_source_prefix +'/' +version +'/data/insurance/'+objname+'.csv'}
                dest_object_key=objname+'/'+objname+'.csv'
                s_3.copy_object( CopySource=copy_source, Bucket=target_bucket_insurance_raw, Key=dest_object_key )
            for objname in ['accounts','credit_cards','customers','investments','loans','transactions']:
                copy_source = {'Bucket': data_source_bucket,'Key':  data_source_prefix +'/' +version +'/data/personal/'+objname+'.csv'}
                dest_object_key=objname+'/'+objname+'.csv'
                s_3.copy_object( CopySource=copy_source, Bucket=target_bucket_personal_raw, Key=dest_object_key ) 
            for objname in ['accounts','advisors','clients','investments','loans','transactions']:
                copy_source = {'Bucket': data_source_bucket,'Key':  data_source_prefix +'/' +version +'/data/wealth/'+objname+'.csv'}
                dest_object_key=objname+'/'+objname+'.csv'
                s_3.copy_object( CopySource=copy_source, Bucket=target_bucket_wealth_raw, Key=dest_object_key )
        elif requestType == 'Delete':
            print('Deleting S3 content...')
            b_operator = boto3.resource('s3')
            b_operator.Bucket(str(target_bucket_personal_raw)).objects.all().delete()
            b_operator.Bucket(str(target_bucket_wealth_raw)).objects.all().delete()
            b_operator.Bucket(str(target_bucket_insurance_raw)).objects.all().delete()
            b_operator.Bucket(str(target_bucket_personal_curated)).objects.all().delete()
            b_operator.Bucket(str(target_bucket_wealth_curated)).objects.all().delete()
            b_operator.Bucket(str(target_bucket_insurance_curated)).objects.all().delete()
    # Everything OK... send the signal back
        print('Execution succesful!')
        stepfn.start_execution(stateMachineArn=f'arn:aws:states:{region}:{accountID}:stateMachine:Init', input='{}')
        cfnresponse.send(event,
                        context,
                        cfnresponse.SUCCESS,
                        response_data)
    except Exception as e:
        print('Execution failed...')
        print(str(e))
        response_data['Data'] = str(e)
        cfnresponse.send(event,
                        context,
                        cfnresponse.FAILED,
                        response_data)    
