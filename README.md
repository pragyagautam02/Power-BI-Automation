## ✔ Power BI Automation Using Open AI API
- A python script to automate the extraction of Report Details from Power Bi(.pbix) Files.
- In the scripts, first user need to select a pbix file from the File Selecting Dialog Box, and then the program will extract the details from that selected power bi file.
- And after the extraction is done, the program will internally store the details in the Excel Workbook Formats, JSON formats and Finally creates the updated the pbit file in separate folder.

****

### REQUIREMENTS :
- python 3
- os 
- tkinter 
- filedialog, Tk from tkinter
- askdirectory from tkinter.filedialog
- openpyxl
- Table, TableStyleInfo from openpyxl.worksheet.table
- Alignment from openpyxl.styles.alignment
- codecs
- json
- zipfile
- pathlib
- Path from pathlib
- openai
- os
- shutil

****

### How To Use it :
- User just need to download the file, and run the Project.py, on local system.
- After running the file, user will be provided with following three selection options:
    - Single .pbix file
    - Multiple .pbix file
    - A Folder
- After selection is done by user, the respective pop up will open for selecting respective option from the local system.
- Then in the backend the python script will follow the below steps inorder to extract details:
    - first converted the pbix file to pbit file via exporting
    - then read the pbit file in json format
    - then from the json file, using the indexing, it extracted the details like measures, relationships and the source information.
    - then for each measures and modification, we got the description of that measures using Open AI API.
- After this part is done, then the final extracted details are being stored in three folders namely EXCEL Output. JSON Output and UPDATED pbit.
- In EXCEL Output directory, there will be details for Measures, Source Information and Relationships in respective sheets.
- In JSON Output directory, there will be the DataModelSchema for each of the pbix file.
- In Updated pbit directory, there will be pbit file for each pbix file, with measures and modifications description inside it fetched from Open AI API.

### Purpose :
- This scripts helps user to get the extract the Measures and its description, Source Information and the Relationships.

### Compilation Steps :
- Install the mentioned required modules.
- After that download the code file, and run Project.py on local system.
- Then the script will start running and user can explore it by selecting different option as per user's requirement and checking the extracted details.