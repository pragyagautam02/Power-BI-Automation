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
import xlrd
import pandas as pd
from xlwt import Pattern
import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo


## created open AI key
openai.api_key = "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"

## ============================================================================================================================================
## function defined to extract the data in xls format
def xls_extract(data, file, base_file_name):
    # print(base_file_name)

    # Workbook is created
    # wb = Workbook()

    # creating sheet for measures
    # Measures = wb.add_sheet('Measures')
    # Measures.write(0, 0, 'Measure Name')
    # Measures.write(0, 1, 'Measure Expression')
    # Measures.write(0, 2, 'Measure Description')

    ## ----------------------------------------------------- MEASURES ----------------------------------------------------------------------
    wb = openpyxl.Workbook()
    ws = wb.create_sheet(title="Measures")
    ws.append(['Measure Name', 'Measure Expression', 'Measure Description'])
    cnt = 1
    for t in data['model']['tables']:
        if 'measures' in t:
            list_measures = t['measures']
            for i in list_measures:
                prompt = "Explain the following calculation in a few sentences in simple business terms without using DAX function names: " + i['expression']
                completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=64)
                cnt += 1
                ws.append([i['name'], i['expression'], completion.choices[0]['text'].strip()])

    table = Table(displayName="Table1", ref="A1:C" + str(cnt))
    ws.add_table(table)

    # cnt = 0
    # for t in data['model']['tables']:
    #     if 'measures' in t:
    #         list_measures = t['measures']
    #         for i in list_measures:
    #             prompt = "Explain the following calculation in a few sentences in simple business terms without using DAX function names: " + str(i['expression'])
    #             completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=64)
    #             cnt += 1
    #             Measures.write(cnt, 0, i['name'])
    #             Measures.write(cnt, 1, i['expression'])
    #             Measures.write(cnt, 2, completion.choices[0]['text'].strip())

    ## ----------------------------------------------------- SOURCE INFORMATION ----------------------------------------------------------------------
    # Apply some style to the table
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False, showRowStripes=True,
                           showColumnStripes=False)
    table.tableStyleInfo = style
    source = wb.create_sheet('Source Information')
    source.append(['Table No', 'Table Name', 'Table Type', 'Table Source'])
    i = 0
    for t in data['model']['tables']:
        if 'partitions' in t:
            list_partitions = t['partitions']
            List_source = (list_partitions[0]['source']['expression'])
            if List_source[0] == 'let':
                name = list_partitions[0]['name'].split('-')[0]
                i += 1
                p = List_source[1]
                Ttype = p.split("(")[0].split('= ')[1]

                st = 0
                ed = len(p) - 1
                while (p[st] != '"'):
                    st += 1
                while (p[ed] != '"'):
                    ed -= 1
                # print(st, ed)
                TSource = p[st: ed + 1]
                source.append([i, name, Ttype, TSource])

    i += 1
    table = Table(displayName="Source", ref="A1:D" + str(i))
    source.add_table(table)

    # Apply some style to the table
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False, showRowStripes=True,
                           showColumnStripes=False)
    table.tableStyleInfo = style

    # i = 0
    # # creating sheet for source information
    # source = wb.add_sheet('Source Information')
    # source.write(0, 0, 'Table No.')
    # source.write(0, 1, 'Table Name')
    # source.write(0, 2, 'Table Type')
    # source.write(0, 3, 'Table Source')
    # for t in data['model']['tables']:
    #     if 'partitions' in t:
    #         list_partitions = t['partitions']
    #         List_source = (list_partitions[0]['source']['expression'])
    #         if List_source[0] == 'let':
    #             name = list_partitions[0]['name'].split('-')[0]
    #             i += 1
    #             p = List_source[1]
    #             Ttype = p.split("(")[0].split('= ')[1]
    #
    #             st = 0
    #             ed = len(p)-1
    #             while(p[st]!='"'):
    #                 st += 1
    #             while(p[ed]!='"'):
    #                 ed -= 1
    #             # print(st, ed)
    #             TSource = p[st : ed+1]
    #
    #
    #             source.write(i, 0, i)
    #             source.write(i, 1, name)
    #             source.write(i, 2, Ttype)
    #             source.write(i, 3, TSource)

    ## ----------------------------------------------------- RELATIOPNSHIPS ----------------------------------------------------------------------
    relation = wb.create_sheet('Relationships')
    cnt1 = 0
    relation.append(['From Table', 'From Column', 'To Table', 'To Column', 'State', 'Direction', 'Cardinality'])

    if 'relationships' in data['model']:
        for t in data['model']['relationships']:
            d = ""
            a = ""
            if "joinOnDateBehavior" not in t:
                cnt1 += 1
                if "crossFilteringBehavior" in t:
                    d = "Both Directional"
                else:
                    d = "Single Directional"

                if "toCardinality" in t:
                    if t['toCardinality'] == "one":
                        a = 'One to one (1:1)'
                    elif t['toCardinality'] == "many":
                        a = 'Many to many (*:*)'
                    else:
                        pass

                elif "fromCardinality" in t:
                    if t['fromCardinality'] == "one":
                        a = 'One to one (1:1)'
                    elif t['fromCardinality'] == "many":
                        a = 'Many to many (*:*)'
                    else:
                        pass
                else:
                    a = 'Many to one (*:1)'

                relation.append([t['fromTable'], t['fromColumn'], t['toTable'], t['toColumn'], t['state'], d, a])
    else:
        print('No Relation')

    table = Table(displayName="Relationships", ref="A1:G" + str(cnt1 + 1))
    relation.add_table(table)

    # Apply some style to the table
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False, showRowStripes=True,showColumnStripes=False)
    table.tableStyleInfo = style
    dir_name = os.path.dirname(file)
    new_dir = pathlib.Path(dir_name, "EXCEL Output")
    new_dir.mkdir(parents=True, exist_ok=True)
    file_name = base_file_name + ".xlsx"
    save1 = str(new_dir) + "\\" + file_name
    wb.save(save1)
    workbook = openpyxl.load_workbook(save1)
    sheet_to_remove = workbook['Sheet']
    workbook.remove(sheet_to_remove)
    workbook.save(save1)
    #
    # relation = wb.add_sheet('Relationships')
    # relation.write(0, 0, 'From Table')
    # relation.write(0, 1, 'From Column')
    # relation.write(0, 2, 'To Table')
    # relation.write(0, 3, 'To Column')
    # relation.write(0, 4, 'State')
    # relation.write(0, 5, 'Direction')
    # relation.write(0, 6, 'Cardinality')
    # cnt1 = 0
    #
    # # try:
    # if 'relationships' in data['model']:
    #     for t in data['model']['relationships']:
    #         if "joinOnDateBehavior" not in t:
    #             cnt1 += 1
    #             relation.write(cnt1, 0, t['fromTable'])
    #             relation.write(cnt1, 1, t['fromColumn'])
    #             relation.write(cnt1, 2, t['toTable'])
    #             relation.write(cnt1, 3, t['toColumn'])
    #             relation.write(cnt1, 4, t['state'])
    #
    #             if "crossFilteringBehavior" in t:
    #                 relation.write(cnt1, 5, "Both Directional")
    #             else:
    #                 relation.write(cnt1, 5, "Single Directional")
    #
    #             if "toCardinality" in t:
    #                 if t['toCardinality'] == "one":
    #                     relation.write(cnt1, 6, 'One to one (1:1)')
    #                 elif t['toCardinality'] == "many":
    #                     relation.write(cnt1, 6, 'Many to many (*:*)')
    #                 else:
    #                     pass
    #
    #             elif "fromCardinality" in t:
    #                 if t['fromCardinality'] == "one":
    #                     relation.write(cnt1, 6, 'One to one (1:1)')
    #                 elif t['fromCardinality'] == "many":
    #                     relation.write(cnt1, 6, 'Many to many (*:*)')
    #                 else:
    #                     pass
    #             else:
    #                 relation.write(cnt1, 6, 'Many to one (*:1)')
    # else:
    #     print("NO relation")
    # # except:
    # #     print("No Relation")
    # dir_name = os.path.dirname(file)
    # # print(dir_name)
    #
    # ## saving to dataset folder
    # new_dir = pathlib.Path(dir_name, "EXCEL Output")
    # # print(new_dir)
    # new_dir.mkdir(parents=True, exist_ok=True)
    # # You have to make a file inside the new directory
    # file_name = base_file_name + ".xls"
    #
    # ## saving the data in json format
    # save1 = str(new_dir) + "\\" + file_name
    # # print(save1)
    #
    # # df = pd.read_excel(save1, header=None)
    # # df.to_excel('Akash.xlsx', index=False, header=False)
    # # wb.save('Akash.xlsx')
    #
    #
    # ## saving the excel workbook file
    # wb.save(save1)

