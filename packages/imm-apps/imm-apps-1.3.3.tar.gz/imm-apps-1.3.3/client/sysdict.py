from source.excel import Excel
from functools import reduce
import os,json
from pathlib import Path
from pprint import pprint
import argparse

BASEDIR = Path(__file__).parents[1]
# All data directory
DATADIR = BASEDIR / "data"

# get combined excel throgh add up all input excels.
def addupExcels(excels):
    excel_objs = list(map(lambda x: Excel(x), excels))
    return reduce(lambda a, b: a + b, excel_objs)

def getAllExcels(excel_path):
    excels= Path(excel_path).glob("*.xlsx")
    return [str(excel.absolute()) for excel in excels]

def getSheetsDict(merged_excel:Excel):
    sheets_dict={}
    for sheet_name,sheet_obj in merged_excel.sheets.items():
        variables_dict={}
        for variable_name, variable_obj in sheet_obj.data.items():
            variables_dict[variable_name]=variable_obj.description
        sheets_dict[sheet_name]=variables_dict
    return sheets_dict

def getTablesDict(merged_excel:Excel):
    tables_dict={}
    for table_name,table_obj in merged_excel.tables.items():
        variables_dict={}
        for variable_name, variable_title in table_obj.column_titles.items():
            variables_dict[variable_name]=variable_title
        tables_dict[table_name]=variables_dict
    return tables_dict

def save(sysdict:dict,excel_path):
    sysdict_path=  excel_path/"sysdict.json"
    with open(sysdict_path,"w")as f:
        json.dump(sysdict,f,indent=3)
    print(f"{sysdict_path} has been created.")
    
def main():
    parser=argparse.ArgumentParser(description="For generate system dict for variables and descriptions")
    parser.add_argument("-l", "--language", help="Input language name, default is English.")
    args = parser.parse_args()
    
    excel_path=DATADIR / 'excel'/args.language if args.language else DATADIR/'excel'
    if not excel_path.exists():
        print(f"{excel_path} is not exited. The language {args.language} is not supported in current system.")
        exit(1)
    excels=getAllExcels(excel_path)
    merged_excel=addupExcels(excels)
    sheets_dict=getSheetsDict(merged_excel)
    tables_dict=getTablesDict(merged_excel)
    sysdict={**sheets_dict,**tables_dict}
    save(sysdict,excel_path)
    
    
    
if  __name__=="__main__":
    main()
    
    
