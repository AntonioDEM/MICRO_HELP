import re
from typing import List, Tuple, Dict, Any, Union

class TextFormatter:
    """Gestisce la formattazione del testo e dei tag speciali"""
    
    def __init__(self):
        self.inline_tags = {
            r'\\textbf\{([^}]+)\}': 'bold',
            r'\\textit\{([^}]+)\}': 'italic',
            r'\\underline\{([^}]+)\}': 'underline',
            r'\\link\{([^}]+)\}\{([^}]+)\}': 'link',
            r'\\code\{([^}]+)\}': 'code'
        }

    def process_text(self, text: str) -> List[Tuple[str, Any]]:
        """
        Processa il testo identificando e gestendo i vari tag di formattazione.
        
        Args:
            text: Il testo da processare con i tag di formattazione
            
        Returns:
            Lista di tuple (tag, contenuto) dove tag indica il tipo di formattazione
            e contenuto è il testo o un dizionario con le informazioni del tag
        """
        fragments = []
        last_end = 0
        matches = self._find_all_matches(text)
        
        # Processa i frammenti di testo
        for start, end, tag, content, original in sorted(matches, key=lambda x: x[0]):
            # Aggiungi il testo normale prima del tag
            if start > last_end:
                normal_text = text[last_end:start]
                if normal_text:
                    fragments.append(('normal', normal_text))
            
            # Aggiungi il contenuto formattato
            fragments.append((tag, content))
            last_end = end

        # Aggiungi eventuale testo rimanente
        if last_end < len(text):
            remaining_text = text[last_end:]
            if remaining_text:
                fragments.append(('normal', remaining_text))

        return fragments

    def _find_all_matches(self, text: str) -> List[Tuple[int, int, str, Any, str]]:
        """
        Trova tutti i tag di formattazione nel testo.
        
        Returns:
            Lista di tuple (start, end, tag, content, original)
        """
        matches = []
        
        for pattern, tag in self.inline_tags.items():
            for match in re.finditer(pattern, text):
                if tag == 'link':
                    matches.append(self._process_link_match(match, tag))
                elif tag == 'code':
                    matches.append(self._process_code_match(match, tag))
                else:
                    matches.append(self._process_standard_match(match, tag))
                    
        return matches

    def _process_link_match(self, match: re.Match, tag: str) -> Tuple[int, int, str, Dict[str, str], str]:
        """Processa un match di tipo link."""
        return (
            match.start(),
            match.end(),
            tag,
            {'text': match.group(1), 'url': match.group(2)},
            match.group(0)
        )

    def _process_code_match(self, match: re.Match, tag: str) -> Tuple[int, int, str, str, str]:
        """Processa un match di tipo codice."""
        code_content = match.group(1)
        is_block = '\n' in code_content
        return (
            match.start(),
            match.end(),
            'code_block' if is_block else 'code',
            code_content.strip(),
            match.group(0)
        )

    def _process_standard_match(self, match: re.Match, tag: str) -> Tuple[int, int, str, str, str]:
        """Processa un match standard (bold, italic, underline)."""
        return (
            match.start(),
            match.end(),
            tag,
            match.group(1),
            match.group(0)
        )

    def process_multiline_text(self, text: str) -> str:
        """Gestisce il testo multilinea e gli a capo"""
        if not text:
            return ""
        
        lines = text.split('\n')
        processed_lines = []
        current_paragraph = []
        
        for line in lines:
            line = line.rstrip()
            
            if not line:
                if current_paragraph:
                    processed_lines.append(' '.join(current_paragraph))
                    current_paragraph = []
                processed_lines.append('')
                continue
            
            if line.endswith('\\'):
                if current_paragraph:
                    processed_lines.append(' '.join(current_paragraph))
                    current_paragraph = []
                processed_lines.append(line[:-1].strip())
                continue
            
            current_paragraph.append(line.strip())
        
        if current_paragraph:
            processed_lines.append(' '.join(current_paragraph))
        
        return '\n\n'.join(line for line in processed_lines if line is not None)