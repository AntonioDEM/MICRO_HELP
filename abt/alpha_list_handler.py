import tkinter as tk
from typing import List

class GestoreLista:
    def __init__(self):
        self.lettere = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        self.indentazione = 5
        
    def processa_lista(self, widget_testo: tk.Text, alpha_list: List[str]):
        for idx, elemento in enumerate(alpha_list):
            lettera = self.lettere[idx]
            componenti = [comp.strip() for comp in elemento.strip().split("\n")]
            
            # Primo livello (a), b), c))
            widget_testo.insert("end", f"{lettera}) {componenti[0]}\n")
            
            if len(componenti) > 1:
                # Gestione sottopunti e dettagli
                sottopunto_counter = 1
                dettaglio_counter = 1
                
                for comp in componenti[1:]:
                    if comp.startswith("Sottopunto"):
                        # È un sottopunto (a.1, a.2, b.1, b.2)
                        indent = " " * self.indentazione
                        widget_testo.insert("end", f"{indent}{lettera}.{sottopunto_counter}) {comp}\n")
                        sottopunto_counter += 1
                    else:
                        # È un dettaglio (a.1.1, a.1.2)
                        indent = " " * (self.indentazione * 2)
                        widget_testo.insert("end", f"{indent}{lettera}.{sottopunto_counter-1}.{dettaglio_counter}) {comp}\n")
                        dettaglio_counter += 1