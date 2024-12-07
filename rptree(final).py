import os
from termcolor import colored
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

def format_size(size):
    """Convert file size to a readable format (e.g., KB, MB)."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def generate_tree(directory_path, prefix="", depth=None, current_level=0, file_filter=None, exclude_hidden=True, search_query=None, progress=None):
    if not os.path.isdir(directory_path):
        print("Error: The specified path is not a valid directory.")
        return
    
    if depth is not None and current_level >= depth:
        return

    try:
        entries = sorted(os.listdir(directory_path), key=lambda x: (os.path.isfile(os.path.join(directory_path, x)), x.lower()))
    except OSError as e:
        print(f"Error reading directory contents: {e}")
        return

    for i, entry in enumerate(entries):
        is_last = (i == len(entries) - 1)
        entry_path = os.path.join(directory_path, entry)
        
        if exclude_hidden and entry.startswith('.'):
            continue
        if file_filter and not entry.endswith(file_filter):
            continue

        connector = "└── " if is_last else "├── "
        
        display_entry = entry

        # Highlight search matches, directories, and specific files with color
        if search_query and search_query.lower() in entry.lower():
            display_entry = colored(entry, 'red')
        elif os.path.isdir(entry_path):
            display_entry = colored(entry, 'blue')
        elif entry.endswith('.py'):
            display_entry = colored(entry, 'yellow')
        
        # Show file size if it's a file
        if os.path.isfile(entry_path):
            file_size = format_size(os.path.getsize(entry_path))
            display_entry += f" ({file_size})"
        
        print(prefix + connector + display_entry)
        
        if os.path.isdir(entry_path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            generate_tree(entry_path, new_prefix, depth, current_level + 1, file_filter, exclude_hidden, search_query, progress)

        # Update the progress bar if provided
        if progress:
            progress.update(1)

def select_directory():
    """Open a file dialog to select a directory."""
    directory = filedialog.askdirectory(title="Select Directory")
    return directory

def display_tree():
    """Get inputs and display the directory tree with GUI options."""
    directory = select_directory()
    if not directory:
        return
    
    # Get depth from the user
    depth = simpledialog.askinteger("Depth", "Enter maximum depth (leave blank for full depth):", minvalue=0) or None
    
    # Get file filter and search query
    file_filter = simpledialog.askstring("File Filter", "Enter file type to display only (e.g., .txt, leave blank to include all):")
    search_query = simpledialog.askstring("Search", "Enter search query to highlight matching entries (optional):")

    # Count total files and directories for the progress bar
    total_files = sum(len(files) + len(dirs) for _, dirs, files in os.walk(directory))

    # Initialize the progress bar
    with tqdm(total=total_files, desc="Generating Tree", unit="entry") as progress:
        # Generate and display the tree structure
        print("\nDirectory Tree Structure:\n")
        generate_tree(directory, depth=depth, file_filter=file_filter, search_query=search_query, progress=progress)

# GUI setup
root = tk.Tk()
root.withdraw()  # Hide main window

# Run the GUI interface for tree generation
display_tree()