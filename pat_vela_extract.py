from bs4 import BeautifulSoup

from lxml import etree
import json

HTML_PATH = "C://Users//michele.belotti//Development//my//patente_2//data//pat_vela.html"
# Leggi il contenuto del file HTML
with open(HTML_PATH, "r", encoding="utf-8") as file:
    html_content = file.read()

keys=["id", "img", "question",  "anwser"]
keys_id=[0, 1, 2, 4]

# Parsing del contenuto HTML
parser = etree.HTMLParser()
tree = etree.fromstring(html_content, parser)


# Trova tutte le righe (<tr>)
rows = tree.xpath("//tr")

# Estrai i dati da ciascuna riga
all_data = []
for row in rows:
    # Trova tutte le celle (<td>)
    cells = row.xpath(".//td")
    row_data = []
    missing_data=False
    for cell in cells:
        # Concatena e pulisci il testo da tutti i <span> dentro la cella
        text_parts = cell.xpath(".//span/text()")
        text = ' '.join(part.strip() for part in text_parts)  # Pulisce ogni parte e la unisce
        img = cell.xpath(".//img/@src")
        if img:  # Controlla anche se c'è un'immagine
            text = img[0]  # Usa l'attributo src dell'immagine
        row_data.append(text if text else "")  # Inserisce una stringa vuota se non c'è nulla
    if len(row_data)==7:
        row_dict = dict()
        for i in range(4):
            row_dict[keys[i]]=row_data[keys_id[i]]
            if i != 1 and row_data[i]=="":
                missing_data=True
    else:
        raise("wrong data row")

    if missing_data:
        print(row_data)

    all_data.append(row_dict)

# Salvataggio dei dati in formato JSON
def save_to_json(data, filename="C://Users//michele.belotti//Development//my//patente_2//data//pat_vela.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Salva il file JSON
save_to_json(all_data)