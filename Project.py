## imported necessary modules
import json
from pathlib import Path
from dax_extract import read_data_model_schema
import requests
import openai
import os
from tkinter import filedialog
import xlwt
from xlwt import Workbook

## opening file dialog to
file = filedialog.askopenfilename(title="Select file")
# print(file)
#

x = list(file)
x[-1] = 't'
file = ''.join(x)

# taking path of pbit file
pbit_path = Path(file)
print(pbit_path)


data = read_data_model_schema(pbit_path)
openai.api_key = "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"

# getting the datas in json format
data_str = json.dumps(data)
json_object = json.loads(data_str)
# print(json.dumps(json_object, indent=1))
# print(json.dumps(json_object, indent=3))

# Workbook is created
wb = Workbook()
# creating sheet for measures
Measures = wb.add_sheet('Measures')
Measures.write(0, 0, 'Measure Name')
Measures.write(0, 1, 'Measure Expression')
Measures.write(0, 2, 'Measure Description')

# print("\n")
# print("MEASURES")
cnt = 0
for t in data['model']['tables']:
    if 'measures' in t:
        list_measures = t['measures']
        for i in list_measures:
            prompt="Explain the following calculation in a few sentences in simple business terms without using DAX function names: "+i['expression']
            completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=64)
            # print("Measure Name : ", i['name'])
            # print("Measure Expression : ", i['expression'])
            # print("Measure Description: ", completion.choices[0]['text'].strip())
            cnt += 1
            # output.write(i['name'] + "," + i['expression'] + ", descript")
            # output.write('\n')
            Measures.write(cnt, 0, i['name'])
            Measures.write(cnt, 1, i['expression'])
            Measures.write(cnt, 2, completion.choices[0]['text'].strip())



# print("\n")
# print("SOURCE OF INFORMATION")
i = 0
# creating sheet for source information
source = wb.add_sheet('Source Information')
source.write(0, 0, 'Table No.')
source.write(0, 1, 'Path')
for t in data['model']['tables']:
    if 'partitions' in t:
        list_partitions= t['partitions']
        List_source = (list_partitions[0]['source']['expression'])
        if List_source[0] == 'let':
            i += 1
            # print("Table " + str(i) + " Path :" + List_source[1])
            p = List_source[1].split("(")[2].split(")")
            source.write(i, 0, i)
            source.write(i, 1, p[0])


# print("\n")
# print("RELATIONSHIPS")
# creating sheet for source information
relation = wb.add_sheet('Relationships')
relation.write(0, 0, 'From Table')
relation.write(0, 1, 'From Column')
relation.write(0, 2, 'To Table')
relation.write(0, 3, 'To Column')
relation.write(0, 4, 'Direction')
relation.write(0, 5, 'Cardinality')
cnt1 = 0
for t in data['model']['relationships']:
    # print("From Table : ", t['fromTable'])
    # print("From Column : ", t['fromColumn'])
    # print("To Table : ", t['toTable'])
    # print("To Column : ", t['toColumn'])
    # print("Direction : ", t['crossFilteringBehavior'])
    # print("Cardinality : ", t['toCardinality'])
    cnt1 += 1
    relation.write(cnt1, 0, t['fromTable'])
    relation.write(cnt1, 1, t['fromColumn'])
    relation.write(cnt1, 2, t['toTable'])
    relation.write(cnt1, 3, t['toColumn'])
    relation.write(cnt1, 4, t['crossFilteringBehavior'])
    relation.write(cnt1, 5, t['toCardinality'])


wb.save('Details.xls')

