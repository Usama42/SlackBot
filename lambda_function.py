import json
import boto3
import logging
from botocore.vendored import requests
import os
import urllib3
import base64
from urllib.parse import parse_qsl, urlparse
from urllib.parse import parse_qs
import urllib.parse
from functools import lru_cache
from urllib3.util import parse_url
from itertools import chain 
from urllib3.exceptions import (
    DecodeError, ReadTimeoutError, ProtocolError, LocationParseError)
    

    

# Your app's Slack bot user token
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]


# Slack client for Web API requests
def get_list(command_text):
    command_array = (command_text.split(",")) 
    print(command_array)
    if(len(command_array)) > 1:
        region = command_array[1]
    else:
        region = 'us-east-1'
   
    RunInstances = []    
    
    ec2 = boto3.resource('ec2', region)
    url = "web-hook-url"
    
    filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]

    instances = ec2.instances.filter(Filters = filters)

    RunningInstances = []

    for instance in instances:
        RunningInstances.append(instance.id)
        print(RunningInstances)
    
    #RunInstances.append(RunningInstances)
    #print(RunInstances)
    print(RunningInstances)
    return RunningInstances
    #instanceList = json.dumps(RunningInstances)
client = boto3.client('ec2')
def add_rule(client, command_text):
    #command_array = (command_text.split(",")) 
    #print(command_array)
    #if(len(command_array)) > 1:
        #region = command_array[1]
    #else:
        #region = 'us-east-1'
    #print(region)
    #get_running(command_text)
    http = urllib3.PoolManager()
    url = "web-hook-url"
    #response = http.request("POST", url, body=json.dumps(payload), headers={'Content-Type': 'application/json'})
    RunningInstances = get_list(command_text)
    Run = json.dumps(RunningInstances)
    payload = {
  "attachments": [
    {
      "fallback": "Message",
      "text": ("Which instance ID you want to select in a Format : ID Index"),
      "fields": [
        {
          "title": "Enter values starting from 0",
          "value": (Run),
        }
      ],
      "color": "red"
    }
  ],
  "icon_emoji": "gun"
}
    response = http.request("POST", url, body=json.dumps(payload), headers={'Content-Type': 'application/json'})
    #RunningInstances = get_list(command_text)
    #print(RunningInstances)

def add_egress(command_text, group_ID):
    command_array = (command_text.split(",")) 
    print(command_array)
    region_name = command_array[1]
    client = boto3.client('ec2', region_name=region_name)
    IpProtocol = (command_array[2])
    FromPort = int(command_array[3])
    ToPort = int(command_array[4])
    CidrIp = (command_array[5])
    Description = command_array[6]
    permissions = [
        {
            'IpProtocol': IpProtocol,
            'FromPort': FromPort,
            'ToPort': ToPort,
            'IpRanges': [
                {
                    'CidrIp': CidrIp,
                    'Description' : Description
                }
            ] ,
         }
    ]
    #sg_id = 'sg-07b7d727c5733ac04'
    
    client.authorize_security_group_egress(GroupId=group_ID, IpPermissions=permissions)
  
    response_msg = "Egress Rules has been added successfully!!!"
    return response_msg
    
    
def add_ingress(command_text, group_ID):
    command_array = (command_text.split(",")) 
    region_name = command_array[1]
    client = boto3.client('ec2', region_name=region_name)
    IpProtocol = (command_array[2])
    FromPort = int(command_array[3])
    ToPort = int(command_array[4])
    CidrIp = (command_array[5])
    Description = command_array[6]
    permissions = [
        {
            'IpProtocol': IpProtocol,
            'FromPort': FromPort,
            'ToPort': ToPort,
            'IpRanges': [
                {
                    'CidrIp': CidrIp,
                    'Description' : Description
                   
                }
            ] ,
         }
    ]
    #sg_id = 'sg-07b7d727c5733ac04'
    
    client.authorize_security_group_ingress(GroupId=group_ID, IpPermissions=permissions)
    response_msg = "Ingress Rules has been added successfully!!!"
    return response_msg


