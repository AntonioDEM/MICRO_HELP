import re
from typing import List, Tuple, Dict, Any
import tkinter as tk
from tkinter import ttk
from .code_block_handler import CodeBlockHandler
from .alpha_list_handler import GestoreLista

class TextFormatter:
    """Gestisce la formattazione del testo e dei tag speciali"""
    
    def __init__(self):
        # Tag di formattazione inline standard
        self.inline_tags = {
            r'\\textbf\{([^}]+)\}': 'bold',
            r'\\textit\{([^}]+)\}': 'italic',
            r'\\underline\{([^}]+)\}': 'underline',
            r'\\link\{([^}]+)\}\{([^}]+)\}': 'link',
            r'\\code\{([^}]+)\}': 'code',
            r'\\codeb\{([^}]+)\}': 'code_block'  # Aggiunto
        }
        
        # Tag speciali
        self.special_tags = {
            r'\\raw\{([^}]+)\}': 'raw',     # Per mostrare i comandi come testo
            r'\\escape\{([^}]+)\}': 'escape' # Alternativa per escapare i caratteri
        }
        self.code_block_handler = CodeBlockHandler()
        self.lista_handler = GestoreLista()

    def process_text(self, text: str) -> List[Tuple[str, Any]]:
        """
        Processa il testo identificando e gestendo i vari tag di formattazione.
        Supporta raw text e caratteri di escape.
        """
        if not text:
            return []

        # Prima processa i raw blocks
        raw_blocks = self._extract_raw_blocks(text)
        if raw_blocks:
            return self._process_with_raw_blocks(text, raw_blocks)

        # Processamento normale
        fragments = []
        last_end = 0
        matches = self._find_all_matches(text)
        
        for start, end, tag, content, original in sorted(matches, key=lambda x: x[0]):
            # Testo normale prima del tag
            if start > last_end:
                normal_text = text[last_end:start]
                if normal_text:
                    fragments.append(('normal', normal_text))
            
            # Contenuto formattato
            fragments.append((tag, content))
            last_end = end

        # Testo rimanente
        if last_end < len(text):
            remaining_text = text[last_end:]
            if remaining_text:
                fragments.append(('normal', remaining_text))

        return fragments
    
    def _insert_formatted_text(self, text_widget: tk.Text, text: str, base_tag: str = None):
            """Inserisce testo formattato"""
            fragments = self.text_formatter.process_text(text)
            
            for tag, content in fragments:
                if tag == 'code_block':
                    # Debug
                    print(f"Processing code block: {content}")
                    # Se content è un dict con 'content' e 'position'
                    if isinstance(content, dict):
                        self.text_formatter.code_block_handler.process_block(
                            text_widget, 
                            content['content'],
                            content['position']
                        )
                    else:
                        # Se è una stringa diretta
                        self.text_formatter.code_block_handler.process_block(
                            text_widget, 
                            content,
                            str(text_widget.index("end"))
                        )
                else:
                    tags = (tag,) if tag != 'normal' else ()
                    if base_tag:
                        tags = (base_tag,) + tags
                    text_widget.insert('end', content, tags)

    def _extract_raw_blocks(self, text: str) -> List[Tuple[int, int, str]]:
        """Estrae i blocchi raw dal testo"""
        raw_blocks = []
        for pattern in (r'\\raw\{([^}]+)\}', r'\\escape\{([^}]+)\}'):
            for match in re.finditer(pattern, text):
                raw_blocks.append((
                    match.start(),
                    match.end(),
                    match.group(1)
                ))
        return sorted(raw_blocks, key=lambda x: x[0])

    def _process_with_raw_blocks(self, text: str, raw_blocks: List[Tuple[int, int, str]]) -> List[Tuple[str, Any]]:
        """Processa il testo preservando i blocchi raw"""
        fragments = []
        last_end = 0
        
        for start, end, content in raw_blocks:
            # Processa il testo prima del blocco raw
            if start > last_end:
                pre_text = text[last_end:start]
                if pre_text:
                    fragments.extend(self.process_text(pre_text))
            
            # Aggiungi il blocco raw senza processarlo
            fragments.append(('normal', content))
            last_end = end
        
        # Processa il testo rimanente
        if last_end < len(text):
            remaining = text[last_end:]
            if remaining:
                fragments.extend(self.process_text(remaining))
        
        return fragments

    def _find_all_matches(self, text: str) -> List[Tuple[int, int, str, Any, str]]:
        """Trova tutti i tag di formattazione nel testo"""
        matches = []
        
        # Processa i tag inline
        for pattern, tag in self.inline_tags.items():
            for match in re.finditer(pattern, text):
                if tag == 'link':
                    matches.append(self._process_link_match(match, tag))
                elif tag == 'code':
                    matches.append(self._process_code_match(match, tag))
                elif tag == 'code_block':  # gestione specifica per codeb
                    matches.append(self._process_codeb_match(match, tag))
                else:
                    matches.append(self._process_standard_match(match, tag))
        
        return sorted(matches, key=lambda x: x[0])
    
    def _process_codeb_match(self, match: re.Match, tag: str) -> Tuple[int, int, str, str, str]:
        """Processa un match di tipo codeb"""
        code_content = match.group(1)
        return (
            match.start(),
            match.end(),
            'code_block',
            code_content,
            match.group(0)
        )

    def _process_link_match(self, match: re.Match, tag: str) -> Tuple[int, int, str, Dict[str, str], str]:
        """Processa un match di tipo link"""
        return (
            match.start(),
            match.end(),
            tag,
            {'text': match.group(1), 'url': match.group(2)},
            match.group(0)
        )

    def _process_code_match(self, match: re.Match, tag: str) -> Tuple[int, int, str, str, str]:
        """Processa un match di tipo codice"""
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
        """Processa un match standard (bold, italic, underline)"""
        return (
            match.start(),
            match.end(),
            tag,
            match.group(1),
            match.group(0)
        )

    def process_multiline_text(self, text: str) -> str:
        """
        Gestisce il testo multilinea preservando formattazione e raw blocks.
        Supporta:
        - A capo espliciti con \
        - A capo impliciti con linee vuote
        - Raw blocks
        - Escapeing di caratteri speciali
        """
        if not text:
            return ""
        
        lines = text.split('\n')
        processed_lines = []
        current_paragraph = []
        in_raw_block = False
        raw_content = []
        
        for line in lines:
            line = line.rstrip()
            
            # Gestione raw blocks
            if '\\raw{' in line:
                if current_paragraph:
                    processed_lines.append(' '.join(current_paragraph))
                    current_paragraph = []
                in_raw_block = True
                raw_content.append(line)
                continue
            
            if in_raw_block:
                raw_content.append(line)
                if '}' in line:
                    in_raw_block = False
                    processed_lines.append('\n'.join(raw_content))
                    raw_content = []
                continue
            
            # Gestione normale
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
                processed_lines.append(line[:-1].rstrip())
                continue
            
            current_paragraph.append(line.strip())
        
        # Processa l'ultimo paragrafo o raw block
        if in_raw_block and raw_content:
            processed_lines.append('\n'.join(raw_content))
        elif current_paragraph:
            processed_lines.append(' '.join(current_paragraph))
        
        return '\n\n'.join(line for line in processed_lines if line is not None)
