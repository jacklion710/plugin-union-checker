# graphics.py
from tkinter import Tk, Frame, Button, Text, Scrollbar, filedialog, messagebox
from file_search import Search

from tkinter import Tk

class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title("Plugin Profile")
        self.geometry("600x400")
        self.search = Search()
        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        button_frame = Frame(self)
        button_frame.pack(pady=10)

        # Create a search button
        search_button = Button(button_frame, text="Search Plugins", command=self.search_plugins)
        search_button.pack(side="left", padx=5)

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
        # Get users OS and search folders
        user_os = self.search.detect_os()
        plugins = self.search.search_folder("/")

        # Clear command window
        self.command_window.configure(state="normal")
        self.command_window.delete("1.0", "end")

        # Display users OS
        self.command_window.insert("end", f"Operating System: {user_os}\n\n")

        # Display the plugin profile
        self.command_window.insert("end", "Plugin Profile:\n")
        for plugin, formats in plugins.items():
            self.command_window.insert("end", f"{plugin}: {', '.join(formats)}\n")
        self.command_window.configure(state="disabled")

    def save_profile(self):
        # Get the plugin profile form the command window
        profile = self.command_window.get("1.0", "end-1c")

        # Ask user for a file path to save to
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

        if file_path:
            try:
                # Save the profile to the selected path
                with open(file_path, "w") as file:
                    file.write(profile)
                messagebox.showinfo("Save Profile", "Plugin profile saved successfully.")
            except IOError:
                messagebox.showerror("Save Profile", "An error occured while saving the profile.")