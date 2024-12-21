from typing import List, Dict, Any

class ListManager:
    """Gestisce le liste numerate, puntate e letterate"""
    
    def __init__(self):
        self.bullet_chars = ['•', '○', '▪', '▫']
        self.letter_chars = ['a', 'b', 'c', 'd', 'e', 'f']
        self.alpha_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        self.number_stack = [0] * 3
        self.letter_stack = [0] * 3
        self.alpha_stack = [0] * 3  # Nuovo stack per la numerazione alfabetica
        self.current_section = None

    def reset(self):
        """Resetta tutti i contatori"""
        self.number_stack = [0] * 3
        self.letter_stack = [0] * 3
        self.alpha_stack = [0] * 3  # Reset anche dello stack alfabetico
        self.current_section = None

    def start_section(self, section_name: str):
        """Inizia una nuova sezione"""
        if self.current_section != section_name:
            self.reset()
            self.current_section = section_name

    def get_bullet(self, level: int) -> str:
        """Restituisce il carattere bullet per il livello specificato"""
        return self.bullet_chars[level % len(self.bullet_chars)]

    def get_letter(self, level: int) -> str:
        """Restituisce la lettera per il livello specificato"""
        self.letter_stack[level] += 1
        letter_idx = self.letter_stack[level] - 1
        letter = self.letter_chars[letter_idx % len(self.letter_chars)]
        
        if level > 0:
            parent_number = self.number_stack[level - 1]
            return f"{parent_number}.{letter}"
        return letter

    def get_number(self, level: int) -> str:
        """Restituisce il numero per il livello specificato"""
        self.number_stack[level] += 1
        # Resetta i livelli successivi
        for i in range(level + 1, len(self.number_stack)):
            self.number_stack[i] = 0
            self.letter_stack[i] = 0
        
        return '.'.join(str(num) for num in self.number_stack[:level + 1])
    
    def get_alpha_marker(self, level: int) -> str:
        """
        Restituisce il marker alfabetico gerarchico per il livello specificato.
        Es: a), a1), a1.1)
        """
        self.alpha_stack[level] += 1
        
        # Resetta i livelli successivi
        for i in range(level + 1, len(self.alpha_stack)):
            self.alpha_stack[i] = 0
            
        if level == 0:
            # Primo livello: a), b), c)
            return f"{self.alpha_chars[self.alpha_stack[0] - 1]})"
        elif level == 1:
            # Secondo livello: a1), a2), a3)
            parent = self.alpha_chars[self.alpha_stack[0] - 1]
            return f"{parent}{self.alpha_stack[1]})"
        else:
            # Terzo livello: a1.1), a1.2), a1.3)
            parent = self.alpha_chars[self.alpha_stack[0] - 1]
            return f"{parent}{self.alpha_stack[1]}.{self.alpha_stack[2]})"

    def format_list_item(self, item: Dict[str, Any], is_numbered: bool = False) -> Dict[str, Any]:
        """Formatta un elemento della lista con il suo marker appropriato"""
        level = item.get('level', 0)
        text = item['text']
        is_lettered = item.get('lettered', False)
        is_alpha = item.get('alpha', False)  # Per le liste alfabetiche
        
        if is_numbered:
            if is_alpha:
                marker = self.get_alpha_marker(level)  # Usa il nuovo nome del metodo
                marker_text = marker  # Il marker include già la parentesi
                tag = f"alpha_{level}"
            elif is_lettered:
                marker = self.get_letter(level)
                marker_text = f"{marker})"
                tag = f"letter_{level}"
            else:
                marker = self.get_number(level)
                marker_text = f"{marker}."
                tag = f"number_{level}"
        else:
            marker = self.get_bullet(level)
            marker_text = marker
            tag = f"bullet_{level}"
        
        return {
            'text': text,
            'marker': marker_text,
            'tag': tag,
            'level': level
        }