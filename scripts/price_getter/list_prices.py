#!/usr/bin/env python3

import json

from string import Template


with open('raw_price_data.json') as _json:
    raw_data = json.load(_json)

products = []

for item in raw_data:
    if 'instanceType' in item['product']['attributes']:
        if item['product']['attributes']['tenancy'] == 'Shared':
            if item['product']['attributes']['marketoption'] == 'OnDemand':
                if item['product']['attributes']['capacitystatus'] == 'Used':
                    if item['product']['attributes']['preInstalledSw'] == 'NA':
                        item['cost'] = list(list(item['terms']['OnDemand'].items())[0][1]['priceDimensions'].items())[0][1]['pricePerUnit']['USD']
                #if item['product']['attributes']['instanceFamily'] == 'GPU instance':
                        products.append(item)

        # print(item['product']['attributes']['instance'])
        #if 'instanceType' not in item['product']['attributes']:
            #print(item)

skeleton = Template("""<!DOCTYPE html>
<html>
<head>
<style>
body { background-color: #222; color: #588; }
td { vertical-align: top; }
</style>
<body>
<table><tbody>
$TABLE_ROWS
</tbody></table>
</body>
</html>
""")

table_rows = ''
for item in sorted(
        products, 
        key=lambda 
        x: (
            x['product']['attributes']['instanceFamily'], 
            x['product']['attributes']['instanceType'].split('.')[0],
            int(x['product']['attributes']['vcpu']),
            x['product']['attributes']['instanceType'])
        ):
    # NOTE: this assumes there's only one item in the OnDemand
    # terms - that's true for my use case, but check your math
    # if you give it a try. 
    table_rows += f"""
<tr>
<td>{item['product']['attributes']['instanceFamily']}</td>
<td>{item['product']['attributes']['instanceType']}</td>
<td>{item['product']['attributes']['vcpu']}</td>
<td>{item['cost']}</td>
<td>{list(list(item['terms']['OnDemand'].items())[0][1]['priceDimensions'].items())[0][1]['pricePerUnit']['USD']}</td>
</tr>
"""

# <td><pre><code>{json.dumps(item, sort_keys=True, indent=2)}</td>
# <td>{item}</td>

with open('prices.html', 'w') as _out:
    _out.write(skeleton.substitute(TABLE_ROWS=table_rows))

