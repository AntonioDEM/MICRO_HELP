<<<<<<< HEAD


# ASP Help System

## 1. GUIDA AI TAG DI FORMATTAZIONE 

```latex
1. STRUTTURA BASE
    ================
    Il sistema usa tag in stile LaTeX per la formattazione del testo. Ogni sezione della guida
    può utilizzare una combinazione dei seguenti tag.
2. TAG DISPONIBILI
    =================
    \\title{...}
- Usato per i titoli principali
- Supporta il testo multilinea
- Font: Segoe UI, 12pt, Bold
    Esempio:
    \\title{Titolo principale su più righe}

\\text{...}

- Usato per il corpo del testo
- Supporto completo multilinea
- Preserva indentazione e formattazione
- Permette paragrafi multipli
- Font: Segoe UI, 10pt
    Esempio:
    \\text{
      Primo paragrafo con
      formattazione preservata.

      Secondo paragrafo con
      indentazione. 
      }
\\heading{...}

- Usato per sottotitoli o sezioni
- Font: Segoe UI, 11pt, Bold
    Esempio:
    \\heading{Sezione Importante}

\\bullets{...}

- Usato per liste puntate
- Ogni elemento deve iniziare con '-'
- Font: Segoe UI, 10pt
    Esempio:
    \\bullets{
- Primo punto
- Secondo punto
- Terzo punto
    }
```

2. ESEMPIO COMPLETO
------------------

```
\\title{Titolo della Sezione}

\\text{
    Questo è un paragrafo introduttivo
    che può continuare su più righe.
    Questo è un secondo paragrafo che
    mantiene la sua formattazione.
}
\\heading{Sottosezione}
\\text{Testo della sottosezione}
\\bullets{
- Punto 1
- Punto 2
- Punto 3
}
```

3. NOTE TECNICHE
---------------

- Ogni tag deve essere chiuso con }
- Gli spazi all'inizio delle righe nel \\text{} vengono preservati
- Le righe vuote in \\text{} creano nuovi paragrafi
- I tag non possono essere nidificati
"""
Questa guida riassume:

1. La struttura generale del sistema

2. Tutti i tag disponibili con esempi
3. Come usare ogni tag correttamente
4. Come funziona la formattazione multilinea
5. Le regole di formattazione per ogni tipo di contenuto

=======


# ASP Help System

## 1. GUIDA AI TAG DI FORMATTAZIONE 

```latex
1. STRUTTURA BASE
    ================
    Il sistema usa tag in stile LaTeX per la formattazione del testo. Ogni sezione della guida
    può utilizzare una combinazione dei seguenti tag.
2. TAG DISPONIBILI
    =================
    \\title{...}
- Usato per i titoli principali
- Supporta il testo multilinea
- Font: Segoe UI, 12pt, Bold
    Esempio:
    \\title{Titolo principale su più righe}

\\text{...}

- Usato per il corpo del testo
- Supporto completo multilinea
- Preserva indentazione e formattazione
- Permette paragrafi multipli
- Font: Segoe UI, 10pt
    Esempio:
    \\text{
      Primo paragrafo con
      formattazione preservata.

      Secondo paragrafo con
      indentazione. 
      }
\\heading{...}

- Usato per sottotitoli o sezioni
- Font: Segoe UI, 11pt, Bold
    Esempio:
    \\heading{Sezione Importante}

\\bullets{...}

- Usato per liste puntate
- Ogni elemento deve iniziare con '-'
- Font: Segoe UI, 10pt
    Esempio:
    \\bullets{
- Primo punto
- Secondo punto
- Terzo punto
    }
```

2. ESEMPIO COMPLETO
------------------

```
\\title{Titolo della Sezione}

\\text{
    Questo è un paragrafo introduttivo
    che può continuare su più righe.
    Questo è un secondo paragrafo che
    mantiene la sua formattazione.
}
\\heading{Sottosezione}
\\text{Testo della sottosezione}
\\bullets{
- Punto 1
- Punto 2
- Punto 3
}
```

3. NOTE TECNICHE
---------------

- Ogni tag deve essere chiuso con }
- Gli spazi all'inizio delle righe nel \\text{} vengono preservati
- Le righe vuote in \\text{} creano nuovi paragrafi
- I tag non possono essere nidificati
"""
Questa guida riassume:

1. La struttura generale del sistema

2. Tutti i tag disponibili con esempi
3. Come usare ogni tag correttamente
4. Come funziona la formattazione multilinea
5. Le regole di formattazione per ogni tipo di contenuto

>>>>>>> 40c852c9d68d1a215a4036cd005b0bb53cc63a46
