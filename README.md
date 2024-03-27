# Plugin Union Checker

The Plugin Union Checker is a Python application that allows users to search for audio plugins on their system and generate a profile of the found plugins. Users can save their plugin profiles and compare them with others to find common plugins.

## Features

* Search for audio plugins on the user's system
* Generate a plugin profile with the found plugins and their formats
* Save the plugin profile to a file
* Compare two plugin profiles to find common plugins
* Generate a common plugin profile report

## Requirements

* Python 3.1 or greater
* Tkinter (Python's standard GUI library)

## Installation

1. Clone the repository or download the source code.

2. Ensure that you have Python 3.1 or higher installed on your system. You can download it from the official Python website: https://www.python.org

3. Install Tkinter:
    * For macOS, you can install Tkinter using Homebrew:

    ```bash
    brew install python-tk
    ```

    * For Windows, Tkinter should be included with the Python installation. If it's not available, you can install it using pip:

    ```py
    pip install tk
    ```

4. Install pyinstaller:

```bash
pip install pyinstaller
```

## Building the Application

### macOS

1. Open a terminal and navigate to the project directory.

2. Run the following command to create a standalone executable:

```bash
pyinstaller --onefile --windowed main.py
```

3. The executable `main.app` will be generated in the `dist` directory

4. You may need to create a virtual env using pip or conda to bundle the dependencies with pyinstaller properly. 

```bash
conda create --name myenv python=3.9
```

```bash
conda activate myenv
```

```bash
conda install pyinstaller
```

If the above steps don't work, you can try specifying the path to the Tcl/Tk libraries explicitly using the `--add-binary` option:

```bash
pyinstaller --onefile --windowed --add-binary="$(python -c 'import tkinter; print(tkinter.Tcl().eval("info library"))')":tcl --add-binary="$(python -c 'import tkinter; print(tkinter.Tk().eval("info library"))')":tk main.py
```

I recommend building on your own system but for convenience I have left an application bundle in `app/macos/main.app/Contents` 

### Windows

1. Open a command prompt and navigate to the project directory.

2. Run the following command to create a standalone executable:
bash

```bash
pyinstaller --onefile --windowed main.py
```

3. The executable will be generated in the dist directory.

Note: On Windows, you may need to add the Python installation directory to your system's PATH environment variable for PyInstaller to work properly.

4. You may need to create a virtual env using pip or conda to bundle the dependencies with pyinstaller properly. 

```bash
conda create --name myenv python=3.9
```

```bash
conda activate myenv
```

```bash
conda install pyinstaller
```

## Usage

1. Open a terminal or command prompt and navigate to the project directory.

2. Run the following command to start the application:

```bash
python main.py
```

3. The Plugin Union Checker GUI will appear. If you have a precompiled build feel free to simply run the executable or app bundle instead.

4. Click the "Search Plugins" button to initiate the search for audio plugins on your system. The search progress will be displayed in the command window.

5. Once the search is complete, you can save your plugin profile by clicking the "Save Profile" button. Enter your name and choose a location to save the profile file.

6. To compare two plugin profiles, make sure you have a profile file for each user in the `profiles/user1` and `profiles/user2` directories.

7. Click the "Compare Profiles" button to compare the two profiles. The application will generate a common plugin profile report, which will be saved in the profiles/common_report directory.

8. The common plugin profile report will list the plugins that are shared between the two users, as well as the plugins that are not shared.

## File Structure

* `main.py`: The main entry point of the application.
* `graphics.py`: Contains the GUI components and event handlers.
* `file_search.py`: Implements the search functionality for audio plugins.
* `compare.py`: Implements the comparison logic for plugin profiles.
* `tests.py`: Contains unit tests for the application.
* `profiles/user1`: Directory to store the plugin profile for user 1.
* `profiles/user2`: Directory to store the plugin profile for user 2.
* `profiles/common_report`: Directory to store the generated common plugin profile reports.

## Acknowledgements

Special thanks to [boot.dev](https://www.boot.dev) for their encouragement and guidance up to my first unguided personal project challenge for their platform.