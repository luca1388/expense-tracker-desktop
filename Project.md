# Expense Tracker Desktop App

## 1. Visione del progetto

Applicazione desktop **personale**, **offline-first**, per la gestione delle spese con particolare attenzione alle **spese ricorrenti** (bollette), ma estendibile a qualsiasi tipologia di costo.

Il progetto ha due obiettivi principali:

- **Funzionale**: aiutare l’utente a capire _dove_ e _quanto_ spende nel tempo
- **Didattico**: imparare Python e buone pratiche di sviluppo software costruendo un’app **production-ready**

---

## 2. Principi guida

- **Semplicità prima di tutto** (no over-engineering)
- **Separazione delle responsabilità**
- **Offline-first & privacy by design**
- **Estendibilità futura (AI locale)**
- **UI funzionale, non decorativa**

---

## 3. Scope e Boundaries

### 3.1 Cosa FA la v1 (in scope)

- Inserimento manuale delle spese
- Categorie predefinite + personalizzabili
- Spese ricorrenti con generazione automatica
- Allegato PDF opzionale per ogni spesa
- Database locale (SQLite)
- Visualizzazione elenco spese
- Grafici di riepilogo e andamento
- UI desktop con Tkinter

### 3.2 Cosa NON fa la v1 (out of scope)

- Parsing automatico dei PDF
- AI / Machine Learning
- Sincronizzazione cloud
- Multi-utente
- Import / Export dati
- UI moderna avanzata

---

## 4. Stack tecnologico

| Area       | Scelta                        |
| ---------- | ----------------------------- |
| Linguaggio | Python 3.11+                  |
| UI         | Tkinter + ttk                 |
| Database   | SQLite (sqlite3)              |
| Grafici    | matplotlib                    |
| PDF (v1)   | Solo archiviazione e apertura |
| AI (v2)    | LLM locale (Ollama)           |

---

## 5. Architettura logica

```
UI (Tkinter)
   ↓
Application Services
   ↓
Domain (modelli + regole)
   ↓
Persistence (SQLite)
```

### Motivazioni

- UI disaccoppiata dalla logica
- Facilità di test e refactor
- Inserimento dell’AI senza riscrivere il core

---

## 6. Struttura del progetto

```
expense_tracker/
│
├── main.py
│
├── ui/
│   ├── main_window.py
│   ├── expense_form.py
│   ├── expense_list.py
│   └── charts.py
│
├── domain/
│   ├── models.py
│   └── rules.py
│
├── services/
│   ├── expense_service.py
│   ├── recurrence_service.py
│   └── stats_service.py
│
├── persistence/
│   ├── db.py
│   └── repositories.py
│
├── resources/
│   └── categories.json
│
└── data/
    └── expenses.db
```

---

## 7. Modello dati (concettuale)

### Expense

- id
- date
- amount
- category_id
- description
- is_recurring
- pdf_path (opzionale)

### Category

- id
- name
- is_custom

### Recurrence

- expense_id
- frequency (monthly, yearly)
- next_date

---

## 8. Gestione spese ricorrenti

- Le ricorrenze sono entità separate
- All’avvio dell’app:

  - si controllano le ricorrenze attive
  - se `next_date <= oggi` → si genera una nuova spesa
  - si aggiorna `next_date`

Approccio semplice, robusto e offline.

---

## 9. Grafici previsti (v1)

1. **Spese per categoria** (periodo selezionato)
2. **Andamento temporale** (mensile)
3. **Confronto periodi** (mese / anno corrente vs precedente)

---

## 10. Estensione AI (v2 – futura)

### Funzionalità previste

- Estrazione importo e categoria da PDF
- Suggerimenti di categorizzazione
- Analisi andamento spese
- Insight automatici

### Vincoli

- AI solo come supporto
- Nessuna modifica automatica senza conferma
- Offline-first (LLM locale)

---

# 11. Piano di azione – User Stories

## EPIC 1 – Setup e Fondamenta

**US-1**

> Come sviluppatore voglio inizializzare il progetto con una struttura chiara per poter lavorare in modo ordinato.

**US-2**

> Come sviluppatore voglio configurare il database SQLite e la connessione per poter salvare i dati localmente.

---

## EPIC 2 – Gestione Categorie

**US-3**

> Come utente voglio avere un set di categorie base per iniziare subito a inserire spese.

**US-4**

> Come utente voglio poter creare categorie personalizzate.

---

## EPIC 3 – Gestione Spese

**US-5**

> Come utente voglio inserire una nuova spesa indicando data, importo, categoria e descrizione.

**US-6**

> Come utente voglio allegare opzionalmente un PDF a una spesa per consultarlo in futuro.

**US-7**

> Come utente voglio visualizzare l’elenco delle spese inserite.

---

## EPIC 4 – Spese Ricorrenti

**US-8**

> Come utente voglio contrassegnare una spesa come ricorrente.

**US-9**

> Come sistema voglio generare automaticamente le spese ricorrenti quando scadono.

---

## EPIC 5 – Analisi e Grafici

**US-10**

> Come utente voglio visualizzare un grafico delle spese per categoria in un periodo.

**US-11**

> Come utente voglio vedere l’andamento delle spese nel tempo.

**US-12**

> Come utente voglio confrontare le spese con il periodo precedente.

---

## EPIC 6 – Qualità e Stabilità

**US-13**

> Come sviluppatore voglio separare chiaramente UI, logica e persistenza per rendere il codice manutenibile.

**US-14**

> Come sviluppatore voglio gestire correttamente errori e dati inconsistenti.

---

## EPIC 7 – Estensione AI (futura)

**US-15**

> Come utente voglio che il sistema suggerisca categoria e importo partendo da un PDF.

**US-16**

> Come utente voglio ricevere suggerimenti sull’andamento delle spese rispetto al passato.

---

## 12. Nota finale

Questo documento è la **Single Source of Truth** del progetto.
Ogni nuova feature deve rispettare:

- i boundaries definiti
- l’architettura stabilita
- il principio di semplicità
