# tests.py
import unittest
from file_search import Search
import os
import shutil

class SearchTests(unittest.TestCase):
    def setUp(self):
        self.test_folder = "test_plugins"
        os.makedirs(self.test_folder, exist_ok=True)
        self.create_test_files()
        self.search = Search()

    def tearDown(self):
        shutil.rmtree(self.test_folder)

    def create_test_files(self):
        plugin_files = [
            "plugin1.au",
            "plugin1.vst",
            "plugin2.vst3",
            "plugin3.aax",
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
        plugins = self.search.search_folder(self.test_folder)
        expected_plugins = {
            "plugin1": ["au", "vst"],
            "plugin2": ["vst3"],
            "plugin3": ["aax"],
        }
        self.assertEqual(plugins, expected_plugins)

    def test_search_folder_nonexistent(self):
        plugins = self.search.search_folder("nonexistent_folder")
        self.assertEqual(plugins, {})

if __name__ == "__main__":
    unittest.main()