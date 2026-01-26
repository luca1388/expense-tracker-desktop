import pdfplumber
import dateparser
import re

# Configurazioni globali (sempre offline)
DATE_SETTINGS = {"DATE_ORDER": "DMY", "DEFAULT_LANGUAGES": ["it"]}
CATEGORIE_MAP = {
    "Utenze e Bollette": [
        "enel",
        "eni",
        "servizio elettrico",
        "a2a",
        "acea",
        "iren",
        "acquedotto",
        "tari",
        "gas",
        "luce",
    ],
    "Telecomunicazioni": [
        "vodafone",
        "tim",
        "windtre",
        "fastweb",
        "iliad",
        "telecom",
        "sky",
        "netflix",
        "disney+",
    ],
    "Alimentari e Casa": [
        "conad",
        "coop",
        "esselunga",
        "lidl",
        "carrefour",
        "despar",
        "eurospin",
        "md",
        "tigros",
    ],
    "Trasporti e Carburante": [
        "telepass",
        "trenitalia",
        "italo",
        "autostrade",
        "shell",
        "eni station",
        "q8",
        "tamoil",
        "uber",
    ],
    "Shopping e Svago": [
        "amazon",
        "ebay",
        "zalando",
        "ikea",
        "decathlon",
        "leroy merlin",
        "apple",
        "google",
        "playstation",
    ],
    "Banca e Finanza": [
        "commissioni",
        "imposta bollo",
        "canone",
        "interessi",
        "mutuo",
        "f24",
    ],
}


def pipeline_estrattore(pdf_path):
    risultati_finali = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, pagina in enumerate(pdf.pages):
            # --- TENTATIVO 1: Tabelle (Precisione Alta) ---
            tabelle = pagina.extract_tables()
            dati_pagina = []

            for tabella in tabelle:
                for riga in tabella:
                    # Puliamo la riga da None o spazi extra
                    riga_pulita = [str(cella).strip() for cella in riga if cella]

                    # Verifichiamo se la riga "sembra" finanziaria (ha una data e un numero)
                    data_obj, importo = analizza_riga_generica(" ".join(riga_pulita))
                    if data_obj and importo:
                        dati_pagina.append(
                            {"data": data_obj, "importo": importo, "metodo": "tabella"}
                        )

            # --- TENTATIVO 2: Testo (Fallback / Resilienza) ---
            # Se le tabelle non hanno prodotto nulla, passiamo al testo
            if not dati_pagina:
                testo_layout = pagina.extract_text(layout=True)
                if testo_layout:
                    for linea in testo_layout.split("\n"):
                        data_obj, importo = analizza_riga_generica(linea)
                        if data_obj and importo:
                            dati_pagina.append(
                                {
                                    "data": data_obj,
                                    "importo": importo,
                                    "metodo": "layout_text",
                                }
                            )

            risultati_finali.extend(dati_pagina)

    return risultati_finali


def analizza_riga_generica(testo):
    """Utility per capire se in una riga c'è una transazione."""
    # Regex per data e importo
    re_data = r"(\d{1,2}[/\-\s](?:\d{1,2}|[a-z]{3,9})[/\-\s]\d{2,4})"
    re_importo = r"(-?\d+(?:\.\d{3})*,\d{2})"

    match_data = re.search(re_data, testo, re.IGNORECASE)
    match_importo = re.search(re_importo, testo)

    if match_data and match_importo:
        dt = dateparser.parse(match_data.group(), settings=DATE_SETTINGS)
        val = clean_amount(match_importo.group())
        return dt, val
    return None, None


def clean_amount(s):
    try:
        return float(s.replace(".", "").replace(",", "."))
    except:
        return None


def classifica_spesa(descrizione):
    desc_low = descrizione.lower()

    for categoria, parole_chiave in CATEGORIE_MAP.items():
        for keyword in parole_chiave:
            if keyword in desc_low:
                return categoria

    return "Altro / Non classificato"


# Modifica alla pipeline precedente:
def pipeline_completa(pdf_path):
    dati_grezzi = pipeline_estrattore(
        pdf_path
    )  # Funzione definita nei messaggi precedenti

    output_finale = []
    print(dati_grezzi)
    for spesa in dati_grezzi:
        print(spesa)
        # Aggiungiamo la categoria basandoci sulla descrizione salvata
        spesa["categoria"] = classifica_spesa(spesa["descrizione"])
        output_finale.append(spesa)

    return output_finale


def main():
    pdf_path = "./data/hype.pdf"
    risultati = pipeline_estrattore(
        pdf_path
    )  # Funzione definita nei messaggi precedenti

    print(risultati)

    # for riga in risultati:
    #     print(
    #         f"Data: {riga['data'].date()}, Importo: {riga['importo']:.2f}, Categoria: {riga['categoria']}, Metodo: {riga['metodo']}"
    #     )


if __name__ == "__main__":
    main()
