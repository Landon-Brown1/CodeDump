import os
import glob
import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

'''
REMOVED USER INPUT
# Custom exception for user exit without selecting a file
class FileNotSelectedError(Exception):
    pass
'''
# Function to clean up and reformat the data in the .iif file
def clean_and_save_daysheet(iif_file_path):
    try:
        # Open the .iif file and read all lines as CSV
        with open(iif_file_path, 'r') as file:
            reader = csv.reader(file)
            lines = list(reader)

        # Find the rows we want to delete
        rows_to_delete = []
        for i, line in enumerate(lines):
            # Check if the line starts with A/R
            if len(line) > 3 and (
                line[0] == "ACCNT" and 
                (line[1] == "Accounts Receivable" and line[2] == "AR") or 
                (line[1] == "Accounts Receivable:USolution" and line[2] == "AR")
            ):
                if i < 15:  # I have never seen it go far from line 7 or 8
                    rows_to_delete.append(i)

        '''
        REMOVED USER INPUT
        # Show a preview of the lines to be deleted
        print("Lines to be deleted:")
        for row in rows_to_delete:
            print(lines[row])  # Print the content of the row

        # Ask user for confirmation to delete these rows
        confirmation = input(f"Do you want to delete these {len(rows_to_delete)} lines? (yes/no): ")
        if confirmation.lower() != "yes":
            print("No changes were made.")
            return
        '''
        
        # Remove the identified rows
        cleaned_lines = [line for i, line in enumerate(lines) if i not in rows_to_delete]

        # Save the cleaned data back as a tab-separated (still .iif!) file
        with open(iif_file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(cleaned_lines)

        print(f"File saved successfully to {iif_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
'''
REMOVED USER INPUT
# Function to open a file dialog and get the .iif file path
def get_file_path():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select .iif File",
        filetypes=(("IIF Files", "*.iif"), ("All Files", "*.*"))
    )
    
    if not file_path:
        raise FileNotSelectedError("No file selected. Exiting.")
    return file_path
    
# Function to select a save path for the cleaned .iif file
def get_save_path():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    save_path = filedialog.asksaveasfilename(
        title="Save Cleaned File As",
        defaultextension=".iif",
        filetypes=(("IIF Files", "*.iif"), ("All Files", "*.*"))
    )
    
    if not save_path:
        raise FileNotSelectedError("No save location selected. Exiting.")
    return save_path
    '''
# Function to get the most recent .iif file from the QBiif folder
def get_most_recent_file(folder_path):
    files = glob.glob(os.path.join(folder_path, "*.iif"))
    
    if not files:
        raise FileNotFoundError("No .iif files found in the specified folder.")

    # comparing the last modified time
    most_recent_file = max(files, key=os.path.getmtime)
    return most_recent_file

# Function to show a start confirmation dialog
def show_start_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    response = messagebox.askokcancel("LB's Quickbooks Export Integrate-O-Matic 3000 v1.3", "You are about to format the most recently saved .iif file in C:>Users>Missy>Documents>Quickbooks IIFs. Do you want to continue?")
    return response

# Main script
if __name__ == "__main__":
    try:
        # Show start confirmation dialog
        if not show_start_dialog():
            print("Program exited by user.")
            exit()

        '''
        REMOVED USER INPUT
        # Ask user to select the .iif file
        iif_file_path = get_file_path()
        if not iif_file_path:  # If no file was selected
            print("No file selected. Exiting.")
            exit()

        # Ask user where to save the cleaned .iif file
        cleaned_file_path = get_save_path()
        if not cleaned_file_path:  # If no save location was chosen
            print("No save location selected. Exiting.")
            exit()
        '''
        # Define the folder path (can adjust this as needed)
        folder_path = r'C:\Users\Missy\Documents\Quickbooks IIFs'

        # Automatically get the most recent .iif file from the folder
        iif_file_path = get_most_recent_file(folder_path)
        print(f"Using file: {iif_file_path}")

        # Run the function to clean and save the modified .iif file
        clean_and_save_daysheet(iif_file_path)

    except FileNotFoundError as e:
        print(e)
        exit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit()