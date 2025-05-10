# Simple SQLite GUI Browser

A straightforward desktop application built with Python and Tkinter to browse SQLite database tables and their data. This tool provides a user-friendly interface for quickly inspecting the contents of SQLite database files (`.db`).

## Features:

* **Database File Selection:** Easily browse and select an SQLite database file (`.db`) using a file dialog.
* **Table Listing:** Displays a list of all tables found within the selected database.
* **Data Viewing:** Shows the data from a selected table in a clear, scrollable treeview format.
* **Column Display:** Automatically detects and displays column headers for the selected table.
* **Resizable Panes:** The table list and data view panes can be resized for user convenience.
* **Status Bar:** Provides feedback on the current operation (e.g., database connected, table loaded, errors).
* **Error Handling:** Includes basic error messages for common issues like invalid file selection or database errors.

## Requirements:

* Python 3.x
* Tkinter (usually included with standard Python installations)
* SQLite3 (usually included with standard Python installations)

No external libraries beyond what's typically available in a standard Python environment are required.

## How to Run:

1.  **Save the Code:** Save the provided Python script as a `.py` file (e.g., `sqlite_gui_tool.py`).
2.  **Open a Terminal or Command Prompt:** Navigate to the directory where you saved the file.
3.  **Execute the Script:** Run the script using the Python interpreter:
    ```bash
    python sqlite_gui_tool.py
    ```
    This will launch the GUI application.

## Usage:

1.  **Launch the Application:** Run the script as described above.
2.  **Select Database:**
    * Click the "Select Database (.db)" button.
    * A file dialog will appear. Navigate to and select your SQLite database file (e.g., `my_database.db`).
    * The path to the selected database (filename only) will appear next to the button, and the status bar will indicate a successful connection.
3.  **Browse Tables:**
    * Once a database is loaded, the listbox on the left will populate with the names of the tables in that database.
    * If no tables are found, a message will indicate this in the status bar.
4.  **View Table Data:**
    * Click on a table name in the listbox.
    * The data from the selected table will be displayed in the treeview on the right.
    * You can scroll vertically and horizontally if the data exceeds the viewable area.
5.  **Change Database:** Simply click the "Select Database (.db)" button again to choose a different database file. The interface will update accordingly.

## Code Overview:

The application is built using the `tkinter` library for the graphical user interface and the `sqlite3` module for database interaction.

* **`SQLiteGUITool` class:** Encapsulates the entire application.
    * **`__init__(self, master)`:** Sets up the main window, frames, widgets (buttons, labels, listbox, treeview), and scrollbars.
    * **`browse_db(self)`:** Handles the database file selection dialog and initiates the connection.
    * **`connect_and_load_tables(self)`:** Manages the SQLite connection and calls `load_tables`.
    * **`load_tables(self)`:** Fetches and displays table names from the connected database.
    * **`on_table_select(self, event)`:** Triggered when a table is selected from the list, then calls `view_table_data`.
    * **`view_table_data(self, table_name)`:** Fetches and displays the data (column headers and rows) for the specified table in the treeview.
    * **`clear_table_list(self)`:** Clears the list of tables.
    * **`clear_data_display(self)`:** Clears the data displayed in the treeview.
    * **`set_status(self, message)`:** Updates the text in the status bar.

## Potential Future Improvements:

* Editable data cells.
* Ability to execute custom SQL queries.
* Schema view for tables.
* Export data (e.g., to CSV).
* More advanced styling and theming.
* Filtering and sorting of data in the treeview.