import tkinter as tk
from tkinter import messagebox

# Function to calculate the percentage
def calculate_percentage(event=None):
    try:
        # Get the dollar amount and percentage from user input
        amount = float(entry_amount.get())
        percentage = float(3)
        
        # Calculate the percentage
        result = (percentage / 100) * amount
        result_label.config(text=f"{percentage}% of ${amount} is: ${result:.2f}")
    
    except ValueError:
        # Display an error message if input is invalid
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Create the main window
root = tk.Tk()
root.title("Percentage Calculator")

# Set the window size (about the size of a credit card)
root.geometry("300x250")

# Set the window to be at the bottom-right corner
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 300
window_height = 250
x_position = screen_width - window_width
y_position = screen_height - window_height
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create and place widgets
label_amount = tk.Label(root, text="Total:", font=("Arial", 12))
label_amount.pack(pady=5)

entry_amount = tk.Entry(root, font=("Arial", 14))
entry_amount.pack(pady=5)

calculate_button = tk.Button(root, text="Calculate", font=("Arial", 14), command=calculate_percentage)
calculate_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14), wraplength=280)
result_label.pack(pady=5)

# also allow for enter key to run the percentage
root.bind("<Return>", calculate_percentage)

# Start the Tkinter event loop
root.mainloop()