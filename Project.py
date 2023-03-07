## imported necessary modules
import json
import pathlib
from pathlib import Path
from dax_extract import read_data_model_schema
import requests
import openai
import os
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askdirectory
import xlwt
from xlwt import Workbook


## created open AI key
openai.api_key = "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"

## function defined to extract the data
def extractData(file):
    ## getting the directory name
    dir_name = os.path.dirname(file)

    ## getting file base name
    file_name = Path(file).stem

    x = list(file)
    x[-1] = 't'
    file = ''.join(x)

    # taking path of pbit file
    pbit_path = Path(file)

    ## reading data in json format
    data = read_data_model_schema(pbit_path)
    # getting the datas in json format
    # data_str = json.dumps(data)
    # json_object = json.loads(data_str)
    # print(json.dumps(json_object, indent=3))

    ## saving to dataset folder
    new_dir = pathlib.Path(dir_name, "Output")
    new_dir.mkdir(parents=True, exist_ok=True)
    # You have to make a file inside the new directory
    file_name += ".json"

    ## saving the data in json format
    save1 = str(new_dir) + "\\" + file_name
    out_file = open(Path(save1), "w")

    json.dump(data, out_file, indent=6)

    ## saving file to current location of python file only
    # save_path = dirname + "/" + file_name + ".json"
    # Path(save_path).touch()

    out_file.close()




## printing the menu
print("Do you want to select file or folder\n1.File\n2.Folder")

## asking user for option
op = int(input("\nEnter Option : "))

if(op==1):
    # opening file dialog to select file
    file = filedialog.askopenfilename(title="Select file")
    print(file)
    extractData(file)
else:
    ## opening file dialog to select folder
    folder = askdirectory(title="Select folder")
    print(folder)

    # # Change the directory
    # os.chdir(folder)

    # def read_files(file_path):
    #     with open(file_path, 'r') as file:
    #         print(file.read())

    # Iterate over all the files in the directory
    for f in os.listdir():
        ## searching for file with specific file extension
        if f.endswith('.pbix'):
            # Create the filepath of particular file
            file_path = f"{folder}/{f}"
            print(file_path)
            # read_files(file_path)
            extractData(file_path)

#
# # Workbook is created
# wb = Workbook()
# # creating sheet for measures
# Measures = wb.add_sheet('Measures')
# Measures.write(0, 0, 'Measure Name')
# Measures.write(0, 1, 'Measure Expression')
# Measures.write(0, 2, 'Measure Description')
#
# # print("\n")
# # print("MEASURES")
# cnt = 0
# for t in data['model']['tables']:
#     if 'measures' in t:
#         list_measures = t['measures']
#         for i in list_measures:
#             prompt="Explain the following calculation in a few sentences in simple business terms without using DAX function names: "+i['expression']
#             completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=64)
#             # print("Measure Name : ", i['name'])
#             # print("Measure Expression : ", i['expression'])
#             # print("Measure Description: ", completion.choices[0]['text'].strip())
#             cnt += 1
#             # output.write(i['name'] + "," + i['expression'] + ", descript")
#             # output.write('\n')
#             Measures.write(cnt, 0, i['name'])
#             Measures.write(cnt, 1, i['expression'])
#             Measures.write(cnt, 2, completion.choices[0]['text'].strip())
#
#
#
# # print("\n")
# # print("SOURCE OF INFORMATION")
# i = 0
# # creating sheet for source information
# source = wb.add_sheet('Source Information')
# source.write(0, 0, 'Table No.')
# source.write(0, 1, 'Table Name')
# source.write(0, 2, 'Source')
# for t in data['model']['tables']:
#     if 'partitions' in t:
#         list_partitions= t['partitions']
#         List_source = (list_partitions[0]['source']['expression'])
#         if List_source[0] == 'let':
#             name = list_partitions[0]['name'].split('-')[0]
#             i += 1
#             # print("Table " + str(i) + " Path :" + List_source[1])
#             # p = List_source[1].split("(")[2].split(")")
#             p = List_source[1]
#             source.write(i, 0, i)
#             source.write(i, 1, name)
#             source.write(i, 2, p)
#
#
# # print("\n")
# # print("RELATIONSHIPS")
# # creating sheet for source information
# relation = wb.add_sheet('Relationships')
# relation.write(0, 0, 'From Table')
# relation.write(0, 1, 'From Column')
# relation.write(0, 2, 'To Table')
# relation.write(0, 3, 'To Column')
# cnt1 = 0
#
# for t in data['model']['relationships']:
#     # print("From Table : ", t['fromTable'])
#     # print("From Column : ", t['fromColumn'])
#     # print("To Table : ", t['toTable'])
#     # print("To Column : ", t['toColumn'])
#     # print("Direction : ", t['crossFilteringBehavior'])
#     # print("Cardinality : ", t['toCardinality'])
#     if "joinOnDateBehavior" not in t:
#         cnt1 += 1
#         relation.write(cnt1, 0, t['fromTable'])
#         relation.write(cnt1, 1, t['fromColumn'])
#         relation.write(cnt1, 2, t['toTable'])
#         relation.write(cnt1, 3, t['toColumn'])
#     if "crossFilteringBehavior" in t:
#         relation.write(0, 4, 'Direction')
#         relation.write(cnt1, 4, t['crossFilteringBehavior'])
#
#     if "toCardinality" in t:
#         relation.write(0, 5, 'Cardinality')
#         relation.write(cnt1, 5, t['toCardinality'])
#
#
# wb.save('Details.xls')
#
