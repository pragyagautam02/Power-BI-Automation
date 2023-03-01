## ✔ Power BI Automation Using Open AI API
- A python script to automate the extraction of Report Details from Power Bi(.pbix) Files.
- In the scripts, first user need to select a pbix file from the File Selecting Dialog Box, and then the program will extract the details from that selected power bi file.
- And after the extraction is done, the program will internally store the details in the Excel Workbook named Details.
****

### REQUIREMENTS :
- python 3
- os 
- tkinter 
- filedialog from tkinter
- json
- Path from pathlib
- read_data_model_schema from dax_extract
- requests
- openai
- xlwt
- Workbook from xlwt
****

### How To Use it :
- User just need to download the file, and run the Project.py, on local system.
- After running a file dialog box will appear, though which we need to select the pbix file, of which we need the report details.
- After selecting the files, in the backend the python script will follow the below steps inorder to extract details:
    - first converted the pbix file to pbit file via exporting
    - then read the pbit file ion json format
    - then from the json file, using the indexing, it extracted the details like measures, relationships and the source information.
    - then for each measures, we got the description of that measures using Open AI API.
- After this part is done, then the final details are being stored in the Excel Workbook, under the three different sheeets.

### Purpose :
- This scripts helps user to get the extract the measures and its description, relationships, and the source informations.

### Compilation Steps :
- Install the mentioned required modules.
- After that download the code file, and run Project.py on local system.
- Then the script will start running and user can explore it by selecting different and extrating the details from it.