#!/usr/bin/env python3

import json
import re

from string import Template

with open('../get_raw_price_data/data.json') as _json:
    raw_data = json.load(_json)

products = []

gpu_names = {
    'p4d': 'NVIDIA A100 Tensor Core',
    'p4de': 'NVIDIA A100 Tensor Core',
    'p3': 'NVIDIA Tesla V100',
    'p3dn': 'NVIDIA Tesla V100',
    'p2': 'NVIDIA K80',
    'g5': 'NVIDIA A10G Tensor Core',
    'g5g': 'NVIDIA T4G Tensor Core',
    'g4dn': 'NVIDIA T4 Tensor Core',
    'g4ad': 'AMD Radeon Pro V520',
    'g3': 'NVIDIA Tesla M60',
    'g3s': 'NVIDIA Tesla M60',
    'g2': '(Not listed)'
}

# Post filter here. 
for item in raw_data:
    if 'instanceType' in item['product']['attributes']:
        if item['product']['attributes']['tenancy'] == 'Shared':
            if item['product']['attributes']['marketoption'] == 'OnDemand':
                if item['product']['attributes']['capacitystatus'] == 'Used':
                    if item['product']['attributes']['preInstalledSw'] == 'NA':
                        item['cost'] = round(float(list(list(item['terms']['OnDemand'].items())[0][1]['priceDimensions'].items())[0][1]['pricePerUnit']['USD']), 3)
                        item['name_key'] = item['product']['attributes']['instanceType'].split('.')[0]
                        if item['name_key'] in gpu_names:
                            item['gpu_name'] = gpu_names[item['name_key']]
                            item['family_with_gpu'] = f"{item['product']['attributes']['instanceFamily']} {gpu_names[item['name_key']]}"
                        else:
                            item['gpu_name'] = ''
                            item['family_with_gpu'] = f"{item['product']['attributes']['instanceFamily']}"
                        if 'gpu' in item['product']['attributes']:
                            item['gpu'] = item['product']['attributes']['gpu']
                        else:
                            item['gpu'] = '0'
                        products.append(item)

# skeleton = Template("""<!DOCTYPE html>
# <html><head><style>
# body { background-color: #222; color: #588; }
# td { vertical-align: top; padding-right: 8px; }
# .name_1, .name_2, .vcpu, .gpu, .memory { text-align: center;}
# </style>
# <body><table><tbody><tr>
# <th>Family</th>
# <th colspan="2">Name</th>
# <th>vCPUs</th>
# <th>GPUs</th>
# <th>Memory</th>
# <th>Cost/Hour</th>
# </tr>
# $TABLE_ROWS
# </tbody></table></body></html>
# """)

table_rows = ''
for item in sorted(
        products, 
        key=lambda 
        x: (
            x['family_with_gpu'],
            x['product']['attributes']['instanceFamily'], 
            x['cost'], 
            x['product']['attributes']['instanceType'].split('.')[0],
            int(x['product']['attributes']['vcpu']),
            x['product']['attributes']['instanceType'])
        ):

    matches = re.search(
        r"(\w+)(\d+)(.*)", 
        item['product']['attributes']['instanceType'].split('.')[0]
    )
    item['name_1'] = matches.group(1)
    item['name_2'] = matches.group(2)
    item['name_3'] = matches.group(3)

    # item['name_key'] = item['product']['attributes']['instanceType'].split('.')[0]

    # gpu_names = {
    #     'p4d': 'NVIDIA A100 Tensor Core',
    #     'p4de': 'NVIDIA A100 Tensor Core',
    #     'p3': 'NVIDIA Tesla V100',
    #     'p3dn': 'NVIDIA Tesla V100',
    #     'p2': 'NVIDIA K80',
    #     'g5': 'NVIDIA A10G Tensor Core',
    #     'g5g': 'NVIDIA T4G Tensor Core',
    #     'g4dn': 'NVIDIA T4 Tensor Core',
    #     'g4ad': 'AMD Radeon Pro V520',
    #     'g3': 'NVIDIA Tesla M60',
    #     'g3s': 'NVIDIA Tesla M60',
    #     'g2': '(Not listed)'
    # }

    # if item['name_key'] in gpu_names:
    #     item['gpu_name'] = gpu_names[item['name_key']]
    # else:
    #     item['gpu_name'] = ''
    # if 'gpu' in item['product']['attributes']:
    #     item['gpu'] = item['product']['attributes']['gpu']
    # else:
    #     item['gpu'] = '0'


    # item['family_with_gpu'] = item['family_with_gpu'].replace(' Instances', '').replace('Machine Learning', 'ML').replace('optimized', '').replace('instance', '').replace('purpose', '').replace('Accelerator', '')
    item['family_with_gpu'] = item['family_with_gpu'].replace(' instance', '').replace(' Instances', '')

    # NOTE: this assumes there's only one item in the OnDemand
    # terms - that's true for my use case, but check your math
    # if you give it a try. 
    table_rows += f"""
<tr>
<td class="family">{item['family_with_gpu']}</td>
<td class="name_1">{item['product']['attributes']['instanceType'].split('.')[0]}</td>
<td class="name_2">{item['product']['attributes']['instanceType'].split('.')[1]}</td>
<td class="vcpu">{item['product']['attributes']['vcpu']}</td>
<td class="gpu">{item['gpu']}</td>
<td class="memory">{item['product']['attributes']['memory'].replace(' GiB', '')}</td>
<td class="cost">{item['cost']}</td>
</tr>
"""


with open('template.html') as _template:
    skeleton = Template(_template.read())
    with open('../../site/index.html', 'w') as _out:
        _out.write(skeleton.substitute(TABLE_ROWS=table_rows))


