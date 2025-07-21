# ██████╗  █████╗ ██╗   ██╗██████╗  ██████╗ ██╗     ██╗            ██╗██╗███████╗     ██████╗ ██████╗ ██████╗ ██████╗ ███████╗ ██████╗████████╗ ██████╗ ██████╗ 
# ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗██╔═══██╗██║     ██║            ██║██║██╔════╝    ██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
# ██████╔╝███████║ ╚████╔╝ ██████╔╝██║   ██║██║     ██║            ██║██║█████╗      ██║     ██║   ██║██████╔╝██████╔╝█████╗  ██║        ██║   ██║   ██║██████╔╝
# ██╔═══╝ ██╔══██║  ╚██╔╝  ██╔══██╗██║   ██║██║     ██║            ██║██║██╔══╝      ██║     ██║   ██║██╔══██╗██╔══██╗██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
# ██║     ██║  ██║   ██║   ██║  ██║╚██████╔╝███████╗███████╗    ██╗██║██║██║         ╚██████╗╚██████╔╝██║  ██║██║  ██║███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
# ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝    ╚═╝╚═╝╚═╝╚═╝          ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
#                                                                                                                                           
# / Created: 07-2025 / Last Updated: 07-2025 / Author: L. Brown                                                                                                                                           
# 
#   3 STEPS TO USE THIS CODE:
#
#       1. =SETUP=      Make sure your "iif_folder_path" (saved in "config.json") contains the iif file you want to clean (ex. ExportSummary-xxxxxxxx.iif). 
#                           -NOTE: You can get this from Patriot by going to Payroll > Export Payroll.
#       2. =WORK=       Run the code by executing the following program once.
#                           -NOTE: You will be prompted with a confirmation dialogue before any changes are made. 
#       3. =CLEANUP=    archive section tbd
#

import os
import re
import glob
import csv
import json
import tkinter as tk
from tkinter import messagebox

# Load names, file locations, accounts from config.json file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

name_map = config['employee_name_map']
memo_account_map = config['memo_account_map']
folder_path = config['iif_folder_path']

###############################################################
# Function to match names to QB Employee List names
def convert_memo_name(memo: str) -> str:
    name_match = re.match(r'(.*?):', memo)
    if not name_match:
        return memo
    name = name_match.group(1).strip()
    return name_map.get(name, name)
###############################################################

###############################################################
# Function to clean up and reformat the data in the .iif file
def clean_and_save_daysheet(iif_file_path):
    try:
        with open(iif_file_path, 'r') as file:
            reader = csv.reader(file, delimiter='\t')
            lines = list(reader)

        new_trns_header = ['!TRNS', 'TRNSTYPE', 'DATE', 'ACCNT', 'AMOUNT', 'DOCNUM', 'MEMO', 'NAME']
        new_spl_header = ['!SPL', 'TRNSTYPE', 'DATE', 'ACCNT', 'AMOUNT', 'DOCNUM', 'MEMO', 'NAME']
        endtrns = ['!ENDTRNS']

        employee_entries = {}
        original_docnum = None
        
        for line in lines:
            if not line or line[0].startswith('!') or line[0] == 'ENDTRNS':
                continue

            if line[0] not in ('TRNS', 'SPL'):
                continue

            trnstype = line[2]
            date = line[3]
            accnt = line[4]
            amount = line[6]
            docnum = line[7]
            memo = line[8] if len(line) > 8 else ''
            name = convert_memo_name(memo)
            
            if not original_docnum and docnum.isdigit():
                original_docnum = int(docnum)

            if accnt == 'Payroll Taxes':
                for keyword, new_accnt in memo_account_map.items():
                    if keyword in memo:
                        accnt = new_accnt
                        break

            entry_type = line[0]
            line_data = [entry_type, trnstype, date, accnt, amount, docnum, memo, name]

            if name not in employee_entries:
                employee_entries[name] = []
            employee_entries[name].append(line_data)

        if original_docnum is None:
            raise ValueError("No valid DOCNUM found in the original file.")

        sorted_employees = sorted(employee_entries.keys())
        result_lines = [new_trns_header, new_spl_header, endtrns]

        for idx, employee in enumerate(sorted_employees):
            assigned_docnum = str(original_docnum + idx)
            for i, line in enumerate(employee_entries[employee]):
                line[5] = assigned_docnum
                line[0] = 'TRNS' if i == 0 else 'SPL'
                result_lines.append(line)
            result_lines.append(['ENDTRNS'])

        with open(iif_file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(result_lines)

        print(f"File successfully cleaned and saved to: {iif_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
###############################################################

###############################################################
# Get most recent .iif file from the correct folder
def get_most_recent_file(folder_path):
    files = glob.glob(os.path.join(folder_path, "*.iif"))
    if not files:
        raise FileNotFoundError("No .iif files found in the specified folder.")
    return max(files, key=os.path.getmtime)
###############################################################

###############################################################
# Start confirmation dialog
def show_start_dialog():
    root = tk.Tk()
    root.withdraw()
    response = messagebox.askokcancel(
        "LB's Payroll Export Format-inator v0.1",
        f"You are about to reformat the most recently saved .iif file in {folder_path}. "
        "Do you want to continue?"
    )
    return response
###############################################################

# Main execution
if __name__ == "__main__":
    try:
        if not show_start_dialog():
            print("Program exited by user.")
            exit()

        iif_file_path = get_most_recent_file(folder_path)
        print(f"Using file: {iif_file_path}")
        clean_and_save_daysheet(iif_file_path)

    except FileNotFoundError as e:
        print(e)
        exit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit()