# AI Agent – Doporučovač elektronických produktů

Tento workflow v **n8n** vytváří chytrého asistenta, který pomáhá uživatelům najít vhodné elektronické produkty podle jejich dotazů.

## Funkce

1. **Chatová komunikace**
   - Uživatel píše dotazy do chatu (např. „Chci monitor Dell do 30 tisíc“).
   - Agent okamžitě odpovídá a zobrazí 2–5 nejvhodnějších produktů.

2. **Vyhledávání produktů**
   - Agent používá **MySQL databázi (query_sql node)** s tabulkou `products`.
   - Pokud uživatel nezadá značku ani cenový limit, doporučení bere podle **globálních preferencí (populární značky a kategorie)**.

3. **Doporučení a e-mail**
   - Po zobrazení seznamu se agent zeptá, zda chce výsledky poslat e‑mailem.
   - Pokud uživatel potvrdí a zadá e-mail, workflow:
     - Vytvoří **HTML e‑mail** se seznamem produktů ve formě přehledné tabulky.
     - Odešle e-mail pomocí `send_mail` node.

4. **Paměť konverzace**
   - `Simple Memory` umožňuje udržet kontext (např. zapamatovat si e-mail z předchozí zprávy).

## Použité nody

- **When chat message received** – vstup z chatu
- **AI Agent** – logika asistenta řízená jazykovým modelem
- **OpenAI Chat Model** – LLM model pro zpracování jazyka
- **query_sql** – výběr produktů z databáze
- **send_mail** – odeslání doporučených produktů e-mailem
- **Simple Memory** – ukládání kontextu konverzace (např. e-mail uživatele)

## Jak to funguje

1. Uživatel napíše dotaz do chatu.
2. Agent spustí dotaz do databáze, vrátí seznam 2–5 produktů.
3. Agent nabídne možnost poslat seznam na e-mail.
4. Po potvrzení odešle e‑mail s tabulkou produktů.

