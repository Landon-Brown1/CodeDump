# ██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███╗   ██╗    ██████╗ ██████╗ ███████╗    ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
# ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║    ██╔══██╗██╔══██╗██╔════╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
# ██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║██╔██╗ ██║    ██████╔╝██║  ██║█████╗      ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
# ██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║██║╚██╗██║    ██╔═══╝ ██║  ██║██╔══╝      ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
# ██║        ██║      ██║   ██║  ██║╚██████╔╝██║ ╚████║    ██║     ██████╔╝██║         ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
# ╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ╚═╝     ╚═════╝ ╚═╝         ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
# / Created: 05-2024 / Last Updated: 04-2025 / Author: L. Brown                                                                                                                                           
# 
# DISCLAIMER: This is the first time I have written in Python, and I am by no means fluent. Bear with me. :)
#
#   !!!THIS PROGRAM IS CURRENTLY HARDCODED FOR CAREISMATIC INC INVOICES. IT WILL -NOT- WORK FOR OTHER PDFs UNLESS COORDINATES ARE MODIFIED ACCORDINGLY!!!
#   Update coordinates by uncommenting the pdf.tree.write function, and commenting out the code that overwrites all the data. This will make the program instead create an XML 
#   file from all PDFs it reads. Use the XML file to find the coordinates of the data you want, then use those in the LTTextLineHorizontal bounding boxes to create a new dataframe.
#
#   3 STEPS TO USE THIS CODE:
#
#       1. =SETUP=      MAKE SURE THE "res" FOLDER HAS -ONLY- AND -ALL- OF THE INVOICE PDFs YOU WANT TO PROCESS (ex. May invoices). 
#                           -NOTE: You can get these from Outlook by selecting all invoices you need and using the "Project1.SaveAttachmentsToDisk" macro.
#       2. =WORK=       RUN THE CODE BY CLICKING THE PLAY BUTTON IN THE TOP RIGHT CORNER OF THIS SCREEN ONCE.
#                           -NOTE: The output window will notify you when it is done processing invoices, usually runs about 15-30 seconds. 
#       3. =CLEANUP=    ONCE THE CODE IS FINISHED, MOVE THE INVOICES FROM THE "res" FOLDER TO A NEW FOLDER LABELED "res[MONTH_YEAR]" (ex. "res05_24") and,
#                       RENAME "CAREISMATIC_INVOICES_LIST.CSV" TO "CAREISMATIC_INVOICES_LIST [MONTH_YEAR].csv" (ex. "Careismatic_Invoices_List 05_24")
#                           -NOTE: You do not have to do step 3, but if you don't then the invoices/spreadsheet will not be archived.
#
#libraries that contain the functions used in the code below
from datetime import date
import pandas as pd
import pdfquery
import os
from os import listdir
from os.path import isfile, join
import shutil

''''''
# Function to grab your file paths from one library file
def load_paths(file_path):
    paths = {}

    try:
        # Open the file and read
        with open(file_path, 'r') as file:
            # Loop on each line until end of file
            for line in file:
                # Ignore empty and commented lines
                if line.strip() and not line.startswith('#'):
                    # Split the line into key and value, separated by '='
                    key, value = line.strip().split('=', 1)
                    paths[key] = value

    except FileNotFoundError:
        print(f"Error: file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return paths

# Function to clean and convert total_due output for math stuff
def clean_total(val, credit):
    if not val:
        return 0.0  # fallback for empty values

    val = val.replace('$', '').replace(',', '').strip()

    # Remove CR if it exists and note it's a credit
    if credit:
        val = val.upper().replace('CR', '').strip()

    try:
        amount = float(val)
        return -amount if credit else amount
    except ValueError:
        return 0.0  # fallback for weird values


''''''
# Start by getting file paths from library
file_paths = load_paths('lib/local.txt')

# Access paths dynamically using keys
master_path = file_paths.get('MASTER', 'default_path_1.csv')  # added a default in case no key is there
list_path = file_paths.get('LIST', 'default_path_2.csv')
res_path = file_paths.get('RES', 'default_path_3')

#overwrites the previous Careismatic_Invoices_List.csv if it exists and reset it to the master file. this keeps from appending values if you rerun the same invoices by accident.
shutil.copy(master_path, list_path)

#this is the path that all NEW Careismatic Invoices are saved to from Outlook using VBA "SaveAttachmentsToDisk" Macro (res folder)
myPath = res_path

#this creates a new list of all the pdf's that are in the res folder.
# *this will check for ALL Invoices left in 'res', so be sure everything you don't want is out of that folder (i.e. last month's invoices).*
allFiles = [p for p in listdir(myPath) if isfile(join(myPath, p))]

#var for sum
grand_total = 0

#begin loop, runs once for each invoice in /res folder. everything that is inside this indented paragraph below is one cycle of the "loop".
for file in allFiles:

    #gets the name of the current file
    docName = os.path.splitext(file)[0]
    credit = False

    #if the doc is a credit memo, the parsing will be slightly different
    if 'CM_' in docName:
        #use old algo
        credit = True

    #crates a readable PDF "object" using the filename
    pdf = pdfquery.PDFQuery(myPath + '/' + docName + '.pdf')

    #opens the pdf for reading
    pdf.load()

    #convert and write the pdf to XML ***DO NOT DELETE, USED TO GET COORDS FOR NEW PDFs***
    #pdf.tree.write('XML/' + docName + '.xml', pretty_print = True)

    #find and set each variable we want from the PDF using their specific XML coordinates.

    #I have to have an if statement as I have two different bounding setups for invoices and credits.
    if credit:
        #Coords for old invoice format
        print(f"CREDIT DETECTED")

        # Old coords for credit memos
        inv_num     = pdf.pq('LTTextLineHorizontal:in_bbox("331.32, 67.47, 364.68, 77.47")').text().strip()
        inv_date    = pdf.pq('LTTextLineHorizontal:in_bbox("434.98, 67.47, 485.02, 77.47")').text().strip()
        num_items   = pdf.pq('LTTextLineHorizontal:in_bbox("163.5, 155.017, 168.504, 164.017")').text().strip()
        po          = pdf.pq('LTTextLineHorizontal:in_bbox("212.1, 67.47, 259.9, 77.47")').text().strip()
        num_boxes   = pdf.pq('LTTextLineHorizontal:in_bbox("104.72, 192.47, 110.28, 202.47")').text().strip()
        total_due   = pdf.pq('LTTextLineHorizontal:in_bbox("320.32, 39.47, 373.68, 49.47")').text().strip()

    else:    
        #Coords for new invoice format as of 9/6/2024                                                       
        inv_num     = pdf.pq('LTTextLineHorizontal:in_bbox("325.66, 71.37, 370.34, 81.57")').text()
        inv_date    = pdf.pq('LTTextLineHorizontal:in_bbox("434.88, 71.37, 485.12, 81.57")').text()
        num_items   = pdf.pq('LTTextLineHorizontal:in_bbox("150.99, 155.917, 174.602, 165.117")').text()
        po          = pdf.pq('LTTextLineHorizontal:in_bbox("35.18, 550.031, 103.819, 557.231")').text()
        num_boxes   = pdf.pq('LTTextLineHorizontal:in_bbox("94.0, 155.917, 107.604, 165.117")').text()
        total_due   = pdf.pq('LTTextLineHorizontal:in_bbox("523.86, 201.37, 574.1, 211.57")').text()

    #clean up the values for math by removing dollar signs, commas, 'CR's, etc.
    total_due = clean_total(total_due, credit)

    #Add every total together for a sum
    grand_total += total_due

    #prints each output for debug and visual purposes
    print(inv_num)
    print(inv_date)
    print(num_items)
    print(po)
    print(num_boxes)
    print(total_due)
    print('Total: ' , round(grand_total, 2))
    print('---------------------------------')

    #creates a DataFrame object -- the object is just an array of values that corresponds to each column name
    outDataFrame = pd.DataFrame({'INVOICE #': [inv_num],
                                'INVOICE DATE': [inv_date],
                                'ITEMS ON INV': [num_items],
                                'PO #': [po],
                                'BOXES ON PO': [num_boxes],
                                'TOTAL COST': [total_due]})

    #appends (the 'a' denotes 'append') the above DataFrame to a .CSV (comma separated value) file that we can open and view in Excel
    with open(list_path, 'a', newline='') as f:
        outDataFrame.to_csv(f, header=False, index=False)

#Write the final total as a bottom row
outDataFrame = pd.DataFrame([['', '', '', '', 'TOTAL:', round(grand_total, 2)]])
with open(list_path, 'a', newline='') as f:
        outDataFrame.to_csv(f, header=False, index=False)

#when you see this in your output window, the code is finished running
print('DONE!')
