# tests.py
import unittest
from unittest.mock import Mock
from file_search import Search
from compare import Compare
from graphics import Window
import os
import shutil
import tempfile

class SearchTests(unittest.TestCase):
    def setUp(self):
        self.test_folder = "test_plugins"
        os.makedirs(self.test_folder, exist_ok=True)
        self.create_test_files()
        mock_window = Mock()
        mock_window.command_window = Mock()
        mock_window.progress_bar = Mock()
        mock_window.progress_bar.__getitem__ = Mock(return_value=None)
        mock_window.progress_bar.__setitem__ = Mock()
        self.search = Search(mock_window)

    def tearDown(self):
        shutil.rmtree(self.test_folder)

    def create_test_files(self):
        plugin_files = [
            "plugin1.component",
            "plugin1.vst",
            "plugin2.vst3",
            "plugin3.aaxplugin",
            "not_a_plugin.txt",
        ]
        for file in plugin_files:
            file_path = os.path.join(self.test_folder, file)
            with open(file_path, "w") as f:
                f.write("Test plugin file")

    def test_detect_os(self):
        detected_os = self.search.detect_os()
        self.assertIn(detected_os, ["Darwin", "Windows", "Linux"])

    def test_search_folder(self):
        selected_formats = ["VST", "VST3"]
        plugins = self.search.search_folder(self.test_folder, len(os.listdir(self.test_folder)), [], selected_formats)
        expected_plugins = {
            "plugin1": ["VST"],
            "plugin2": ["VST3"]
        }
        self.assertEqual(self.sort_plugins(plugins), self.sort_plugins(expected_plugins))

    def test_search_folder_nonexistent(self):
        selected_formats = ["AU", "VST", "VST3", "AAX"]
        plugins = self.search.search_folder("nonexistent_folder", 0, [], selected_formats)
        self.assertEqual(plugins, {})

    def test_set_search_paths(self):
        search_paths = self.search.set_search_paths()
        if self.search.os == "Darwin":
            expected_paths = [
                "/Library/Audio/Plug-Ins/Components",
                "/Library/Audio/Plug-Ins/VST",
                "/Library/Audio/Plug-Ins/VST3",
                "/Library/Application Support/Avid/Audio/Plug-Ins"
            ]
        elif self.search.os == "Windows":
            expected_paths = [
                "C:\\Program Files\\VSTPlugins",
                "C:\\Program Files\\Common Files\\VST3",
                "C:\\Program Files\\Common Files\\Avid\\Audio\\Plug-Ins"
            ]
        else:
            expected_paths = []
        self.assertEqual(search_paths, expected_paths)

    def test_search_folder_r(self):
        plugins = {}
        processed_files = []
        selected_formats = ["VST", "VST3"]
        self.search.search_folder_r(plugins, self.test_folder, len(os.listdir(self.test_folder)), processed_files, selected_formats)
        expected_plugins = {
            "plugin1": ["VST"],
            "plugin2": ["VST3"]
        }
        self.assertEqual(self.sort_plugins(plugins), self.sort_plugins(expected_plugins))
    
    def sort_plugins(self, plugins):
        return {plugin: sorted(formats) for plugin, formats in plugins.items()}

class CompareTests(unittest.TestCase):
    def setUp(self):
        self.profile1 = {
            "plugin1": ["VST", "AU"],
            "plugin2": ["VST3"],
            "plugin3": ["AAX"]
        }
        self.profile2 = {
            "plugin1": ["VST"],
            "plugin2": ["VST3", "AU"],
            "plugin4": ["AAX"]
        }

    def test_compare_profiles(self):
        compare = Compare(self.profile1, self.profile2)
        common_plugins, not_shared_plugins = compare.compare_profiles()
        expected_common_plugins = {
            "plugin1": ["VST"],
            "plugin2": ["VST3"]
        }
        expected_not_shared_plugins = {
            "plugin1": ["AU"],
            "plugin3": ["AAX"],
            "plugin4": ["AAX"]
        }
        self.assertEqual(common_plugins, expected_common_plugins)
        self.assertEqual(not_shared_plugins, expected_not_shared_plugins)

    def test_output_common_plugins(self):
        compare = Compare(self.profile1, self.profile2)
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            compare.output_common_plugins(temp_file.name, "User1", "User2")
            with open(temp_file.name, "r") as file:
                content = file.read()
                self.assertIn("User1 and User2 common plugins profile", content)
                self.assertIn("Plugins shared:", content)
                self.assertIn("plugin1: VST", content)
                self.assertIn("plugin2: VST3", content)
                self.assertIn("Plugins not shared:", content)
                self.assertIn("plugin1: AU", content)
                self.assertIn("plugin3: AAX", content)
                self.assertIn("plugin4: AAX", content)
        os.unlink(temp_file.name)

class WindowTests(unittest.TestCase):
    def setUp(self):
        self.window = Window()

    def test_create_widgets(self):
        self.assertIsNotNone(self.window.search_button)
        self.assertIsNotNone(self.window.stop_button)
        self.assertIsNotNone(self.window.command_window)

    def test_stop_search(self):
        self.window.stop_search()
        self.assertTrue(self.window.search.stop_flag)
        self.assertEqual(self.window.stop_button.cget("state"), "disabled")

if __name__ == "__main__":
    unittest.main()
