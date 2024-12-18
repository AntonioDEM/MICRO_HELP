import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from enum import Enum
import shutil
import sys

class ThemeManager:
    def __init__(self):
        # Ottieni il percorso del programma in esecuzione
        if getattr(sys, 'frozen', False):
            # Se è un exe (PyInstaller)
            self.base_path = Path(sys._MEIPASS)
        else:
            # Se è in sviluppo
            self.base_path = Path(__file__).parent

        # Definisci i percorsi
        self.data_path = self.base_path / "data"
        self.themes_path = self.data_path / "themes"
        self.available_themes_path = self.themes_path / "available"
        self.current_theme_path = self.themes_path / "current"

        # Crea le cartelle se non esistono
        self.available_themes_path.mkdir(parents=True, exist_ok=True)
        self.current_theme_path.mkdir(parents=True, exist_ok=True)

    def get_available_themes(self) -> List[str]:
        """Ottiene la lista dei temi disponibili"""
        return [f.stem for f in self.available_themes_path.glob("*.json")]

    def get_current_theme(self) -> Dict[str, Any]:
        """Legge il tema corrente"""
        current_theme_file = self.current_theme_path / "theme.json"
        if not current_theme_file.exists():
            # Se non esiste un tema corrente, usa il tema di default
            self.set_theme("light")
        
        with open(current_theme_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def set_theme(self, theme_name: str) -> bool:
        """Imposta il tema corrente"""
        theme_file = self.available_themes_path / f"{theme_name}.json"
        if not theme_file.exists():
            return False

        # Copia il tema selezionato nella cartella current
        shutil.copy2(
            theme_file, 
            self.current_theme_path / "theme.json"
        )
        return True

    def import_theme(self, theme_file: Path) -> bool:
        """Importa un nuovo tema nella cartella dei temi disponibili"""
        try:
            # Verifica che il file sia un JSON valido con la struttura corretta
            with open(theme_file, "r", encoding="utf-8") as f:
                theme_data = json.load(f)
                # Qui potresti aggiungere una validazione della struttura
            
            # Copia il file nella cartella dei temi disponibili
            shutil.copy2(
                theme_file, 
                self.available_themes_path / theme_file.name
            )
            return True
        except Exception as e:
            print(f"Errore nell'importazione del tema: {e}")
            return False