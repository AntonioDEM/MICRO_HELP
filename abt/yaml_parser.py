from pathlib import Path
import yaml
from typing import Dict, Any, List

class YAMLParser:
    """Gestisce il parsing del file YAML con supporto per strutture flessibili"""
    
    def __init__(self):
        self.sections_stack = []
        
    def load_content(self, file_path: Path) -> Dict[str, Any]:
        """Carica e valida il contenuto YAML"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
            return self._process_content(content)
        except Exception as e:
            print(f"Errore nel caricamento del file YAML: {e}")
            return self._get_error_content()

    def _process_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Processa e normalizza il contenuto YAML supportando formati flessibili"""
        processed = {}
        
        for section_name, section_data in content.items():
            # Se è una stringa diretta, la trattiamo come text
            if isinstance(section_data, str):
                processed[section_name] = {
                    'text': section_data.strip()
                }
            # Se è un dizionario, processiamo la struttura
            elif isinstance(section_data, dict):
                processed[section_name] = self._process_section(section_data)
        
        return processed

    def _process_section(self, section_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa una sezione supportando formati multipli"""
        processed = {}
        
        # Gestione diretta del testo
        if isinstance(section_data, str):
            return {'text': section_data.strip()}
            
        # Gestione del titolo
        if 'title' in section_data:
            processed['title'] = section_data['title'].strip()
            
        # Gestione del testo principale
        if 'text' in section_data:
            processed['text'] = section_data['text'].strip()
            
        # Gestione delle sezioni
        processed['sections'] = []
        
        # Se c'è una sottosezione diretta
        if 'content' in section_data:
            subsection = {
                'text': section_data['content'].strip()
            }
            processed['sections'].append(subsection)
            
        # Gestione delle sezioni tradizionali
        if 'sections' in section_data:
            for subsection in section_data['sections']:
                processed_subsection = self._process_subsection(subsection)
                if processed_subsection:
                    processed['sections'].append(processed_subsection)
                    
        # Gestione diretta delle liste
        if 'bullets' in section_data:
            processed['sections'].append({
                'bullets': self._process_list_items(section_data['bullets'])
            })
            
        if 'numbered' in section_data:
            processed['sections'].append({
                'numbered': self._process_list_items(section_data['numbered'])
            })
        
        return processed

    def _process_subsection(self, subsection: Any) -> Dict[str, Any]:
        """Processa una sottosezione in modo flessibile"""
        # Se è una stringa diretta, la trattiamo come testo
        if isinstance(subsection, str):
            return {'text': subsection.strip()}
            
        processed = {}
        
        # Gestione heading opzionale
        if 'heading' in subsection:
            processed['heading'] = subsection['heading'].strip()
            
        # Gestione testo
        if 'text' in subsection:
            processed['text'] = subsection['text'].strip()
            
        # Gestione liste
        if 'bullets' in subsection:
            processed['bullets'] = self._process_list_items(subsection['bullets'])
            
        if 'numbered' in subsection:
            processed['numbered'] = self._process_list_items(subsection['numbered'])
        
        return processed

    def _process_list_items(self, items: Any) -> List[Dict[str, Any]]:
        """Processa gli elementi delle liste in modo flessibile"""
        processed = []
        
        if isinstance(items, list):
            for item in items:
                if isinstance(item, str):
                    processed.append({
                        'text': item.strip(),
                        'level': 0
                    })
                elif isinstance(item, dict):
                    processed_item = {
                        'text': item['text'].strip(),
                        'level': item.get('level', 0)
                    }
                    if 'lettered' in item:
                        processed_item['lettered'] = item['lettered']
                    processed.append(processed_item)
                    
        return processed

    def _get_error_content(self) -> Dict[str, Any]:
        """Restituisce un contenuto di errore predefinito"""
        return {
            "error": {
                "title": "Guida non disponibile",
                "text": "Il contenuto della guida non può essere caricato.",
                "sections": []
            }
        }