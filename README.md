# KN-Solvro – RAG na FastMCP + Claude Desktop + EDA (cocktails)

> **TL;DR:** Lokalny serwer **MCP** w Pythonie (FastMCP) udostępniający narzędzia do pracy z `cocktails.csv`: wyszukiwanie, filtrowanie i **prosty RAG** (TF-IDF + cosine). Repo zawiera też szybkie **EDA**. Integracja z **Claude Desktop** pozwala testować narzędzia bezpośrednio w czacie.

## Spis treści
- [Cel](#cel)
- [Funkcjonalności](#funkcjonalności)
- [Struktura repozytorium](#struktura-repozytorium)
- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Uruchomienie MCP servera](#uruchomienie-mcp-servera)
- [Integracja z Claude Desktop (MCP)](#integracja-z-claude-desktop-mcp)
- [Jak używać (przykłady)](#jak-używać-przykłady)
- [Jak to działa (RAG)](#jak-to-działa-rag)
- [EDA – eksploracja danych](#eda--eksploracja-danych)
- [Testy](#testy)
- [Rozwiązywanie problemów](#rozwiązywanie-problemów)
- [Licencja](#licencja)

---

## Cel
Zbudować proste, lokalne urządzenie **RAG**, które:
1) eksploruje zestaw **cocktails**,  
2) wystawia narzędzia przez **MCP** (FastMCP),  
3) integruje się z **Claude Desktop** do wygodnego testowania i rozmowy z danymi.

## Funkcjonalności
- **EDA (cocktails)** – szybkie statystyki i sanity-check danych.
- **MCP tools (FastMCP)**:
  - `read_drinks()` – lista kolumn w CSV,
  - `get_column(column_name)` – zwrot wybranej kolumny,
  - `filter_drinks_by_ingredient(ingredient)` – filtrowanie rekordów po fragmencie tekstu,
  - `rag_query(query, k=5)` – **retrieval** TF-IDF + cosine i zwrot kontekstu (top-K),
  - `recommend_cocktails(ingredients=[], tastes=[], k=5)` – prosta rekomendacja po składnikach/profilach smakowych.
- **Integracja z Claude Desktop (MCP)** – narzędzia dostępne w interfejsie czatu.

## Struktura repozytorium
```
├─ data/
│  └─ cocktails.csv
├─ eda/
│  └─ EDA_cocktails.ipynb          # notatnik z eksploracją danych (opcjonalnie outputs/)
├─ mcp_servers/
│  └─ csv_server.py                # MCP server: tools + prosty RAG (TF-IDF)
├─ tests/
│  └─ test_tools.py                # proste smoke testy (opcjonalnie)
├─ requirements.txt
└─ README.md
```

## Wymagania
- **Python** 3.10–3.12 (testowane na 3.11).
- System: Windows / macOS / Linux.
- (Windows) Zalecane **Microsoft C++ Build Tools** jeśli będziesz dodawać paczki z binariami.
- **Claude Desktop** (do integracji MCP).

## Instalacja
```bash
git clone <URL_DO_TEO_REPO>
cd <NAZWA_REPO>
python -m venv .venv
# Windows:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt`:
```
fastmcp
pandas
scikit-learn
```

## Uruchomienie MCP servera
Plik serwera: `mcp_servers/csv_server.py`.  
Upewnij się, że `data/cocktails.csv` istnieje.

```bash
python mcp_servers/csv_server.py
```

Serwer działa przez **stdio** – nie otwiera portu HTTP. Zwykle uruchamia go **Claude Desktop**, patrz niżej.

## Integracja z Claude Desktop (MCP)
1. Otwórz **Claude Desktop → Settings → Developer → Edit Config**.  
2. W pliku `%APPDATA%\Claude\claude_desktop_config.json` (Windows) dodaj/zmień:

```json
{
  "mcpServers": {
    "csv-mcp": {
      "type": "stdio",
      "command": "C:\\pełna\\ścieżka\\do\\repo\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\pełna\\ścieżka\\do\\repo\\mcp_servers\\csv_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

> Na macOS/Linux wskaż `.venv/bin/python` i odpowiednią ścieżkę do `csv_server.py`.

3. **Zapisz** plik i **zrestartuj** Claude Desktop.  
4. W nowym czacie powinny pojawić się narzędzia MCP z serwera `csv-mcp`.

## Jak używać (przykłady)
Wpisuj w czacie z Claude (on wywoła narzędzia MCP):

- **Sprawdź kolumny:**
  > *“Użyj `read_drinks` i wypisz dostępne kolumny.”*

- **Pobierz kolumnę:**
  > *“Wywołaj `get_column` dla `name` i pokaż 10 pierwszych.”*

- **Znajdź po składniku:**
  > *“`filter_drinks_by_ingredient(\"tequila\")` i podaj pasujące drinki.”*

- **RAG – kontekst do zapytania:**
  > *“`rag_query(\"lekka cytrusowa propozycja do kolacji\", k=5)` i zsyntetyzuj odpowiedź.”*

- **Rekomendacje:**
  > *“`recommend_cocktails(ingredients=[\"rum\",\"mięta\"], tastes=[\"citrus\"], k=5)` i zaproponuj 2 najlepsze z krótkim uzasadnieniem.”*

## Jak to działa (RAG)
- **Retrieval:** dane z każdego wiersza CSV są łączone w jeden tekst i indeksowane przez **TF-IDF**; podobieństwo liczone **cosine similarity**.  
- **Augmentation:** narzędzie `rag_query` zwraca **top-K** dopasowań (z `score`, `name`, `snippet` i `row`).  
- **Generation:** Claude używa zwróconego kontekstu, by sformułować końcową odpowiedź.

To podejście jest szybkie, działa **offline** i nie wymaga dodatkowych kluczy API.

## EDA – eksploracja danych
- Notatnik: `eda/EDA_cocktails.ipynb`.  
- Zawiera: opis kolumn, rozkłady, null-mapę i proste wykresy.  
- Uruchom:
  ```bash
  jupyter notebook eda/EDA_cocktails.ipynb
  ```

## Testy
Prosty smoke test narzędzi (przykład w `tests/test_tools.py`) – można uruchamiać lokalnie na DataFrame lub jako test integracyjny MCP (np. przez mock stdio).

## Rozwiązywanie problemów
- **Claude nie widzi serwera** – sprawdź, czy w configu jest klucz `mcpServers`, a `command` wskazuje na Twoje `.venv/.../python(.exe)`.  
- **`spawn ENOENT`** – zwykle zła ścieżka do Pythona lub `csv_server.py`.  
- **Polskie znaki** – ustaw `PYTHONIOENCODING=utf-8` (jak w przykładzie).  
- **`File not found: cocktails.csv`** – umieść `cocktails.csv` w `data/` albo popraw ścieżkę w `csv_server.py`.

## Licencja
MIT (dostosuj, jeśli wymagane). Prawa do danych `cocktails.csv` należą do ich źródła.

---

**Kontakt:** Imię Nazwisko · e-mail · (opcjonalnie) LinkedIn/GitHub.
