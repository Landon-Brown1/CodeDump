import os
import glob
import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

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
        
        # Remove the identified rows
        cleaned_lines = [line for i, line in enumerate(lines) if i not in rows_to_delete]

        # Save the cleaned data back as a tab-separated (still .iif!) file
        with open(iif_file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(cleaned_lines)

        print(f"File saved successfully to {iif_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

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
