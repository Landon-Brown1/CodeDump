# ██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███╗   ██╗    ██████╗ ██████╗ ███████╗    ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
# ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║    ██╔══██╗██╔══██╗██╔════╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
# ██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║██╔██╗ ██║    ██████╔╝██║  ██║█████╗      ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
# ██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║██║╚██╗██║    ██╔═══╝ ██║  ██║██╔══╝      ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
# ██║        ██║      ██║   ██║  ██║╚██████╔╝██║ ╚████║    ██║     ██████╔╝██║         ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
# ╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ╚═╝     ╚═════╝ ╚═╝         ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
# / Created: 05-2024 / Last Updated: 12-2024 / Author: L. Brown                                                                                                                                           
# 
# DISCLAIMER: This is the first time I have written in Python, and I am by no means fluent. Bear with me. :)
#
#   !!!THIS PROGRAM IS CURRENTLY HARDCODED FOR CAREISMATIC INC INVOICES. IT WILL -NOT- WORK FOR OTHER PDFs UNLESS COORDINATES on lines 54-59 ARE MODIFIED ACCORDINGLY!!!
#   Update coordinates by uncommenting the code at line 46, and commenting out lines 52-78. This will make the program instead create an XML file from all PDFs it reads. 
#   Use the XML file to find the coordinates of the data you want, then use the code on line 50 to create a new dataframe.
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

#overwrites the previous Careismatic_Invoices_List.csv if it exists and reset it to the master file. this keeps from appending values if you rerun the same invoices by accident.
shutil.copy('C:/Users/Missy/Documents/PDFs/Careismatic_Invoices/Master.csv', 'C:/Users/Missy/Documents/PDFs/Careismatic_Invoices/Careismatic_Invoices_List.csv')

#this is the path that all NEW Careismatic Invoices are saved to from Outlook using VBA "SaveAttachmentsToDisk" Macro (res folder)
myPath = 'C:/Users/Missy/Documents/PDFs/Careismatic_Invoices/res'

#this creates a new list of all the pdf's that are in the res folder.
# *this will check for ALL Invoices left in 'res', so be sure everything you don't want is out of that folder (i.e. last month's invoices).*
allFiles = [p for p in listdir(myPath) if isfile(join(myPath, p))]

#begin loop, runs once for each invoice in /res folder. everything that is inside this indented paragraph below is one cycle of the "loop".
for file in allFiles:

    #gets the name of the current file
    docName = os.path.splitext(file)[0]

    #crates a readable PDF "object" using the filename
    pdf = pdfquery.PDFQuery(myPath + '/' + docName + '.pdf')

    #opens the pdf for reading
    pdf.load()

    #convert and write the pdf to XML ***DO NOT DELETE, USED TO GET COORDS FOR NEW PDFs***
    #pdf.tree.write('resXML/' + docName + '.xml', pretty_print = True)

    #finds and sets each variable we want from the PDF using their specific XML coordinates
    #Coords for new invoice format as of 9/6/2024                                                       #Coords for old invoice format
    inv_num     = pdf.pq('LTTextLineHorizontal:in_bbox("325.66, 71.37, 370.34, 81.57")').text()         #inv_num     = pdf.pq('LTTextLineHorizontal:in_bbox("325.76, 115.47, 370.24, 125.47")').text()
    inv_date    = pdf.pq('LTTextLineHorizontal:in_bbox("434.88, 71.37, 485.12, 81.57")').text()         #inv_date    = pdf.pq('LTTextLineHorizontal:in_bbox("434.98, 115.47, 485.02, 125.47")').text()
    num_items   = pdf.pq('LTTextLineHorizontal:in_bbox("150.99, 155.917, 174.602, 165.117")').text()    #num_items   = pdf.pq('LTTextLineHorizontal:in_bbox("160.16, 192.47, 176.84, 202.47")').text()
    po          = pdf.pq('LTTextLineHorizontal:in_bbox("35.18, 550.031, 103.819, 557.231")').text()     #po          = pdf.pq('LTTextLineHorizontal:in_bbox("56.99, 549.017, 82.01, 558.017")').text()
    num_boxes   = pdf.pq('LTTextLineHorizontal:in_bbox("94.0, 155.917, 107.604, 165.117")').text()     #num_boxes   = pdf.pq('LTTextLineHorizontal:in_bbox("104.72, 192.47, 110.28, 202.47")').text()
    total_due   = pdf.pq('LTTextLineHorizontal:in_bbox("523.86, 201.37, 574.1, 211.57")').text()         #total_due   = pdf.pq('LTTextLineHorizontal:in_bbox("315.5, 87.47, 369.44, 97.47")').text()

    #prints each output for debug and visual purposes
    print(inv_num)
    print(inv_date)
    print(num_items)
    print(po)
    print(num_boxes)
    print(total_due)
    print('---------------------------------')

    #creates a DataFrame object -- the object is just an array of values that corresponds to each column name
    outDataFrame = pd.DataFrame({'INVOICE #': [inv_num],
                                'INVOICE DATE': [inv_date],
                                'ITEMS ON INV': [num_items],
                                'PO #': [po],
                                'BOXES ON PO': [num_boxes],
                                'TOTAL COST': [total_due]})

    #appends (the 'a' denotes 'append') the above DataFrame to a .CSV (comma separated value) file that we can open and view in Excel
    with open('C:/Users/Missy/Documents/PDFs/Careismatic_Invoices/Careismatic_Invoices_List.csv', 'a') as f:
        outDataFrame.to_csv(f, header=False)

#added the last run date of the spreadsheet to the end -->[BROKEN, the INVOICE and INVOICE DATE here would have to be a DataFrame object like inv_num or inv_date :(]
#DATEaFrame = pd.DataFrame({'INVOICE#': "Updated:", 
#                           'INVOICE DATE': date.today()})
#
#with open('C:/Users/Missy/Documents/PDFs/Careismatic_Invoices/Careismatic_Invoices_List.csv', 'a') as f:
#        DATEaFrame.to_csv(f, header=False)

#when you see this in your output window, the code is finished running
print('DONE!')
