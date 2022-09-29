#!/usr/bin/env python3

import boto3

client = boto3.client('pricing')
paginator = client.get_paginator('describe_services')

services = []

response_iterator = paginator.paginate(
    PaginationConfig={
        # 'MaxItems': 5,
        'PageSize': 10
    }
)

for page in response_iterator:
    for service in page['Services']:
        services.append(service)
        # print(service)

with open('services.html', 'w') as _out:
    for item in sorted(services, key=lambda x: x['ServiceCode'].lower()):
        _out.write(f"<ul><li><div>{item['ServiceCode']}</div><ul>")
        _out.write("\n")
        for attribute in sorted(item['AttributeNames'], key=lambda x: x.lower()): 
            _out.write(f"<li>{attribute}</li>")
        _out.write("\n")
        _out.write("</ul></ul>")
        _out.write("\n")



