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


import boto3
import json
import uuid  
from datetime import datetime
import time
import os


def lambda_handler(event, context):
    # Create a DataZone client

    datazone = boto3.client('datazone')
    accountid = context.invoked_function_arn.split(":")[4]
    region = os.environ['AWS_REGION']
    glue = boto3.client('glue')

    # Generate a new UUID for the run
    run_id = str(uuid.uuid4())

    # Your DataZone domain and project identifiers
    
    list_domains_response = datazone.list_domains()
    for domain in list_domains_response["items"]:
        if domain["name"] == "CorporateDomain":
            domain_id =domain["id"]
    list_projects_response = datazone.list_projects(
        domainIdentifier=domain_id
    )
    for project in list_projects_response["items"]:
        if project["name"] == "Personal Banking Data Products":
            project_id =project["id"]

    # get job runs
    get_job_runs_response = glue.get_job_runs(
        JobName="Curate_Customers"
    )
    for run in get_job_runs_response["JobRuns"]:
        # OpenLineage metadata with column names in lowercase
        
        CompletedOn = run["CompletedOn"]
        lineage_data = {
            "eventType": "COMPLETE",
            "eventTime":  CompletedOn.strftime("%Y-%m-%dT%H:%M:%Sz"),
            "run": {
                "runId": run_id,  # Generate a new UUID for each run
                "facets":{
                    "environment-properties":{
                        "_producer":"https://github.com/OpenLineage/OpenLineage/tree/1.9.1/integration/spark",
                        "_schemaURL":"https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunFacet",
                        "environment-properties":{
                            "GLUE_VERSION":"3.0",
                            "GLUE_COMMAND_CRITERIA":"glueetl",
                            "GLUE_PYTHON_VERSION":"3"
                        }
                    }
                }
            },
            "job": {
                "namespace": f"{domain_id}.{project_id}",
                "name": "Curate_Customers",
                "facets":{
                    "jobType":{
                        "_producer":"https://github.com/OpenLineage/OpenLineage/tree/1.9.1/integration/glue",
                        "_schemaURL":"https://openlineage.io/spec/facets/2-0-2/JobTypeJobFacet.json#/$defs/JobTypeJobFacet",
                        "processingType":"BATCH",
                        "integration":"glue",
                        "jobType":"JOB"
                    }
                }
            },
            "outputs": [
                {
                    "namespace": f"{domain_id}.{project_id}",
                    "name": f"s3://{accountid}-{region}-datagov-personalbanking-curated/customers/",
                    "facets":{
                        "symlinks":{
                            "_producer":"https://github.com/OpenLineage/OpenLineage/tree/1.9.1/integration/spark",
                            "_schemaURL":"https://openlineage.io/spec/facets/1-0-0/SymlinksDatasetFacet.json#/$defs/SymlinksDatasetFacet",
                            "identifiers":[
                                {
                                    "namespace":f"s3://{accountid}-{region}-datagov-personalbanking-curated/customers/",
                                    "name":"personalbanking_curated.customers",
                                    "type":"TABLE"
                                }
                            ]
                        }
                    }      
                }
            ],
            "producer": "https://github.com/OpenLineage/OpenLineage/tree/1.9.1/integration/glue",
            "schemaURL": "https://openlineage.io/spec/1-0-2/OpenLineage.json#/definitions/RunEvent"
        }
        # Post the lineage event

        print(f"lineage data: {lineage_data}")
        try:
            # Post the lineage event
            post_response = datazone.post_lineage_event(
                domainIdentifier=domain_id,
                clientToken=run_id,
                event=json.dumps(lineage_data, default=str)
            )
            print(f"Lineage event posted successfully: {post_response}")
        
        except Exception as e:
            print(f"Error: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error: {str(e)}')
            }
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Lineage event posted successfully'
        })
    }