# Import necessary modules from tkinter
import tkinter as tk
from tkinter import messagebox

# Initialize an empty task list
tasks = []

# Function to add a new task
def add_task():
    # Get text from the entry field and remove extra spaces
    new_task = add_task_entry.get().strip()
    
    # Append the new task to the file
    with open("ToDo_List.txt", "a") as file:
        file.write(f"{new_task}\n")

    # Clear the entry field
    add_task_entry.delete(0, tk.END)

    # Show a confirmation popup
    messagebox.showinfo("Success", "Task added!")

    # Update the dropdown menus
    refresh_dropdown()

# Function to mark a task as completed
def completed_task():
    # Read existing tasks from file
    with open("ToDo_List.txt", "r") as file:
        tasks = file.readlines()

    complete_item = completed_task_var.get()  # Get selected task
    updated_tasks = []

    # Loop through each task and update the one that matches the selected task
    for task in tasks:
        if task.strip() == complete_item and "done" not in task:
            # Add "done" tag to the task
            updated_tasks.append(task.strip() + " done\n")
        else:
            # Keep task as-is
            updated_tasks.append(task)

    # Write updated tasks back to file
    with open("ToDo_List.txt", "w") as file:
        for task in updated_tasks:
            file.write(task)

    # Reset dropdown selection and show confirmation
    completed_task_var.set("Choose a task")
    messagebox.showinfo("Success", "Task completed!")
    refresh_dropdown()

# Function to delete a selected task
def delete_task():
    # Read all tasks from file
    with open("ToDo_List.txt", "r") as file:
        tasks = file.readlines()

    item_to_delete = delete_task_var.get()  # Get selected task to delete

    # Keep all tasks except the one to delete
    updated_tasks = [task for task in tasks if task.strip() != item_to_delete]

    # Write updated list back to file
    with open("ToDo_List.txt", "w") as file:
        for task in updated_tasks:
            file.write(task)

    # Reset dropdown and show success message
    delete_task_var.set("Choose a task")
    messagebox.showinfo("Success", "Task deleted!")
    refresh_dropdown()

# Function to refresh the dropdown menus with the latest task list
def refresh_dropdown():
    try:
        # Read and clean up task list
        with open("ToDo_List.txt", "r") as file:
            updated = [task.strip() for task in file.readlines()]
    except FileNotFoundError:
        # Handle if file does not exist yet
        updated = []

    # Update Delete dropdown menu
    delete_menu = delete_task_dropdown["menu"]
    delete_menu.delete(0, "end")
    for task in updated:
        delete_menu.add_command(label=task, command=lambda value=task: delete_task_var.set(value))
    delete_task_var.set("Choose a task")

    # Update Completed dropdown menu
    complete_menu = completed_task_dropdown["menu"]
    complete_menu.delete(0, "end")
    for task in updated:
        complete_menu.add_command(label=task, command=lambda value=task: completed_task_var.set(value))
    completed_task_var.set("Choose a task")

# ------------------ GUI SETUP ------------------ #

# Create main window
root = tk.Tk()
root.title("ToDo List")  # Set window title

# Add Task Button
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.grid(row=0, column=2, padx=10)

# Delete Task Button
delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.grid(row=1, column=2, padx=10)

# Mark Task as Completed Button
complete_button = tk.Button(root, text="Mark Task as Completed", command=completed_task)
complete_button.grid(row=2, column=2, padx=10)

# Label and Entry for Adding a Task
tk.Label(root, text="Add Task:").grid(row=0, column=0, padx=10, pady=5)
add_task_entry = tk.Entry(root)
add_task_entry.grid(row=0, column=1, padx=10, pady=5)

# Variables to hold selected dropdown values
delete_task_var = tk.StringVar(root)
delete_task_var.set("Choose a task")

completed_task_var = tk.StringVar(root)
completed_task_var.set("Choose a task")

# Load tasks from file to populate dropdowns initially
try:
    with open("ToDo_List.txt", "r") as file:
        tasks = [task.strip() for task in file.readlines() if task.strip()]
except FileNotFoundError:
    tasks = []

# Create Delete Task Dropdown Menu
delete_task_dropdown = tk.OptionMenu(root, delete_task_var, "Choose a task", *tasks)
delete_task_dropdown.grid(row=1, column=1, padx=10, pady=5)

# Create Completed Task Dropdown Menu
completed_task_dropdown = tk.OptionMenu(root, completed_task_var, "Choose a task", *tasks)
completed_task_dropdown.grid(row=2, column=1, padx=10, pady=5)

# Labels for dropdowns
tk.Label(root, text="Delete Task:").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Mark Task as Completed:").grid(row=2, column=0, padx=10, pady=5)

# Start the GUI loop
root.mainloop()
