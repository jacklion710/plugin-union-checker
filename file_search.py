# file_search.py
import os
import platform

class Search():
    def __init__(self, window):
        self.window = window
        self.os = self.detect_os()
        self.search_paths = self.set_search_paths()
        self.stop_flag = False

    def detect_os(self):
        return platform.system()
    
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
        plugins = {}
        searched_dirs = set()
        for search_path in self.search_paths:
            full_path = os.path.join(folder_path, os.path.basename(search_path))
            if os.path.exists(full_path) and full_path not in searched_dirs:
                self.search_folder_r(plugins, full_path, total_files, processed_files)
                searched_dirs.add(full_path)
        if folder_path not in searched_dirs:
            try:
                self.search_folder_r(plugins, folder_path, total_files, processed_files)
            except FileNotFoundError:
                pass
        return plugins

    def search_folder_r(self, plugins, current_path, total_files, processed_files):
        try:
            for item in os.listdir(current_path):
                if self.stop_flag:
                    break
                item_path = os.path.join(current_path, item)
                if os.path.isfile(item_path):
                    _, file_extension = os.path.splitext(item)
                    if file_extension.lower() in [".component", ".vst", ".vst3", ".aaxplugin"]:
                        plugin_name = os.path.splitext(item)[0]
                        plugin_format = file_extension[1:].upper()
                        if plugin_name not in plugins:
                            plugins[plugin_name] = [plugin_format]
                        else:
                            plugins[plugin_name].append(plugin_format)
                        # Print the found plugin to the console
                        print(f"Found: {plugin_name} ({plugin_format})")
                    processed_files.append(item_path)
                    progress = len(processed_files) / total_files * 100
                    self.window.progress_bar["value"] = progress
                    self.window.update_idletasks()  # Update the GUI
                elif os.path.isdir(item_path):
                    # Print the directory being entered to the console
                    print(f"Entering directory: {item_path}")
                    self.search_folder_r(plugins, item_path, total_files, processed_files)
        except PermissionError:
            pass
