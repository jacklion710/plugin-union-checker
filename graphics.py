# graphics.py
from tkinter import Tk, ttk, Frame, Button, Text, Scrollbar, filedialog, messagebox, simpledialog
from file_search import Search
import threading
from tkinter import Tk
import os

class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title("Plugin Profile")
        self.geometry("600x400")
        self.search = Search(self)
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for buttons
        button_frame = Frame(self)
        button_frame.pack(pady=10)

        # Create a search button
        self.search_button = Button(button_frame, text="Search Plugins", command=self.search_plugins)
        self.search_button.pack(side="left", padx=5)

        # Create a stop button
        self.stop_button = Button(button_frame, text="Stop Search", command=self.stop_search, state="disabled")
        self.stop_button.pack(side="left", padx=5)

        # Create a save button
        save_button = Button(button_frame, text="Save Profile", command=self.save_profile)
        save_button.pack(side="left", padx=5)

        # Create a command window
        self.command_window = Text(self, wrap="word", state="disabled")
        self.command_window.pack(fill="both", expand=True, padx=10, pady=10)

        # Create a scrollbar for the command window
        scrollbar = Scrollbar(self.command_window)
        scrollbar.pack(side="right", fill="y")
        self.command_window.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.command_window.yview)

    def search_plugins(self):
        # Get the user's OS
        user_os = self.search.detect_os()

        # Clear the command window
        self.command_window.configure(state="normal")
        self.command_window.delete("1.0", "end")

        # Display the user's OS
        self.command_window.insert("end", f"Operating System: {user_os}\n\n")
        self.command_window.insert("end", "Searching for plugins...\n")
        self.command_window.configure(state="disabled")
        self.command_window.see("end")

        # Create a progress bar
        self.progress_bar = ttk.Progressbar(self, mode="indeterminate")
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.start()

        # Disable the search button and enable the stop button
        self.search_button.config(state="disabled")
        self.stop_button.config(state="normal")

        # Perform the plugin search in a separate thread
        search_thread = threading.Thread(target=self.perform_search)
        search_thread.start()

    def perform_search(self):
        # Perform the plugin search
        plugins = {}
        total_files = sum(len(files) for search_path in self.search.search_paths for _, _, files in os.walk(search_path))
        processed_files = []

        for search_path in self.search.search_paths:
            if os.path.exists(search_path):
                self.command_window.configure(state="normal")
                self.command_window.insert("end", f"Searching directory: {search_path}\n")
                self.command_window.configure(state="disabled")
                self.command_window.see("end")
                found_plugins = self.search.search_folder(search_path, total_files, processed_files)
                plugins.update(found_plugins)
                # Display the found plugins in the command window
                if found_plugins:
                    self.command_window.configure(state="normal")
                    self.command_window.insert("end", "Found plugins:\n")
                    for plugin, formats in found_plugins.items():
                        self.command_window.insert("end", f"{plugin}: {', '.join(formats)}\n")
                    self.command_window.configure(state="disabled")
                    self.command_window.see("end")
                else:
                    self.command_window.configure(state="normal")
                    self.command_window.insert("end", "No plugins found in this directory.\n")
                    self.command_window.configure(state="disabled")
                    self.command_window.see("end")
            else:
                print(f"Search path not found: {search_path}")

        # Print the plugin profile to the console
        print("\nPlugin Profile:")
        for plugin, formats in plugins.items():
            print(f"{plugin}: {', '.join(formats)}")

        # Stop the progress bar
        self.progress_bar.stop()
        self.progress_bar.destroy()

        # Enable the search button and disable the stop button
        self.search_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def stop_search(self):
        self.search.stop_flag = True
        self.stop_button.config(state="disabled")
        
    def save_profile(self):
        # Get the plugin profile from the search results
        profile = ""
        for plugin, formats in self.search.plugins.items():
            profile += f"{plugin}: {', '.join(formats)}\n"

        # Ask the user for their name
        user_name = simpledialog.askstring("User Name", "Please enter your name:")

        if user_name:
            # Format the user profile
            formatted_profile = f"User's Name: {user_name}\n"
            formatted_profile += f"User's OS: {self.search.os}\n\n"
            formatted_profile += "Plugins:\n"
            formatted_profile += profile

            # Ask the user for a file path to save the profile
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

            if file_path:
                try:
                    # Save the formatted profile to the selected file path
                    with open(file_path, "w") as file:
                        file.write(formatted_profile)
                    messagebox.showinfo("Save Profile", "Plugin profile saved successfully.")
                except IOError:
                    messagebox.showerror("Save Profile", "An error occurred while saving the profile.")
