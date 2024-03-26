# graphics.py
from tkinter import Tk, ttk, Frame, Button, Text, Scrollbar, filedialog, messagebox, simpledialog
from file_search import Search
from compare import Compare
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
        self.plugins = {}

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

        # Create a compare button
        compare_button = Button(button_frame, text="Compare Profiles", command=self.compare_profiles)
        compare_button.pack(side="left", padx=5)

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
        if user_os == "Darwin":
            user_os = "MacOS"
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
        # Combine the plugin formats into a single dictionary
        combined_plugins = {}
        for plugin, formats in self.search.plugins.items():
            if plugin not in combined_plugins:
                combined_plugins[plugin] = formats
            else:
                combined_plugins[plugin].extend(formats)
                combined_plugins[plugin] = list(set(combined_plugins[plugin]))

        # Create the profile content
        profile_content = ""
        for plugin, formats in combined_plugins.items():
            profile_content += f"{plugin}: {', '.join(formats)}\n"

        # Ask the user for their name
        user_name = simpledialog.askstring("User Name", "Please enter your name:")

        if self.search.os == "Darwin":
            self.search.os = "MacOS"

        if user_name:
            # Format the user profile
            formatted_profile = f"{user_name}'s Plugin Profile\n\n"
            formatted_profile += f"{self.search.os}\n\n"
            formatted_profile += "Plugins:\n"
            formatted_profile += profile_content

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

    def compare_profiles(self):
        user1_profile_path = filedialog.askopenfilename(title="Select User 1 Profile", initialdir="profiles/user1", filetypes=[("Text Files", "*.txt")])
        user2_profile_path = filedialog.askopenfilename(title="Select User 2 Profile", initialdir="profiles/user2", filetypes=[("Text Files", "*.txt")])

        if user1_profile_path and user2_profile_path:
            user1_profile = self.load_profile(user1_profile_path)
            user2_profile = self.load_profile(user2_profile_path)

            if user1_profile and user2_profile:
                user1_name = user1_profile.split("\n")[0].split("'s Plugin Profile")[0]
                user2_name = user2_profile.split("\n")[0].split("'s Plugin Profile")[0]

                user1_plugins = self.extract_plugins(user1_profile)
                user2_plugins = self.extract_plugins(user2_profile)

                compare = Compare(user1_plugins, user2_plugins)
                common_report_path = f"profiles/common_report/{user1_name}_{user2_name}_common_report.txt"
                compare.output_common_plugins(common_report_path, user1_name, user2_name)

                messagebox.showinfo("Compare Profiles", "Profile comparison completed. Common report generated.")
            else:
                messagebox.showerror("Compare Profiles", "Failed to load user profiles.")
        else:
            messagebox.showinfo("Compare Profiles", "No profiles selected for comparison.")

    def load_profile(self, profile_path):
        try:
            with open(profile_path, "r") as file:
                profile_content = file.read()
            return profile_content
        except IOError:
            return None

    def extract_plugins(self, profile_content):
        plugins = {}
        lines = profile_content.split("\n")
        for line in lines:
            if ":" in line:
                plugin, formats = line.split(":", 1)
                plugins[plugin.strip()] = [format.strip() for format in formats.split(",")]
        return plugins
