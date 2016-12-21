#!/usr/bin/env python

import boto3
import json

def pprint(blob):
    print((json.dumps(blob, indent=2, sort_keys=True)))

region = "us-east-1"
profile="default"
session = boto3.session.Session(region_name=region, profile_name=profile)
apig = session.client("apigateway")
restApiId="cnpbv8djvg"
apis = apig.get_rest_api(restApiId=restApiId)
resources = apig.get_resources(restApiId=restApiId)["items"]
stages = apig.get_stages(restApiId=restApiId)
del stages["ResponseMetadata"]
pprint(stages)

exit(1)
for resource in resources:
    for resourceMethod in resource["resourceMethods"]:
        method = apig.get_method(restApiId=restApiId,
        resourceId=resource["id"],
        httpMethod=resourceMethod)
        del method["ResponseMetadata"]
        pprint(method)
#print(apis)
#print(resources)