## ============================================================================================================================================
## function defined to extract the data in json format
def json_extract(file):
    ## getting the directory name
    dir_name = os.path.dirname(file)

    ## getting file base name
    base_file_name = Path(file).stem

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
    new_dir = pathlib.Path(dir_name, "JSON Output")
    new_dir.mkdir(parents=True, exist_ok=True)
    # You have to make a file inside the new directory
    file_name = base_file_name + ".json"

    ## saving the data in json format
    save1 = str(new_dir) + "\\" + file_name
    out_file = open(Path(save1), "w")

    json.dump(data, out_file, indent=6)

    ## saving file to current location of python file only
    # save_path = dirname + "/" + file_name + ".json"
    # Path(save_path).touch()

    out_file.close()

    xls_extract(data, file, base_file_name)

## --------------------------------------------------------------- MAIN -------------------------------------------------------------------------
## printing the menu
print("Do you want to select file or folder\n1.File\n2.Folder")

## asking user for option
op = int(input("\nEnter Option : "))

if(op==1):
    # opening file dialog to select file
    file = filedialog.askopenfilename(title="Select file")
    # print(file)
    json_extract(file)
elif(op==2):
    ## opening file dialog to select folder
    folder = askdirectory(title="Select folder")
    # print(folder)

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
            # print(file_path)
            # print(file_path)
            # read_files(file_path)
            json_extract(file_path)
else:
    print("Invalid Input")


