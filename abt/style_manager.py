import tkinter as tk
from tkinter import ttk, font
from typing import Dict, Any, Optional
from enum import Enum
import json
from pathlib import Path

class ThemeType(Enum):
    LIGHT = "light"
    DARK = "dark"
    CUSTOM = "custom"

class StyleManager:
    """
    Gestore avanzato degli stili con supporto per temi e personalizzazione.
    """
    def __init__(self, font_family: str = "Segoe UI", theme: ThemeType = ThemeType.LIGHT):
        self.FONT_FAMILY = font_family
        self.CODE_FONT = "Consolas"
        self.current_theme = theme
        
        # Dimensioni font predefinite
        self.FONT_SIZES = {
            "title": 14,
            "heading": 12,
            "normal": 10,
            "code": 9,
            "small": 8
        }
        
        # Carica i temi
        self.themes = self._load_themes()
        self.current_theme_config = self.themes[theme.value]

    def _load_themes(self) -> Dict[str, Dict[str, Any]]:
        """Carica le configurazioni dei temi"""
        return {
            "light": {
                "background": "#ffffff",
                "foreground": "#000000", #colore testo 
                "selection_background": "#0078d7",
                "selection_foreground": "#ffffff",
                "link_color": "#0066cc",
                "code_background": "#d4cfcf", #"#f8f8f8",
                "code_foreground": "#000000",
                "heading_color": "#2c2c2c",
                "border_color": "#e0e0e0",
                "hover_background": "#f0f0f0",
                "accent_color": "#0078d7"
            },
            "dark": {
                "background": "#1e1e1e",
                "foreground": "#d4d4d4",
                "selection_background": "#264f78",
                "selection_foreground": "#ffffff",
                "link_color": "#4dc9ff",
                "code_background": "#2d2d2d",
                "code_foreground": "#d4d4d4",
                "heading_color": "#ffffff",
                "border_color": "#404040",
                "hover_background": "#2a2a2a",
                "accent_color": "#0078d7"
            }
        }

    def create_text_widget(self, parent: ttk.Frame) -> tk.Text:
        """Crea un widget di testo con stile moderno"""
        text_widget = tk.Text(
            parent,
            wrap="word",
            width=58,
            height=25,
            font=(self.FONT_FAMILY, self.FONT_SIZES["normal"]),
            background=self.current_theme_config["background"],
            foreground=self.current_theme_config["foreground"],
            selectbackground=self.current_theme_config["selection_background"],
            selectforeground=self.current_theme_config["selection_foreground"],
            insertbackground=self.current_theme_config["foreground"],
            padx=15,
            pady=15,
            borderwidth=0,
            relief="flat",
            spacing1=1,
            spacing2=2, ## Interlinea
            spacing3=2 ## Interlinea tra paragrafi, bullett e numbered
        )
        
        self._configure_text_tags(text_widget)
        self._configure_scrollbar_style(parent)
        return text_widget

    def _configure_text_tags(self, text_widget: tk.Text):
        """Configura i tag di testo con stili migliorati"""
        # Tag strutturali
        text_widget.tag_configure("title",
            font=(self.FONT_FAMILY, self.FONT_SIZES["title"], "bold"),
            foreground=self.current_theme_config["heading_color"],
            background=self.current_theme_config["background"],
            spacing1=10,
            spacing2=5,
            spacing3=1,
            relief="solid",             # Aggiunto
            borderwidth=0,              # Aggiunto
            lmargin1=0,                # Aggiunto
            lmargin2=0,                # Aggiunto
            rmargin=0,                 # Aggiunto
            selectbackground="gray",    # Aggiunto per migliorare la selezione
            wrap="none"                # Aggiunto per forzare larghezza completa
            )
        
        text_widget.tag_configure("heading",
            font=(self.FONT_FAMILY, self.FONT_SIZES["heading"], "bold"),
            foreground=self.current_theme_config["heading_color"],
            background=self.current_theme_config["background"],
            spacing1=10,
            spacing2=5,
            spacing3=1,
            relief="solid",             # Aggiunto
            borderwidth=0,              # Aggiunto
            lmargin1=0,                # Aggiunto
            lmargin2=0,                # Aggiunto
            rmargin=0,                 # Aggiunto
            selectbackground="gray",    # Aggiunto per migliorare la selezione
            wrap="none"                # Aggiunto per forzare larghezza completa
            )                              
        
        # Tag per raw text
        text_widget.tag_configure("raw",
            font=(self.CODE_FONT, self.FONT_SIZES["code"]),
            background=self.current_theme_config["code_background"],
            foreground=self.current_theme_config["code_foreground"],
            spacing1=1,
            spacing2=1,
            spacing3=1,
            relief="solid",             # Aggiunto
            borderwidth=0,              # Aggiunto
            lmargin1=0,                # Aggiunto
            lmargin2=0,                # Aggiunto
            rmargin=0,                 # Aggiunto
            selectbackground="gray")    # Aggiunto
        
        # Tag di formattazione
        text_widget.tag_configure("bold",
            font=(self.FONT_FAMILY, self.FONT_SIZES["normal"], "bold"))
            
        text_widget.tag_configure("italic",
            font=(self.FONT_FAMILY, self.FONT_SIZES["normal"], "italic"))
            
        text_widget.tag_configure("underline",
            underline=True)

        
        # Tag per codice
        text_widget.tag_configure("code",
            font=(self.CODE_FONT, self.FONT_SIZES["code"]),
            background=self.current_theme_config["code_background"],
            foreground=self.current_theme_config["code_foreground"],
            spacing1=2,
            spacing2=2,
            rmargin=0,
            borderwidth=1,
            relief="flat"
            ) #or "solid"
            
        text_widget.tag_configure("code_block",
            font=(self.CODE_FONT, self.FONT_SIZES["code"]),
            background=self.current_theme_config["code_background"],
            foreground=self.current_theme_config["code_foreground"],
            spacing1=10,
            spacing2=2,
            spacing3=10,
            rmargin=0,
            lmargin1=0,
            lmargin2=0,
            borderwidth=0,
            relief="flat", #or "solid"
            wrap='none' 
            ) 
            
        # Tag per syntax highlighting
        text_widget.tag_configure("syntax_keyword",
            foreground="#569cd6")
        text_widget.tag_configure("syntax_string",
            foreground="#ce9178")
        text_widget.tag_configure("syntax_comment",
            foreground="#6a9955",
            font=(self.CODE_FONT, self.FONT_SIZES["code"], "italic"))
        
        # Tag per link
        text_widget.tag_configure("link",
            foreground=self.current_theme_config["link_color"],
            underline=True)
        text_widget.tag_bind("link", "<Enter>", 
            lambda e: text_widget.config(cursor="hand2"))
        text_widget.tag_bind("link", "<Leave>", 
            lambda e: text_widget.config(cursor=""))

    def configure_notebook_style(self, style: ttk.Style):
        """Configura uno stile moderno per il notebook"""
        # Frame styles
        style.configure("Card.TFrame",
            background=self.current_theme_config["background"])
        style.configure("Content.TFrame",
            background=self.current_theme_config["background"])
            
        # Notebook styles
        style.configure("Custom.TNotebook",
            background=self.current_theme_config["background"],
            borderwidth=0)
        style.configure("Custom.TNotebook.Tab",
            padding=[12, 8],
            background=self.current_theme_config["background"],
            foreground=self.current_theme_config["foreground"],
            font=(self.FONT_FAMILY, 9))
            
        # Tab states
        style.map("Custom.TNotebook.Tab",
            background=[
                ("selected", self.current_theme_config["accent_color"]),
                ("active", self.current_theme_config["hover_background"])
            ],
            foreground=[
                ("selected", "#ffffff"),
                ("active", self.current_theme_config["foreground"])
            ])

    def _configure_scrollbar_style(self, parent: ttk.Frame):
        """Configura uno stile moderno per le scrollbar"""
        style = ttk.Style()
        
        # Scrollbar moderna e sottile
        style.layout("Custom.Vertical.TScrollbar", 
            [('Vertical.Scrollbar.trough',
                {'children': 
                    [('Vertical.Scrollbar.thumb', {'expand': '1'})],
                'sticky': 'ns'})])
                
        style.configure("Custom.Vertical.TScrollbar",
            background=self.current_theme_config["background"],
            troughcolor=self.current_theme_config["background"],
            borderwidth=0,
            arrowsize=0)
            
        style.map("Custom.Vertical.TScrollbar",
            background=[
                ("active", self.current_theme_config["accent_color"]),
                ("!active", self.current_theme_config["border_color"])
            ])

    def set_theme(self, theme: ThemeType):
        """Cambia il tema corrente"""
        self.current_theme = theme
        self.current_theme_config = self.themes[theme.value]

    def load_custom_theme(self, theme_file: Path):
        """Carica un tema personalizzato da file JSON"""
        try:
            with open(theme_file, 'r') as f:
                custom_theme = json.load(f)
            self.themes["custom"] = custom_theme
            return True
        except Exception as e:
            print(f"Errore nel caricamento del tema: {e}")
            return False