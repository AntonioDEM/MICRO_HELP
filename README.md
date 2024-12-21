
# MicroHelp - Sistema di Help In Linea Semplice

## Premessa
MicroHelp è un sistema di documentazione integrato progettato per creare e visualizzare guide utente interattive direttamente nelle applicazioni Python.

Basato su una struttura **YAML** flessibile, offre un modo semplice ma potente per gestire la documentazione del tuo software.
E' stato progettato pensando alla semplicità d'uso sia per gli sviluppatori che per gli utenti finali. 

La documentazione viene scritta in file **YAML** (help_content.yaml) facilmente modificabili, mentre il sistema di visualizzazione offre un'esperienza di lettura pulita e semi professionale.

Gli sviluppatori possono facilmente integrare MicroHelp nelle proprie applicazioni e mantenere la documentazione aggiornata senza dover ricompilare il software, mentre gli utenti beneficiano di una guida in linea intuitiva e sempre accessibile.

Come è strutturato il codice

    micro_help/
                    ├── main_window.py
                    └── abt/
                        ├── __init__.py
                        ├── help_window.py
                        ├── about_window.py
                        ├── yaml_parser.py
                        ├── text_formatter.py
                        ├── list_manager.py
                        ├── style_manager.py
                        ├── scroll_handler.py
                        └── help_content.yaml 

## Caratteristiche principali

- Separazione tabs per argomenti
- Formattazione ricca del testo con supporto per grassetto, corsivo e sottolineato
- Liste multilivello con supporto per numerazione, punti elenco e lettere (ottimizzare)
- Blocchi di codice con evidenziazione della sintassi
- Link cliccabili per riferimenti esterni
- Sistema di temi integrato (chiaro/scuro)
- Interfaccia utente moderna e reattiva
- Intefaccia interattiva con il software: si puo scrivere interagendo con l'interfaccia principale
        
## Problemi e Ottimizzazioni

- Ottimizzazione formattazione testo
- Ottimizzazione code e block code e chiusura code e code_block
- Ottimizzazione style_manager
- Ottimizzazione text_manager
- Esternalizzare i setting dei temi con un file custom_theme.json
- altro

