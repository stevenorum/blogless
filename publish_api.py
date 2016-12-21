#!/usr/bin/env python

import boto3
import json

region = "us-east-1"
profile="default"
session = boto3.session.Session(region_name=region, profile_name=profile)

cf = session.client("cloudformation")

template_file = "api.json"

stack_name = "API"
template_body = open(template_file,"r").read()

cf.validate_template(TemplateBody=template_body)
response = cf.create_stack(StackName=stack_name, TemplateBody=template_body)
