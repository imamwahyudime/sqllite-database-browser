import tkinter as tk
from tkinter import ttk  # For themed widgets (nicer look)
from tkinter import filedialog
from tkinter import messagebox
import sqlite3
import os

class SQLiteGUITool:
    """
    A simple GUI application to browse SQLite database tables and data.
    """
    def __init__(self, master):
        """Initialize the GUI."""
        self.master = master
        master.title("Simple SQLite Browser")
        master.geometry("800x600") # Set initial window size

        self.db_path = None
        self.conn = None
        self.table_names = []

        # --- Styling ---
        style = ttk.Style()
        # Configure styles for widgets if desired (optional)
        # style.configure("TLabel", padding=5, font=('Helvetica', 10))
        # style.configure("TButton", padding=5)
        # style.configure("TListbox", padding=5)
        # style.configure("Treeview", padding=5)

        # --- Top Frame for File Selection ---
        self.top_frame = ttk.Frame(master, padding="10")
        self.top_frame.pack(fill=tk.X)

        self.btn_browse = ttk.Button(self.top_frame, text="Select Database (.db)", command=self.browse_db)
        self.btn_browse.pack(side=tk.LEFT, padx=5)

        self.lbl_db_path = ttk.Label(self.top_frame, text="No database selected", relief=tk.SUNKEN, padding=5)
        self.lbl_db_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # --- Main Frame for Tables and Data ---
        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # PanedWindow allows resizing sections
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # --- Left Frame for Table List ---
        self.left_frame = ttk.Frame(self.paned_window, padding="5", relief=tk.GROOVE)
        self.paned_window.add(self.left_frame, weight=1) # Add frame to paned window

        self.lbl_tables = ttk.Label(self.left_frame, text="Tables:")
        self.lbl_tables.pack(anchor=tk.W, pady=(0, 5))

        self.listbox_tables = tk.Listbox(self.left_frame, exportselection=False, height=10) # Use standard tk Listbox for better scrollbar integration
        self.listbox_tables.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox_tables.bind('<<ListboxSelect>>', self.on_table_select) # Event binding

        # Scrollbar for table listbox
        self.scrollbar_tables = ttk.Scrollbar(self.left_frame, orient=tk.VERTICAL, command=self.listbox_tables.yview)
        self.scrollbar_tables.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_tables.config(yscrollcommand=self.scrollbar_tables.set)

        # --- Right Frame for Data Display ---
        self.right_frame = ttk.Frame(self.paned_window, padding="5", relief=tk.GROOVE)
        self.paned_window.add(self.right_frame, weight=3) # Add frame, make it wider

        self.lbl_data = ttk.Label(self.right_frame, text="Data:")
        self.lbl_data.pack(anchor=tk.W, pady=(0, 5))

        # Treeview for displaying table data
        self.tree_data = ttk.Treeview(self.right_frame, show='headings') # 'headings' hides the default first empty column
        self.tree_data.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbars for Treeview
        self.scrollbar_data_y = ttk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.tree_data.yview)
        self.scrollbar_data_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_data_x = ttk.Scrollbar(self.right_frame, orient=tk.HORIZONTAL, command=self.tree_data.xview)
        self.scrollbar_data_x.pack(side=tk.BOTTOM, fill=tk.X) # Place X scrollbar below

        self.tree_data.config(yscrollcommand=self.scrollbar_data_y.set, xscrollcommand=self.scrollbar_data_x.set)

        # --- Status Bar ---
        self.status_bar = ttk.Label(master, text="Ready", relief=tk.SUNKEN, anchor=tk.W, padding=5)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def set_status(self, message):
        """Updates the status bar text."""
        self.status_bar.config(text=message)

    def browse_db(self):
        """Opens a file dialog to select the SQLite database file."""
        filepath = filedialog.askopenfilename(
            title="Select SQLite Database File",
            filetypes=(("Database files", "*.db"), ("All files", "*.*"))
        )
        if not filepath:
            return # User cancelled

        # Validate if it's actually a file
        if not os.path.isfile(filepath):
             messagebox.showerror("Error", f"'{filepath}' is not a valid file.")
             return

        self.db_path = filepath
        self.lbl_db_path.config(text=os.path.basename(self.db_path)) # Show only filename
        self.set_status(f"Selected: {self.db_path}")
        self.connect_and_load_tables()

    def connect_and_load_tables(self):
        """Connects to the selected database and loads table names."""
        if self.conn:
            try:
                self.conn.close()
            except sqlite3.Error:
                pass # Ignore errors closing previous connection
            self.conn = None
            self.clear_table_list()
            self.clear_data_display()

        if not self.db_path:
            return

        try:
            self.conn = sqlite3.connect(self.db_path)
            self.set_status(f"Successfully connected to {os.path.basename(self.db_path)}")
            self.load_tables()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect or read database:\n{e}")
            self.set_status(f"Error connecting to database: {e}")
            self.db_path = None
            self.lbl_db_path.config(text="No database selected")
            self.clear_table_list()
            self.clear_data_display()

    def load_tables(self):
        """Fetches table names from the database and populates the listbox."""
        self.clear_table_list()
        if not self.conn:
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            tables = cursor.fetchall()
            if not tables:
                self.set_status("No tables found in this database.")
                return

            self.table_names = [table[0] for table in tables]
            for name in self.table_names:
                self.listbox_tables.insert(tk.END, name)
            self.set_status(f"Found {len(self.table_names)} tables.")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while listing tables:\n{e}")
            self.set_status(f"Error listing tables: {e}")
        finally:
            cursor.close()

    def on_table_select(self, event):
        """Handles selection changes in the table listbox."""
        # Get selected indices
        selected_indices = self.listbox_tables.curselection()
        if not selected_indices:
            return # Nothing selected

        selected_index = selected_indices[0]
        if 0 <= selected_index < len(self.table_names):
            table_name = self.table_names[selected_index]
            self.view_table_data(table_name)
        else:
             self.set_status("Error: Invalid table index selected.") # Should not happen

    def view_table_data(self, table_name):
        """Fetches and displays data for the selected table in the Treeview."""
        self.clear_data_display()
        if not self.conn:
            self.set_status("Error: No database connected.")
            return

        cursor = self.conn.cursor()
        try:
            # Get column names using PRAGMA
            cursor.execute(f'PRAGMA table_info("{table_name}")') # Use quotes for safety
            columns_info = cursor.fetchall()
            if not columns_info:
                 self.set_status(f"Could not retrieve column info for table '{table_name}'.")
                 return

            column_names = [info[1] for info in columns_info]

            # Configure Treeview columns
            self.tree_data['columns'] = column_names
            for col in column_names:
                self.tree_data.heading(col, text=col)
                self.tree_data.column(col, anchor=tk.W, width=100) # Adjust width as needed

            # Fetch data
            # Using f-string here is generally safe IF table_name comes *only*
            # from the list populated by sqlite_master, preventing injection.
            # For external input, use parameterized queries.
            cursor.execute(f'SELECT * FROM "{table_name}"') # Use quotes around table name
            rows = cursor.fetchall()

            # Insert data into Treeview
            if not rows:
                self.set_status(f"Table '{table_name}' is empty.")
            else:
                for i, row in enumerate(rows):
                    # Convert all values to string for display
                    str_row = [str(item) for item in row]
                    self.tree_data.insert('', tk.END, values=str_row, iid=str(i)) # Use iid for unique row IDs
                self.set_status(f"Displayed data for table '{table_name}' ({len(rows)} rows).")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching data from table '{table_name}':\n{e}")
            self.set_status(f"Error viewing table '{table_name}': {e}")
        finally:
            cursor.close()

    def clear_table_list(self):
        """Clears the table listbox."""
        self.listbox_tables.delete(0, tk.END)
        self.table_names = []

    def clear_data_display(self):
        """Clears the data display Treeview."""
        # Delete existing columns
        for col in self.tree_data['columns']:
            # We don't actually delete columns in ttk.Treeview this way
            # We just clear the items and reconfigure columns later
            pass
        self.tree_data['columns'] = () # Reset columns tuple

        # Delete all items (rows)
        for item in self.tree_data.get_children():
            self.tree_data.delete(item)


# --- Main execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SQLiteGUITool(root)
    root.mainloop()
