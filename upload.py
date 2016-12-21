#!/usr/bin/env python

import boto3
import io
import json
import sys
import zipfile

def create_zip(filename):
    file_like_object = io.BytesIO()
    zipf = zipfile.ZipFile(file_like_object, 'w', zipfile.ZIP_DEFLATED)
    zipf.write(filename)
    zipf.close()
    return file_like_object.getvalue()

default_config = {
    "profile": "default",
    "regions": ["us-east-1"],
    "lambdas": [
        {
            "name":"lambda_function",
            "runtime":"python2.7",
            "role":"",
            "handler":"lambda_handler",
            "file":"lambda_handler.py",
            "description":"This is my lambda function!",
            "timeout":3,
            "memory":128
            }
        ]
    }

config_file = sys.argv[1] if len(sys.argv) > 1 else "lambda-upload.json"

with open(config_file,"r") as f:
    config = json.load(f)
lambdas = config["lambdas"]
regions = config.get("regions", ["us-east-1"])
profile = config.get("profile", "default")

failed = []

for region in regions:
    session = boto3.session.Session(region_name=region, profile_name=profile)
    lmbd = session.client("lambda")
    for function in lambdas:
        try:
            zipfile = create_zip(function["file"])
            try:
                f = lmbd.get_function(FunctionName=function["name"])
                lmbd.update_function_code(
                    FunctionName=function["name"],
                    ZipFile=zipfile,
                    Publish=True
                    )
            except Exception as e:
                print(e)
                lmbd.create_function(
                    FunctionName=function["name"],
                    Runtime=function["runtime"],
                    Role=function["role"],
                    Handler=function["handler"],
                    Code={"ZipFile":zipfile},
                    Description=function.get("description", ""),
                    Timeout=function.get("timeout",3),
                    MemorySize=function.get("memory",128)
                    )
        except Exception as e:
            print(e)
            failed.add(region + "/" + function.get("name","<no name specified>"))

if failed:
    print("The following region/function pairs failed:")
    print(", ".join(failed))
