from lecture1 import roles
from lecture1.ReactAgent.mail_agent import MailAgent


if __name__ == '__main__':
    mail_agent = MailAgent()

    user_prompt_old ="""Načti e-maily ze souboru 'mails.json', který se nachází ve složce input. "
                                    "Takto načtené emaily roztřiď. Na auto-reply emaily odpověz."
                                    "Pokud existují emaily, které žádají o schůzku (meetings), pak naplánuj schůzky."
                                    "Pokud mezi emaily jsou některé označeny jako spam, přesuň tyto emaily do koše."
                                    "Pokud mezi emaily jsou nějaké, které jsou důležité a vyžadují moji pozornost, označ je jako důležité."
                                    "Pokud jsou mezi emaily nějaké, které se nepodařilo rozřadit do kategorie, označ je jako neznámé."
                                    "Po dokončení úkolu velmi stručně shrň svoji práci a stručně shrň zda došlo k úspěchu při vykonávání úkolu nebo ne."""

    user_prompt = """Načti všechny e-maily ze souboru `input/mails.json`.
                    Poté s celou dávkou e-mailů proveď následující kroky:
                    
                    1. Identifikuj e-maily, na které lze automaticky odpovědět, a vygeneruj odpovědi.
                    2. Najdi e-maily, které obsahují žádost o naplánování schůzky, a navrhni vhodné termíny (v souladu s pravidly kalendáře).
                    3. Všechny e-maily označené jako spam přesuň do koše.
                    4. E-maily, které jsou důležité a vyžadují moji osobní pozornost, označ jako důležité.
                    5. E-maily, které nelze zařadit do žádné z výše uvedených kategorií, označ jako neznámé.
                    
                    Nakonec velmi stručně shrň:
                    - kolik e-mailů bylo zpracováno,
                    - kolik e-mailů spadalo do každé kategorie,
                    - zda byl úkol úspěšně dokončen, nebo zda nastaly nějaké problémy."""

    messages = [
        {"role": "system", "content": roles.AI_ASSISTANT},
        {"role": "user", "content": user_prompt},
    ]

    result = mail_agent.run_agent(messages)
    print("---VÝSLEDEK---")
    print(result)