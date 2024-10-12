import tkinter as tk
from tkinter import messagebox

def calculator(operation, num1, num2):
    try:
        num1 = float(num1)
        num2 = float(num2)
    except ValueError:
        return "Error: Invalid number"

    if operation == 'add':
        return num1 + num2
    elif operation == 'subtract':
        return num1 - num2
    elif operation == 'multiply':
        return num1 * num2
    elif operation == 'divide':
        if num2 != 0:
            return num1 / num2
        else:
            return "Error: Division by zero"
    else:
        return "Error: Invalid operation"

def perform_calculation():
    operation = operation_var.get()
    num1 = entry_num1.get()
    num2 = entry_num2.get()
    result = calculator(operation, num1, num2)
    messagebox.showinfo("Result", f"Result: {result}")

# Create the main window
root = tk.Tk()
root.title("Simple Calculator")

# Create and place the widgets
tk.Label(root, text="Number 1:").grid(row=0, column=0)
entry_num1 = tk.Entry(root)
entry_num1.grid(row=0, column=1)

tk.Label(root, text="Number 2:").grid(row=1, column=0)
entry_num2 = tk.Entry(root)
entry_num2.grid(row=1, column=1)

tk.Label(root, text="Operation:").grid(row=2, column=0)
operation_var = tk.StringVar(root)
operation_var.set("add")
tk.OptionMenu(root, operation_var, "add", "subtract", "multiply", "divide").grid(row=2, column=1)

tk.Button(root, text="Calculate", command=perform_calculation).grid(row=3, columnspan=2)

# Run the application
root.mainloop()