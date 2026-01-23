# 🗺️ Roadmap – Expense Tracker Desktop

## 🔹 FASE 1 – Ricorrenze (fondamenta tecniche)

### 1.1 Spese ricorrenti – core

- [x] Model `RecurringExpense`
- [x] `RecurringExpenseRepository`
- [x] `RecurringExpenseService.generate_missing_expenses`
- [x] Generazione deterministica (no duplicati)
- [x] Generazione immediata della prima spesa alla creazione
- [x] Campo `recurring_expense_id` in `Expense`
- [ ] Migration DB step-by-step
  - aggiunta `recurring_expense_id` in `expenses`
  - eventuale backfill
  - aggiornamento versione DB

---

## 🔹 FASE 2 – UI: Spese ricorrenti

### 2.1 Lista spese

- [x] Colonna **Frequenza**
- [x] Evidenziazione visiva spese ricorrenti
  - colori soft
- [ ] (Backlog) Click destro su riga ricorrente → **Interrompi ricorrenza**

### 2.2 Sorting & UX Lista

- [ ] Sorting colonne (data, importo, categoria…) mantenendo l’ID interno
- [ ] Colonne numeriche allineate a destra
- [ ] Nascondere il campo ID dalla lista

### 2.3 Actions toolbar

- [ ] Valutare se rimuovere la actions toolbar e invece implementare le azioni con un menu contestuale che appare con click tasto destro sulla riga
- [ ] Delete di una recurring expense

---

## 🔹 FASE 3 – Form Add / Edit Expense

### 3.1 Add Expense

- [x] Form in modale
- [x] Validazione inline
- [x] Helper text / placeholder
- [x] Selezione frequenza con combobox (“Spesa singola” default)

### 3.2 Edit Expense

- [ ] Basic edit expense form
- [ ] Decidere se mostrare la frequency nel form edit 🧠
- [ ] Gestione edit spesa singola vs ricorrente

---

## 🔹 FASE 4 – Navigazione periodo

- [x] Usare nomi dei mesi invece dei numeri
- [x] Migliorare UX del month selector

---

## 🔹 FASE 5 – Analisi dati

- [ ] Nuova sezione **Analisi**
  - UX: dove inserirla?
- [ ] Confronto spese per categoria
  - mese corrente vs mese precedente
- [ ] Totali e variazioni percentuali

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

## 🔹 FASE 8 – Versione 2 dell'app: AI support

- [ ] Possibilità di allegare con le spese un file pdf
- [ ] Un modello LOCALE di AI analizza il documento e ne estrae informazioni rilevanti
  - LLM embedded nell'app in modo che i dati personali dell'utente non sono analizzati da LLM remote di terze parti (privacy first)
  - Valutare Olama
- [ ] Possibilità di importare le spese non solo a mano, ma leggere una cartella contenente files PDF.
  - L'app analizza i documenti e crea (suggerisce) in automatico delle spese leggendo importo e data dal documento (bollette)
  - L'utente deve solo confermare che le spese suggerite si possono inserire riducendo il lavoro manuale
  - Reconciliation: se una spesa era già aggiunta a mano e risulta anche in un documento (estratto conto banca) bisogna fare un merge o comunque non duplicare la spesa
