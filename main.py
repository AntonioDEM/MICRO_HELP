import tkinter as tk
from tkinter import ttk
from pathlib import Path
from abt.help_window import HelpWindow
from abt.about_window import AboutWindow

class MainWindow(tk.Tk):
    """Finestra principale dell'applicazione"""
    
    def __init__(self):
        super().__init__()
        
        # Configurazione base della finestra
        self.title("Help System Demo")
        self.geometry("400x300")
        
        # Creazione del menu
        self.create_menu()
        
        # Frame principale
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Esempio di contenuto
        label = ttk.Label(
            main_frame, 
            text="Benvenuto!\nUsa il menu Help per accedere alla documentazione.",
            justify=tk.CENTER
        )
        label.pack(expand=True)

    def create_menu(self):
        """Crea la barra dei menu"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Menu Help
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Guida", command=self.show_help)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)

    def show_help(self):
        """Mostra la finestra di help"""
        help_window = HelpWindow(self)
        if hasattr(help_window, 'window'):
            self.wait_window(help_window.window)

    def show_about(self):
        """Mostra la finestra about"""
        about_window = AboutWindow(self)
        if hasattr(about_window, 'window'):
            self.wait_window(about_window.window)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()