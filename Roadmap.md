# 🗺️ Roadmap – Expense Tracker Desktop

## 🔹 FASE 1 – Ricorrenze (fondamenta tecniche)

### 1.1 Spese ricorrenti – core

- [x] Model `RecurringExpense`
- [x] `RecurringExpenseRepository`
- [x] `RecurringExpenseService.generate_missing_expenses`
- [x] Generazione deterministica (no duplicati)
- [x] Generazione immediata della prima spesa alla creazione
- [x] Campo `recurring_expense_id` in `Expense`
- [x] Migration DB step-by-step
  - aggiunta `recurring_expense_id` in `expenses`
  - eventuale backfill
  - aggiornamento versione DB

---

## 🔹 FASE 2 – UI: Spese ricorrenti

### 2.1 Lista spese

- [x] Colonna **Frequenza**
- [x] Evidenziazione visiva spese ricorrenti
  - colori soft
- [x] (Backlog) Click destro su riga - ricorrente → **Interrompi ricorrenza**
- [ ] Marcare visivamente le righe interrotte (grigio / colonna Stato)

### 2.2 Sorting & UX Lista

- [x] Sorting colonne (data, importo, categoria…) mantenendo l’ID interno
- [x] Colonne numeriche allineate a sinistra
- [x] Nascondere il campo ID dalla lista
- [ ] Refactor column index
- [ ] Aggiungere sorting per frequency e disattivare per description
- [ ] Default sorting + highlight sorted column

### 2.3 Actions toolbar

- [ ] Valutare se rimuovere la actions toolbar e invece implementare le azioni con un menu contestuale che appare con click tasto destro sulla riga

---

## 🔹 FASE 3 – Form Add / Edit Expense

### 3.1 Add Expense

- [x] Form in modale
- [x] Validazione inline
- [x] Helper text / placeholder
- [x] Selezione frequenza con combobox (“Spesa singola” default)
- [ ] Import/export spesa via CSV (to be validated)

### 3.2 Edit Expense

- [x] Basic edit expense form
- [x] Decidere se mostrare la frequency nel form edit 🧠
- [ ] Gestione edit spesa singola vs ricorrente

---

## 🔹 FASE 4 – Navigazione periodo

- [x] Usare nomi dei mesi invece dei numeri
- [x] Migliorare UX del month selector

---

## 🔹 FASE 5 – Analisi dati

- [ ] Fase preliminare: valutare se creare un menu di sistema (File, View, ...) dove mettere le actions (nuova spesa) e aprire la view di Analisi
- [x] Nuova sezione **Analisi**
  - UX: dove inserirla?
- [x] Confronto spese per categoria
  - mese corrente vs mese precedente
- [x] Totali e variazioni percentuali
- [ ] Sezione (tab) recap annuale: analisi che mostra l'andamento annuale (grafico con spese di categoria per ogni mese, media mensile di spesa globale e per categoria)
      ➡ Grafico: spesa per categoria
      ➡ Grafico: andamento periodo
      ➡ Bottone "Esporta PDF"
      ➡ PDF con:
  - periodo
  - totali
  - grafici

---

## 🔹 FASE 6 – Versioning & Bootstrap

- [ ] Versione App (`APP_VERSION`)
- [ ] Versione DB (`DB_VERSION`)
- [ ] Notifica se esiste una versione più recente dell’app

---

## 🔹 FASE 7 – Rifiniture UI generali

- [ ] Migliorare allineamenti e spaziature
- [ ] Migliore leggibilità tabella
- [ ] Stati hover / selected più chiari
- [ ] Empty screen al primo avvio dell'app

## 🔹 FASE 8 – Versione 2 dell'app: AI support

- [ ] Possibilità di allegare con le spese un file pdf
- [ ] Un modello LOCALE di AI analizza il documento e ne estrae informazioni rilevanti
  - LLM embedded nell'app in modo che i dati personali dell'utente non sono analizzati da LLM remote di terze parti (privacy first)
  - Valutare Olama
  - **Primo step**: analisi PDF senza LLM usando pdfplumber
- [ ] Possibilità di importare le spese non solo a mano, ma leggere una cartella contenente files PDF.
  - L'app analizza i documenti e crea (suggerisce) in automatico delle spese leggendo importo e data dal documento (bollette)
  - L'utente deve solo confermare che le spese suggerite si possono inserire riducendo il lavoro manuale
  - Reconciliation: se una spesa era già aggiunta a mano e risulta anche in un documento (estratto conto banca) bisogna fare un merge o comunque non duplicare la spesa

## 🔹 FASE 9 – Localizzazione dell'app

- [ ] App multilingua: italiano (default) e inglese (fallback)
- [ ] Error handling con codici di errore invece che messaggi cosi si possono localizzare

## 🔹 FASE 10 – Testing

- [x] Aggiungere unit test per spese ricorrenti (STOP / edge cases) ✅
  - stop active
  - stop already stopped → ValueError
  - stop non esistente → ValueError
- [ ] Considerare test per Expense normali (create / update / delete) in futuro
- [x] Fixture `db_connection_test` per DB in-memory
- [x] Fixture `recurring_repository` e `recurring_service` per ridurre boilerplate test
