import tkinter as tk
from tkinter import ttk
import re
from typing import Optional

class CodeBlockHandler:
    """
    Gestisce i blocchi di codice con formattazione personalizzata.
    Da utilizzare in congiunzione con il sistema di help.
    """
    def __init__(self, font_family: str = "Consolas", font_size: int = 9):
        self.font_family = font_family
        self.font_size = font_size
        self.padding_x = 20  # Padding orizzontale
        self.padding_y = 10  # Padding verticale
        
        # Per calcoli futuri se necessario
        self.temp_widget = tk.Text()
        self.temp_widget.configure(font=(font_family, font_size))
        
        # Stile predefinito
        self.style = {
            'background': "#d4cfcf",
            'foreground': "#000000",
            'spacing2': 1,
            'relief': "flat",
            'borderwidth': 1,
            'radius': 10  # Per futura implementazione bordi arrotondati
        }

    def process_block(self, text_widget: tk.Text, code: str, start_index: str):
        """
        Processa un blocco di codice applicando la formattazione.
        
        Args:
            text_widget: Widget di testo dove inserire il codice
            code: Codice da formattare
            start_index: Indice di inizio per il tag
        """
        # Crea un tag unico per questo blocco
        tag_name = f"code_block_{start_index}"
        
        # Configura il tag principale per il testo
        text_widget.tag_configure(tag_name,
            font=(self.font_family, self.font_size),
            background=self.style['background'],
            foreground=self.style['foreground'],
            spacing1=self.padding_y,
            spacing2=self.style['spacing2'],
            spacing3=self.padding_y,
            lmargin1=self.padding_x,
            lmargin2=self.padding_x,
            rmargin=self.padding_x,
            relief=self.style['relief'],
            borderwidth=self.style['borderwidth']
        )
        
        # Inserisci il codice
        text_widget.insert("end", "\n")
        block_start = text_widget.index("end-1c")
        text_widget.insert("end", code + "\n", tag_name)
        block_end = text_widget.index("end-1c")
        
        # Applica il background
        text_widget.tag_add(f"{tag_name}_bg", block_start, block_end)
        text_widget.tag_configure(f"{tag_name}_bg",
            background=self.style['background'],
            relief=self.style['relief'],
            borderwidth=0
        )

    def set_style(self, **kwargs):
        """
        Imposta lo stile del blocco di codice.
        
        Args:
            **kwargs: Dizionario di stili da applicare
        """
        self.style.update(kwargs)

    def get_tag_name(self, index: str) -> str:
        """
        Genera un nome univoco per il tag.
        
        Args:
            index: Indice di riferimento
            
        Returns:
            Nome del tag
        """
        return f"code_block_{index}"