region = 'us-east-1'    
def get_running(command_text):
    command_array = (command_text.split(",")) 
    print(command_array)
    if(len(command_array)) > 1:
        region = command_array[1]
    else:
        region = 'us-east-1'
    print(region)
    RunInstances = []    
    
    ec2 = boto3.resource('ec2', region)
    url = "web-hook-url"
    
    filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]

    instances = ec2.instances.filter(Filters = filters)

    RunningInstances = []

    for instance in instances:
        RunningInstances.append(instance.id)
        print(RunningInstances)
    
    #RunInstances.append(RunningInstances)
    #print(RunInstances)
    print(RunningInstances)
    instanceList = json.dumps(RunningInstances)
    if len(RunningInstances) != 0:
        instanceList = json.dumps(RunningInstances)
        print(instanceList)
        print("Found instances ")
    else:
        print("none found")
        instanceList = "No running Instances found"
       
    print(instanceList) 
    http = urllib3.PoolManager()
   
    reg = json.dumps(region)  
    #msg = json.dumps(instanceList).encode('utf-8')
    url = "web-hook-url"
    payload = {
  "attachments": [
    {
      "fallback": "Message",
      "text": (reg),
      "fields": [
        {
          "title": "Running ec2 Instances in region",
          "value": (instanceList),
        }
      ],
      "color": "red"
    }
  ],
  "icon_emoji": "gun"
}
    response = http.request("POST", url, body=json.dumps(payload), headers={'Content-Type': 'application/json'})
#from urlparse import parse_qs
from boto3 import resource
def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
ec2 = boto3.resource('ec2')
#region = 'us-east-1'

#region = os.getenv('REGION_NAME')

