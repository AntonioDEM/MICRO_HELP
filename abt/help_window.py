import tkinter as tk
from tkinter import ttk
from pathlib import Path
import webbrowser

from .yaml_parser import YAMLParser
from .text_formatter import TextFormatter
from .list_manager import ListManager
from .style_manager import StyleManager
from .scroll_handler import ScrollHandler
from .alpha_list_handler import GestoreLista

class HelpWindow:
    """
    Finestra di help con supporto per formattazione ricca del testo
    e contenuto organizzato in tab.
    """
    
    def __init__(self, parent):
        self.parent = parent
        
        # Inizializza i gestori
        self.yaml_parser = YAMLParser()
        self.text_formatter = TextFormatter()
        self.list_manager = ListManager()
        self.style_manager = StyleManager()
        
        # Carica il contenuto
        self.help_content = self.yaml_parser.load_content(
            Path(__file__).parent / 'help_content.yaml'
        )
        
        # Crea la finestra
        self.setup_window()
        self._create_widgets()
        
    def setup_window(self):
        """Configura la finestra principale"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Guida Utente - ASP - Auto Spec for Pyinstaller")
        self.window.geometry("660x700")
        self.window.resizable(True, True)
        self.window.configure(bg='#f5f5f5')
        
        # Posizionamento affiancato alla finestra principale
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        self.window.geometry(f"600x700+{parent_x + 600}+{parent_y}")
    
    def _create_widgets(self):
        """Crea l'interfaccia principale"""
        # Setup stili
        style = ttk.Style()
        self.style_manager.configure_notebook_style(style)
        
        # Frame principale
        main_frame = ttk.Frame(self.window, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notebook per i tab
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Crea le sezioni
        for section_name, section_data in self.help_content.items():
            self._create_section(notebook, section_name, section_data)
    
    def _create_section(self, notebook: ttk.Notebook, name: str, data: dict):
        """Crea una sezione della guida"""
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text=name.title())
        
        # Container principale
        container = ttk.Frame(frame, relief="solid", borderwidth=1)
        container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Setup canvas e scrollbar
        canvas = tk.Canvas(container, background='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        content_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw", 
                           width=550, height=10001)
        
        # Crea e configura il text widget
        text_widget = self.style_manager.create_text_widget(content_frame)
        text_widget.pack(fill="both", expand=True, padx=5)
        
        # Processa il contenuto
        self._process_section_content(text_widget, data)
        
        # Setup dello ScrollHandler
        ScrollHandler(canvas, content_frame, self.window)
        
        # Disabilita l'editing
        text_widget.config(state="disabled")
    
    def _process_section_content(self, text_widget: tk.Text, data: dict):
        """Processa e inserisce il contenuto di una sezione"""
        if 'title' in data:
            self._insert_formatted_text(text_widget, data['title'], "title")
            text_widget.insert("end", "\n\n")
        
        if 'text' in data:
            self._insert_formatted_text(text_widget, data['text'])
            text_widget.insert("end", "\n\n")
        
        if 'sections' in data:
            for section in data['sections']:
                self._process_subsection(text_widget, section)
    
    def _process_subsection(self, text_widget: tk.Text, section: dict):
        """Processa una sottosezione"""
        self.list_manager.reset()
        
        if 'heading' in section:
            text_widget.insert("end", "\n")
            self._insert_formatted_text(text_widget, section['heading'], "heading")
            text_widget.insert("end", "\n\n")
        
        if 'text' in section:
            self._insert_formatted_text(text_widget, section['text'])
            text_widget.insert("end", "\n\n")
        
        if 'numbered' in section:
            for item in section['numbered']:
                self._insert_list_item(text_widget, item, True)
            text_widget.insert("end", "\n")
        
        if 'bullets' in section:
            for item in section['bullets']:
                self._insert_list_item(text_widget, item, False)
            text_widget.insert("end", "\n")
    
        if 'alpha_list' in section:
            self.text_formatter.lista_handler.processa_lista(text_widget, section['alpha_list'])
            text_widget.insert("end", "\n")
    
    def _insert_formatted_text(self, text_widget: tk.Text, text: str, base_tag: str = None):
        """Inserisce testo formattato con gestione migliorata dei link"""
        fragments = self.text_formatter.process_text(text)
        
        for tag, content in fragments:
            if tag == 'link':
                # Salva la posizione iniziale
                start_pos = text_widget.index("end-1c")
                # Inserisce il testo del link
                text_widget.insert("end", content['text'])
                # Salva la posizione finale
                end_pos = text_widget.index("end-1c")
                
                # Crea un tag unico per questo link
                link_tag = f"link_{len(text_widget.tag_names())}"
                # Configura il tag con lo stile del link
                text_widget.tag_configure(link_tag, 
                                       foreground="blue", 
                                       underline=True)
                # Applica il tag al testo
                text_widget.tag_add(link_tag, start_pos, end_pos)
                
                # Aggiungi il binding per il click
                def open_url(url=content['url']):
                    import webbrowser
                    webbrowser.open(url)
                
                text_widget.tag_bind(link_tag, "<Button-1>", 
                                   lambda e, url=content['url']: open_url(url))
                text_widget.tag_bind(link_tag, "<Enter>", 
                                   lambda e: text_widget.config(cursor="hand2"))
                text_widget.tag_bind(link_tag, "<Leave>", 
                                   lambda e: text_widget.config(cursor=""))
                
            elif tag == 'code_block':
                text_widget.insert("end", "\n")
                text_widget.insert("end", content, ("code_block",))
                text_widget.insert("end", "\n")
            else:
                tags = (tag,) if tag != 'normal' else ()
                if base_tag:
                    tags = (base_tag,) + tags
                text_widget.insert("end", content, tags)
                
    def _insert_code_block(self, text_widget: tk.Text, code: str):
        """Inserisce un blocco di codice con syntax highlighting"""
        import re
        
        # Pattern per il YAML
        patterns = {
            'key': r'^(\s*)([\w-]+)(:)',
            'number': r':\s*(\d+)',
            'value': r':\s*([^{#\n]+)'
        }
        
        lines = code.split('\n')
        for line in lines:
            start_pos = text_widget.index("end-1c")
            
            # Inserisci la linea
            text_widget.insert("end", line + "\n", "code_block")
            
            # Applica syntax highlighting
            for key, pattern in patterns.items():
                for match in re.finditer(pattern, line):
                    if key == 'key':
                        start = f"{start_pos} + {match.start(2)}c"
                        end = f"{start_pos} + {match.end(2)}c"
                        text_widget.tag_add("yaml_key", start, end)
                    elif key == 'number':
                        start = f"{start_pos} + {match.start(1)}c"
                        end = f"{start_pos} + {match.end(1)}c"
                        text_widget.tag_add("yaml_number", start, end)
                    elif key == 'value':
                        start = f"{start_pos} + {match.start(1)}c"
                        end = f"{start_pos} + {match.end(1)}c"
                        text_widget.tag_add("yaml_value", start, end)
    
    def _insert_list_item(self, text_widget: tk.Text, item: dict, is_numbered: bool):
        """Inserisce un elemento di lista"""
        formatted_item = self.list_manager.format_list_item(item, is_numbered)
        indent = "  " * formatted_item['level']
        
        text_widget.insert("end", f"{indent}{formatted_item['marker']} ",
                          formatted_item['tag'])
        
        self._insert_formatted_text(text_widget, formatted_item['text'])
        text_widget.insert("end", "\n")