import tkinter as tk
from tkinter import ttk
import psutil
import time

class ManagementBarApp:
    """
    A system management bar with a refined "Dracula" dark theme.
    Displays real-time CPU, Memory, Disk usage, and the current time.
    """
    def __init__(self, root):
        """
        Initialize the application.
        :param root: The root tkinter window.
        """
        self.root = root
        self.root.title("System Management Bar")

        # --- Color Palette (Dracula Theme) ---
        self.BG_COLOR = "#282a36"      # Background
        self.FG_COLOR = "#f8f8f2"      # Foreground
        self.BTN_BG = "#44475a"        # Button Background
        self.BTN_ACTIVE_BG = "#6272a4"  # Button Hover/Active
        self.ACCENT_COLOR = "#bd93f9"   # Purple Accent
        
        # --- Window Configuration ---
        window_width = 800
        window_height = 40
        screen_width = self.root.winfo_screenwidth()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = 0
        
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        self.root.resizable(False, False)
        # Set the main window background color
        self.root.configure(background=self.BG_COLOR)
        
        # --- Style Configuration ---
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # General style for widgets
        self.style.configure('.', background=self.BG_COLOR, foreground=self.FG_COLOR)

        # Frame and Label style
        self.style.configure('TFrame', background=self.BG_COLOR)
        self.style.configure('TLabel', font=('Segoe UI', 10))
        
        # Separator style
        self.style.configure('TSeparator', background=self.BTN_BG)

        # Button style
        self.style.configure('TButton',
            font=('Segoe UI', 9, 'bold'),
            padding=2,
            background=self.BTN_BG,
            foreground=self.FG_COLOR,
            borderwidth=0,
            relief=tk.FLAT
        )
        self.style.map('TButton',
            background=[('active', self.BTN_ACTIVE_BG)], # Highlight on hover
            relief=[('pressed', tk.FLAT)]
        )

        # Checkbutton style
        self.style.configure('TCheckbutton', font=('Segoe UI', 9))
        self.style.map('TCheckbutton',
            indicatorcolor=[
                ('selected', self.ACCENT_COLOR),
                ('!selected', self.BTN_BG)
            ]
        )
        
        # --- Main Frame ---
        # The main frame holds all the content
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # --- Create Widgets ---
        self.create_widgets(main_frame)
        
        # --- Initial Data Load ---
        self.update_stats()
        self.update_time()

    def create_widgets(self, parent_frame):
        """
        Creates and arranges all the GUI widgets.
        :param parent_frame: The master frame to hold the widgets.
        """
        # --- Stat Labels ---
        self.cpu_label = ttk.Label(parent_frame, text="CPU: ...")
        self.cpu_label.pack(side=tk.LEFT, padx=5)
        
        self.mem_label = ttk.Label(parent_frame, text="Memory: ...")
        self.mem_label.pack(side=tk.LEFT, padx=5)
        
        self.disk_label = ttk.Label(parent_frame, text="Disk: ...")
        self.disk_label.pack(side=tk.LEFT, padx=5)
        
        # A separator to push controls to the right
        separator = ttk.Separator(parent_frame, orient='vertical')
        separator.pack(side=tk.LEFT, fill='y', padx=10, pady=2)
        
        self.time_label = ttk.Label(parent_frame, text="Time: ...", font=('Segoe UI', 10, 'bold'))
        self.time_label.pack(side=tk.LEFT, padx=5)

        # --- Control Widgets (packed to the right) ---
        self.exit_button = ttk.Button(parent_frame, text="Exit", command=self.root.destroy)
        self.exit_button.pack(side=tk.RIGHT, padx=5)
        
        self.refresh_button = ttk.Button(parent_frame, text="Refresh", command=self.update_stats)
        self.refresh_button.pack(side=tk.RIGHT, padx=5)
        
        self.on_top_var = tk.BooleanVar()
        self.on_top_check = ttk.Checkbutton(
            parent_frame, 
            text="Always on Top", 
            variable=self.on_top_var, 
            command=self.toggle_on_top
        )
        self.on_top_check.pack(side=tk.RIGHT, padx=5)

    def update_stats(self):
        """Fetches system stats using psutil and updates the labels."""
        try:
            self.cpu_label.config(text=f"CPU: {psutil.cpu_percent(interval=None):.1f}%")
            self.mem_label.config(text=f"Memory: {psutil.virtual_memory().percent}%")
            self.disk_label.config(text=f"Disk: {psutil.disk_usage('/').percent}%")
        except Exception as e:
            print(f"Error fetching stats: {e}")

    def update_time(self):
        """Updates the time label every second."""
        self.time_label.config(text=time.strftime('%H:%M:%S'))
        self.root.after(1000, self.update_time)

    def toggle_on_top(self):
        """Toggles the window's 'always on top' attribute."""
        self.root.wm_attributes("-topmost", self.on_top_var.get())

def main():
    """Main function to create the root window and start the app."""
    root = tk.Tk()
    app = ManagementBarApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
