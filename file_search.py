# file_search.py
import os
import platform

class Search():
    def __init__(self, window):
        self.window = window
        self.os = self.detect_os()
        self.search_paths = self.set_search_paths()
        self.stop_flag = False
        self.plugins = {}

    def detect_os(self):
        return platform.system() # Users OS
    
    def set_search_paths(self):
        if self.os == "Darwin":                                         # macOS
            return [
                "/Library/Audio/Plug-Ins/Components",                   # AU
                "/Library/Audio/Plug-Ins/VST",                          # VST
                "/Library/Audio/Plug-Ins/VST3",                         # VST3
                "/Library/Application Support/Avid/Audio/Plug-Ins"      # AAX
            ]
        elif self.os == "windows":
            return [
                "C:\\Program Files\\VSTPlugins",                        # VST
                "C:\\Program Files\\Common Files\\VST3",                # VST3
                "C:\\Program Files\\Common Files\\Avid\\Audio\\Plug-Ins"# AAX
            ]
        else:
            raise OSError("Unsupported operating system")
        
    def search_folder(self, folder_path, total_files, processed_files):
        searched_dirs = set()
        
        # Search directories
        for search_path in self.search_paths:
            full_path = os.path.join(folder_path, os.path.basename(search_path))

            # If the path exists recursively search
            if os.path.exists(full_path) and full_path not in searched_dirs:
                self.search_folder_r(self.plugins, full_path, total_files, processed_files)
                searched_dirs.add(full_path)

        # Try path if it hasn't been searched
        if folder_path not in searched_dirs:
            try:
                self.search_folder_r(self.plugins, folder_path, total_files, processed_files)
            except FileNotFoundError:
                pass
        return self.plugins

    def search_folder_r(self, plugins, current_path, total_files, processed_files):
        try:
            # Recursively search for plugins in the current directory and its subdirectories
            for item in os.listdir(current_path):
                # Check if the search has been stopped
                if self.stop_flag:
                    break

                # Get the full path of the current item
                item_path = os.path.join(current_path, item)

                # Get the file extension of the current item
                _, file_extension = os.path.splitext(item)

                # Check if the file extension matches the supported plugin formats
                if file_extension.lower() in [".component", ".vst", ".vst3", ".aaxplugin"]:
                    # Extract the plugin name from the file name
                    plugin_name = os.path.splitext(item)[0]

                    # Determine the plugin format based on the file extension
                    plugin_format = ""
                    if file_extension.lower() == ".component":
                        plugin_format = "AU"
                    elif file_extension.lower() == ".vst":
                        plugin_format = "VST"
                    elif file_extension.lower() == ".vst3":
                        plugin_format = "VST3"
                    elif file_extension.lower() == ".aaxplugin":
                        plugin_format = "AAX"

                    # Add the plugin to the plugins dictionary
                    if plugin_name not in plugins:
                        plugins[plugin_name] = [plugin_format]
                    else:
                        plugins[plugin_name].append(plugin_format)

                    # Display the found plugin in the command window (if a window is provided)
                    if self.window is not None:
                        self.window.command_window.configure(state="normal")
                        self.window.command_window.insert("end", f"{plugin_name}: {plugin_format}\n")
                        self.window.command_window.configure(state="disabled")
                        self.window.command_window.see("end")

                    # Print the found plugin to the console
                    print(f"Found: {plugin_name} ({plugin_format})")

                    # Add the processed file path to the list of processed files
                    processed_files.append(item_path)

                    # Update the progress bar
                    progress = len(processed_files) / total_files * 100
                    self.window.progress_bar["value"] = progress
                    self.window.update_idletasks()  # Update the GUI

                # If the current item is a directory, recursively search it
                elif os.path.isdir(item_path):
                    # Print the directory being entered to the console
                    print(f"Entering directory: {item_path}")

                    # Recursively call the search_folder_r function for the subdirectory
                    self.search_folder_r(plugins, item_path, total_files, processed_files)

        except PermissionError:
            # Skip directories or files that raise a PermissionError
            pass