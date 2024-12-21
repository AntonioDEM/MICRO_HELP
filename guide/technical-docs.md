# Documentazione Tecnica Help System

## Indice
1. [help_window.py](#help_windowpy)
2. [yaml_parser.py](#yaml_parserpy)
3. [text_formatter.py](#text_formatterpy)
4. [list_manager.py](#list_managerpy)
5. [scroll_handler.py](#scroll_handlerpy)

## help_window.py

### Elenco Metodi
- `__init__(self, parent)`
- `setup_window(self)`
- `_create_widgets(self)`
- `_create_section(self, notebook, name, data)`
- `_process_section_content(self, text_widget, data)`
- `_process_subsection(self, text_widget, section)`
- `_insert_formatted_text(self, text_widget, text, base_tag)`
- `_insert_code_block(self, text_widget, code)`
- `_insert_list_item(self, text_widget, item, is_numbered)`

### Descrizione
La classe HelpWindow è il coordinatore principale del sistema di help. Gestisce la creazione della finestra di help e coordina l'interazione tra i vari componenti.

#### Funzionalità Chiave
- Creazione finestra di help con supporto multi-tab
- Gestione del caricamento e visualizzazione del contenuto
- Coordinamento tra parser YAML, formattazione del testo e gestione delle liste

## yaml_parser.py

### Elenco Metodi
- `__init__(self)`
- `load_content(self, file_path)`
- `_process_content(self, content)`
- `_process_section(self, section_data)`
- `_process_list_items(self, items)`
- `_get_error_content(self)`

### Descrizione
Il YAMLParser si occupa del caricamento e della normalizzazione del contenuto YAML.

#### Funzionalità Chiave
- Parsing del file YAML
- Normalizzazione della struttura dei dati
- Gestione degli errori di caricamento
- Supporto per sezioni annidate

## text_formatter.py

### Elenco Metodi
- `__init__(self)`
- `process_text(self, text)`
- `_process_link_match(self, match, tag)`
- `_process_code_match(self, match, tag)`
- `_process_standard_match(self, match, tag)`
- `process_multiline_text(self, text)`

### Descrizione
TextFormatter gestisce la formattazione del testo e l'elaborazione dei tag speciali.

#### Funzionalità Chiave
- Parsing dei tag di formattazione (bold, italic, underline)
- Gestione dei link
- Gestione dei blocchi di codice
- Formattazione multilinea

## list_manager.py

### Elenco Metodi
- `__init__(self)`
- `reset(self)`
- `get_bullet(self, level)`
- `get_letter(self, level)`
- `get_number(self, level)`
- `format_list_item(self, item, is_numbered)`

### Descrizione
ListManager gestisce la creazione e formattazione delle liste numerate, puntate e letterate.

#### Funzionalità Chiave
- Supporto per liste multilivello
- Gestione della numerazione gerarchica
- Supporto per liste letterate
- Formattazione degli elementi delle liste

## scroll_handler.py

### Elenco Metodi
- `__init__(self, canvas, content_frame, window)`
- `setup_canvas(self)`
- `setup_scroll_bindings(self)`
- `configure_scroll(self, event)`
- `_dispatch_scroll_windows(self, event)`
- `_dispatch_scroll_unix(self, event)`
- `_perform_scroll(self, delta)`
- `on_enter_canvas(self, event)`
- `on_leave_canvas(self, event)`
- `on_destroy(self, event)`

### Descrizione
ScrollHandler gestisce lo scrolling delle pagine di help con supporto multi-tab.

#### Funzionalità Chiave
- Gestione dello scrolling per tutte le pagine
- Supporto cross-platform (Windows/Unix)
- Gestione eventi del mouse
- Pulizia automatica dei binding

### Note Implementative
- Usa un dizionario statico per tracciare i canvas attivi
- Supporta scroll fluido e configurabile
- Gestisce correttamente la pulizia delle risorse

---

### Best Practices
1. **Gestione delle Risorse**
   - Tutti i binding vengono puliti correttamente
   - Le risorse vengono liberate quando le finestre vengono chiuse

2. **Modularità**
   - Ogni classe ha responsabilità ben definite
   - Le dipendenze sono chiaramente dichiarate
   - Il codice è organizzato in moduli logici

3. **Estensibilità**
   - Facile aggiungere nuovi tipi di formattazione
   - Supporto per nuovi tipi di liste
   - Sistema di parser YAML flessibile

### Limitazioni Note
1. Il sistema di help è sincrono (caricamento bloccante)
2. La sintassi YAML deve seguire una struttura specifica
3. Il supporto per immagini non è implementato

### Suggerimenti per l'Uso
1. Organizzare il contenuto YAML in sezioni logiche
2. Utilizzare i tag di formattazione in modo consistente
3. Testare su diverse piattaforme per verificare lo scrolling
4. Mantenere una struttura gerarchica chiara nelle liste

