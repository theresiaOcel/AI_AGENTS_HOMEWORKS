# AI Email Agent

Tento projekt demonstruje schopnosti inteligentního agenta zpracovávat příchozí emaily a automaticky s nimi pracovat podle obsahu.

## Funkcionality

Agent provádí následující kroky:

1. **Klasifikace emailu**: Na základě obsahu je email zařazen do jedné z kategorií:
   - `meeting`: Naplánování schůzky v Google Kalendáři nebo návrh alternativního termínu.
   - `auto-reply`: Automatická odpověď podle databáze často kladených dotazů (FAQ).
   - `spam`: Označení jako spam.
   - `important`: Označení jako důležitý.
   - `unknown`: Nezařaditelné emaily.

2. **Kalendář**:
   - Kontrola dostupnosti termínu.
   - Vytvoření schůzky s informacemi (popis, lokace, online přes Google Meet).
   - Návrh alternativního volného termínu.

3. **Odpovědi na emaily**:
   - HTML formátované potvrzení o naplánování schůzky.
   - Automatická odpověď na běžné otázky z FAQ.
   - Návrh termínu pokud původní není dostupný.

4. **Zpracování a archivace emailů**:
   - Simulace přesunu emailů do složek (`spam`, `important`, `unknown`) pomocí zápisu do `.json` logů.

## Předpoklady

- Python 3.10+
- Přístupové údaje (credentials) ke Google Calendar API a Gmail API
- OpenAI API klíč (přes `.env`)

## Instalace

```bash
pip install -r requirements.txt
```

## Credentials

**NUTNÉ DOPLNIT**:

- `google_calendar_credential.json`
- `google_calendar_token.json`
- `gmail_credentials.json` (volitelně, pokud se používá odesílání emailu)

Tyto soubory nejsou součástí repozitáře – je nutné je získat z Google Cloud Console a umístit do složky `lecture7/credentials`.


## Simulace emailů

Testovací emaily jsou uloženy ve složce `lecture7/data/emails.json`. Načítání je simulováno jako reálný inbox.

## Ukázka složek pro záznam přesunutých emailů

Při klasifikaci emailu agent vytváří ve složce `data_outputs/` složky podle typu emailu a do nich ukládá `.json` soubory s obsahem zpráv, např.:

```
data_outputs/
├── spam/
│   └── log_20250804_145900.json
├── important/
│   └── log_20250804_145900.json
└── unknown/
```

## Auto-reply databáze

Soubor `faq.json` obsahuje přehled nejčastějších dotazů a odpovědí pro automatické zpracování.