#print(region)
 
    
#expected_token = os.environ['EXPECTED_TOKEN']
def lambda_handler(event, context):
    
   
    params = parse_qs(event['body'])
    
    response_url = params['response_url'][0]
    trigger_id = params['trigger_id'][0]
    user = params['user_name'][0]
    command = params['command'][0]
    channel = params['channel_name'][0]
    command_text = params['text'][0]  # running us-east1
    #subcommand = params['text'][0].lower()
    #print(subcommand)
    print(command_text)
    print(trigger_id)
   
    if "running" in command_text:
        response_msg = get_running(command_text)
        
    elif  "Add SG Rule" in command_text:
        client = boto3.client('ec2')
        response_msg = add_rule(client, command_text)

    elif "Security Group Rules" in command_text:
        http = urllib3.PoolManager()
        url = "web-hook-url"
        payload = {
      "attachments": [
        {
          "fallback": "Message",
          "text": ("Security Group Rules"),
          "fields": [
            {
              "title": "You have to add Ingress Rules first!!",
              "value": ("Format: ID index , Region, IpProtocol, FromPort, ToPort, IpRanges, Description")
            }
          ],
          "color": "red"
        }
      ],
      "icon_emoji": "gun"
    }
        response = http.request("POST", url, body=json.dumps(payload), headers={'Content-Type': 'application/json'})
    #from urlparse import parse_qs
    elif "Adding Ingress" in command_text:
        command_array = (command_text.split(",")) 
        print(command_array)
        numb = command_array[0]
        region_name = command_array[1]
        RunningInstances = get_list(command_text)
        id = RunningInstances[int(numb)]
        print(id)
        ec2 = boto3.client('ec2', region_name=region_name)
        response = ec2.describe_instances(InstanceIds=[id,],)
        print(response)
        client = boto3.client('ec2', region_name=region_name)
        response1 = client.describe_instance_attribute(
    Attribute='groupSet',
    InstanceId=id,
)

        print(response1)
        sg = response1['Groups']
        gp_id = sg[0]
        sg_id = str(gp_id['GroupId'])
        response = client.describe_security_groups(GroupIds=[sg_id])
        print(response)
        print(response['SecurityGroups'][0])
        rules = (response['SecurityGroups'][0])
        current_rules = (rules['IpPermissions'])
        print(current_rules)
        port = int(command_array[3])
        address = (command_array[5])
        result_list = [(v) for d in current_rules for k,v in d.items()]
        print(result_list)
        if port in result_list:
           print("Exists")
           response_msg = json.dumps("Rules you are trying to add are already exists")
           http = urllib3.PoolManager()
           url = "web-hook-url"
           payload = {
         "attachments":  [
           {
             "fallback": "Message",
             "text": ("Security Group Details"),
             "fields": [
               {
                 "title": (response_msg),
                 "value": ("Format: InstanceID, Region , IpProtocol, FromPort, ToPort, IpRanges, Description")
               }
             ],
             "color": "red"
           }
         ],
         "icon_emoji": "gun"
       }
           response = http.request("POST", url, body=json.dumps(payload), headers={'Content-Type': 'application/json'})
        else:
            response_msg = add_ingress(command_text, sg_id)
            print(response_msg)    
            http = urllib3.PoolManager()
            url = "web-hook-url"
            payload = {
          "attachments": [
            {
              "fallback": "Message",
              "text": ("Security Group Details"),
              "fields": [
                {
                  "title": (response_msg),
                  "value": ("Format: InstanceID, index , IpProtocol, FromPort, ToPort, IpRanges, Description")
                }
              ],
              "color": "red"
            }
          ],
          "icon_emoji": "gun"
        }
            response = http.request("POST", url, body=json.dumps(payload), headers={'Content-Type': 'application/json'})

    elif "Adding Egress" in command_text:
        command_array = (command_text.split(",")) 
        print(command_array)
        numb = command_array[0]
        region_name = command_array[1]
        RunningInstances = get_list(command_text)
        id = RunningInstances[int(numb)]
        print(id)
        ec2 = boto3.client('ec2', region_name=region_name)
        print(id)
        response = ec2.describe_instances(InstanceIds=[id,],)
    
        print(response)
        client = boto3.client('ec2', region_name=region_name)
        response1 = client.describe_instance_attribute(
    Attribute='groupSet',
    InstanceId=id,
)

        print(response1)
        sg = response1['Groups']
        gp_id = sg[0]
        sg_id = gp_id['GroupId']
        response = client.describe_security_groups(GroupIds=[sg_id])
        print(response)
        print(response['SecurityGroups'][0])
        rules = (response['SecurityGroups'][0])
        current_rules =(rules['IpPermissionsEgress'])
        print(current_rules)
        port = int(command_array[3])
        address = (command_array[5])
        result_list = [(v) for d in current_rules for k,v in d.items()]
        print(result_list)
        if port in result_list:
           print("Exists")
           response_msg = json.dumps("Rules you are trying to add are already exists")
           http = urllib3.PoolManager()
           url = "web-hook-url"
           payload = {
         "attachments": [
           {
             "fallback": "Message",
             "text": ("Security Group Details"),
             "fields": [
               {
                 "title": (response_msg),
                 "value": ("Format: InstanceID, Region , IpProtocol, FromPort, ToPort, IpRanges, Description")
               }
             ],
             "color": "red"
           }
         ],
         "icon_emoji": "gun"
       }
           response = http.request("POST", url, body=json.dumps(payload), headers={'Content-Type': 'application/json'})
   
        else:
            response_msg = add_egress(command_text, sg_id)
            print(response_msg)    
            http = urllib3.PoolManager()
            url = "web-hook-url"
            payload = {
          "attachments": [
            {
              "fallback": "Message",
              "text": ("Security Group Details"),
              "fields": [
                {
                  "title": (response_msg),
                  "value": ("Format: InstanceID, Region , IpProtocol, FromPort, ToPort, IpRanges, Description")
                }
              ],
              "color": "red"
            }
          ],
          "icon_emoji": "gun"
        }
            response = http.request("POST", url, body=json.dumps(payload), headers={'Content-Type': 'application/json'})
    elif "Stop Instance" in command_text:
        response_msg = stop_instance(command_text)        
    
    else:
        response_msg = json.dumps("Invalid Command, Enter commands according to the given format!!")
        http = urllib3.PoolManager()
        url = "web-hook-url"
        payload = {
          "attachments": [
            {
              "fallback": "Message",
              "text": ("Error!!"),
              "fields": [
                {
                  "title": (),
                  "value": (response_msg)
                }
              ],
              "color": "red"
            }
          ],
          "icon_emoji": "gun"
        }
        response = http.request("POST", url, body=json.dumps(payload), headers={'Content-Type': 'application/json'})    
                 
        
def stop_instance(command_text):
    command_array = (command_text.split(",")) 
    numb = command_array[0]
    region_name = command_array[1]
    client=boto3.client('ec2', region_name=region_name)
    print(command_array)
    RunningInstances = get_list(command_text)
    if len(RunningInstances) > 0 :
        id = RunningInstances[int(numb)]
        print(id)
        title = "Instance has been stopped successfully!!"
        response = client.stop_instances(
        InstanceIds=[
        id,
        ],
        Force=True|False
        )
    else:
        response = "The Instance is already been stopped!!"
        title = "------------------------------------"
    http = urllib3.PoolManager()
    url = "web-hook-url"
    payload = {
      "attachments": [
        {
          "fallback": "Message",
          "text": ("Stopping Instance"),
          "fields": [
            {
              "title": (title),
              "value": (response)
            }
          ],
          "color": "red"
        }
      ],
      "icon_emoji": "gun"
    }
    response = http.request("POST", url, body=json.dumps(payload), headers={'Content-Type': 'application/json'})    
    
   
