# file_search.py
import os
import platform

class Search():
    def __init__(self):
        self.os = self.detect_os()
        self.search_paths = self.set_search_paths()

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
        
    def search_folder(self, folder_path):
        plugins = {}
        searched_dirs = set()
        for search_path in self.search_paths:
            full_path = os.path.join(folder_path, os.path.basename(search_path))
            if os.path.exists(full_path) and full_path not in searched_dirs:
                self.search_folder_r(plugins, full_path)
                searched_dirs.add(full_path)
        if folder_path not in searched_dirs:
            try:
                self.search_folder_r(plugins, folder_path)
            except FileNotFoundError:
                pass
        return plugins

    def search_folder_r(self, plugins, current_path):
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            if os.path.isfile(item_path):
                if item.endswith((".au", ".vst", ".vst3", ".aax")):
                    plugin_name = os.path.splitext(item)[0]
                    plugin_format = os.path.splitext(item)[1][1:]
                    if plugin_name not in plugins:
                        plugins[plugin_name] = [plugin_format]
                    else:
                        plugins[plugin_name].append(plugin_format)
            elif os.path.isdir(item_path):
                self.search_folder_r(plugins, item_path)