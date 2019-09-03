#!/usr/bin/env python3

import boto3
from datetime import datetime
import json
import os
from sneks.bash import *

region_name = os.environ["AWS_REGION"]
profile_name = os.environ["AWS_PROFILE"]
stack_name = os.environ["STACK_NAME"]

boto3.setup_default_session(region_name=region_name, profile_name=profile_name)

def tsstr(tstamp):
    dt = datetime.fromtimestamp(tstamp/1000)
    # return dt.strftime("%c")
    # return dt.strftime("%x %X")
    return dt.strftime("%y/%m/%d %H:%M:%S.%f")[:-3]

events_per_stream = 3

start_string = "START RequestId: "
end_string = "REPORT RequestId: "

cf = boto3.client("cloudformation")
logs = boto3.client("logs")
resources = cf.describe_stack_resources(StackName=stack_name)["StackResources"]
function_names = []
for resource in resources:
    if resource["ResourceType"] == "AWS::Lambda::Function":
        function_names.append(resource["PhysicalResourceId"])
for function_name in function_names:
    log_group = "/aws/lambda/{}".format(function_name)
    print("{}:".format(log_group))
    streams = logs.describe_log_streams(logGroupName=log_group, orderBy="LastEventTime", descending=True, limit=3)["logStreams"]
    for stream in reversed(streams):
        print_blue("{logStreamName} : {lastEventTimestamp}\n".format(logStreamName=stream["logStreamName"], lastEventTimestamp=tsstr(stream["lastEventTimestamp"])))
        events = logs.get_log_events(logGroupName=log_group, logStreamName=stream["logStreamName"])["events"]
        events.sort(key=lambda x: x["timestamp"])
        starts = [i for i in range(len(events)) if "START RequestId: " in events[i]["message"]]
        if len(starts) < events_per_stream:
            pass
        else:
            events = events[starts[-1*events_per_stream]:]
        for event in events:
            print("{timestamp} {message}".format(timestamp=blue_text(tsstr(event["timestamp"])), message=white_text(event["message"].rstrip())))
            if end_string in event["message"]:
                print("")
