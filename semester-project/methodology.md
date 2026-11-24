Níže je kompletní návrh jednotné metodiky pro všechny tři varianty vycházející z [project-proposal.md](./project-proposal.md). Dokument je postavený tak, aby přesně naplňoval požadavky na férové srovnání, umožnil vyhodnotit výzkumné otázky i hypotézy a eliminoval riziko zkreslení lidských zásahů.

## 1. Výchozí podmínky před spuštěním (Zmrazení vstupů)

Aby bylo možné výsledky všech tří variant (Varianta A: MetaGPT, Varianta B: LangGraph, Varianta C: OpenHands) objektivně porovnat, musí každý vývojář před prvním spuštěním splnit následující podmínky:

1. **Identické vstupní soubory:** Všechny tři systémy dostanou na vstupu naprosto stejnou sadu podkladů: `user-stories.md` (odvozené uživatelské příběhy a akceptační kritéria pro F1–F9 bez důvěrného zadání Junáka), `openAPI.yaml` (závazný kontrakt REST API), `initial-prompt.md` (jednotné zadání tech stacku a provozních podmínek) a konkrétní prompt z [`milestone-prompts/`](https://github.com/h0ldemslav/artificial-intelligence-course-pef-mendelu/tree/main/semester-project/milestone-prompts) (viz sekce 2). Po zahájení experimentu se tyto soubory nesmí měnit.

2. **Identický jazykový model:** Všechny tři nástroje musí být nakonfigurovány na model `gemini-3.8-flash` přes Google AI Studio API se stejnou teplotou (`temperature=0.2`) pro konzistentní generování kódu.

3. **Přesný rozsah implementace:** Všechny tři varianty implementují 100 % příběhů s prioritou **Must** (22 příběhů) a **Should** (7 příběhů) dle `user-stories.md`, což odpovídá všem endpointům v `openAPI.yaml`. Volitelné příběhy **Could** (`US-X.1` QR platba, `US-X.2` potvrzovací e-mail) se neimplementují.

4. **Povinný tech stack a technické kotvy pro automatické testy:**

- **Backend:** Python (FastAPI, SQLAlchemy/SQLModel, Pydantic) vystavený přesně na adrese `http://localhost:8080/api/v1`.

- **Frontend:** React (Vite, TypeScript, TailwindCSS) s uživatelským rozhraním v češtině (NFR-7).

- **Databáze:** PostgreSQL, která je nutná pro atomickou transakční kontrolu kapacity při souběžné zátěži 300 uživatelů v `US-F7.4` (metriky M11–M14).

- **Spuštění a testovací endpointy:** Celý systém musí jít spustit jedním příkazem (`docker compose up --build` dle NFR-8). Endpointy `/health`, `/test/reset` a `/test/login-as` se zpřístupní v M3.1; `/test/bulk-users` se přidá až v M3.3. Ve finálním stavu musí být při nastavení `APP_ENV=test` dostupné všechny endpointy ze sekce `test-support`, včetně fixního UUID výchozí akce `11111111-1111-4111-8111-111111111111`.

5. **Čistý repozitář:** Každá varianta běží ve svém izolovaném repozitáři se stejnou výchozí adresářovou strukturou (`/backend`, `/frontend`, `.github/workflows/ci.yml`).

6. **Aktivní měření spotřeby (M22):** Před prvním dotazem na LLM musí být zapnuté logování počtu volání modelu, vstupních a výstupních tokenů a času běhu.

## 2. Společný harmonogram milníků (Struktura běhu)

Hypotéza H5 v project-proposalu stanovuje hranici nejvýše 5 lidských zásahů na milník (metrika M20). Aby měl pojem „milník“ u všech tří vývojářů stejnou váhu a respektoval datové závislosti v `user-stories.md` a `openAPI.yaml`, dělí se fáze návrhu a implementace na 4 přesně ohraničené milníky:

| Milník   | Název a rozsah                                                       | Klíčové výstupy a kontrola při schválení                                                                                                                                                                                                                                                                                           |
| -------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **M2**   | **Návrh architektury a datového modelu**                             | Návrh DB schématu (všechny entity z `openAPI.yaml`), struktura `docker-compose.yml` (PostgreSQL + FastAPI na `:8080/api/v1` + React) a návrh českých obrazovek (NFR-7). Kód aplikace se ještě nepíše.                                                                                                                              |
| **M3.1** | **Iterace 1: Jádro, skautIS mock, správa akcí a registrace**         | Pokrývá **F1, F2, F3, US-F8.1** a endpointy `/health`, `/test/reset`, `/test/login-as`. Funguje výběr fiktivní osoby ze skautISu, založení akce adminem, registrace se 4 kategoriemi údajů, validace, časové okno registrace a generování 8znakového kódu `[A-HJKMNP-Z2-9]{8}`.                                                    |
| **M3.2** | **Iterace 2: Skupiny, pravidlo nezletilých a matice oprávnění**      | Pokrývá **F4, F5, F6**. Funguje založení skupiny s 6znakovým kódem `[A-HJKMNP-Z2-9]{6}`, připojení a odebrání člena, výpočet plnoletosti k `event.startDate`, stav `awaiting_group` pro nezletilé bez skupiny, zákaz nezletilého vedoucího a serverová kontrola 4 kategorií údajů podle rolí (HTTP 403 při neoprávněném přístupu). |
| **M3.3** | **Iterace 3: Programy se souběžností, administrace, export a audit** | Pokrývá **F7, US-F8.2–F8.4, F9** a endpoint `/test/bulk-users`. Funguje přihlašování na programy s DB transakčním zámkem kapacity a kontrolou časových kolizí, přehled účastníků s filtry a vyhledáváním bez diakritiky, CSV export v UTF-8 s BOM a neměnný auditní log bez hodnot zdravotních údajů.                              |

## Spouštění milníků 

Každý milník (`M2`, `M3.1`, `M3.2`, `M3.3`) spusťte jako novou čistou session (nový běh) nad aktuálním zacommitovaným stavem repozitáře. V každé session musí být jako vstup dostupné `initial-prompt.md`, `user-stories.md`, `openAPI.yaml` a konkrétní prompt z [`milestone-prompts/`](https://github.com/h0ldemslav/artificial-intelligence-course-pef-mendelu/tree/main/semester-project/milestone-prompts).

## 3. Specifika ovládání: MAS (Varianty A, B) vs. Single Agent (Varianta C)

Aby se ze single agenta nestalo interaktivní párové programování s člověkem, platí pro řízení běhu tato pravidla:

- **Varianta A (MetaGPT) a Varianta B (LangGraph):** Agentní týmy běží autonomně uvnitř daného milníku (předávají si artefakty mezi rolemi architekta, vývojáře a testera). Člověk do běhu nezasahuje, dokud se orchestrátor sám nezastaví na kontrolním bodu milníku nebo neskončí chybou.

- **Varianta C (OpenHands – Single Agent):** V nastavení OpenHands musí být vypnuto delegování úkolů na subagenty. Vývojář nesmí s agentem chatovat po malých krocích. Na začátku milníku zadá jeden souhrnný zadávací prompt (celé zadání daného milníku včetně pokynu napsat a spustit testy) a nechá OpenHands pracovat autonomně v jeho smyčce, dokud agent sám neohlásí splnění úkolu nebo se nezasekne. Každá další zpráva od člověka se započítává jako zásah.

## 4. Pravidla pro lidské zásahy a taxonomie událostí (Metriky M20 a M21)

Člověk vystupuje výhradně jako kontrolor milníků a sám kód nepíše. Každou interakci během běhu klasifikujeme do jedné z těchto kategorií:

### A. Běžný průchod (Nepočítá se jako zásah, M20 +0)

- **`MILESTONE_START`:** První zadání úkolu na začátku milníku M2, M3.1, M3.2 nebo M3.3.
- **`MILESTONE_APPROVED`:** Člověk zkontroluje výstup milníku (projde dokumentaci, spustí aplikaci a testy) a potvrdí přechod na další milník bez výhrad.

- **`RATE_LIMIT_PAUSE`:** Pokud běh spadne čistě kvůli HTTP 429 (vyčerpání limitu požadavků za minutu na Gemini API) nebo výpadku sítě, vývojář počká na obnovení kvóty a obnoví běh ze uloženého checkpointu bez změny promptu. Do deníku se zapíše jen ztracený čas, nikoli lidský zásah.

### B. Započítávaný lidský zásah (M20 +1, cíl ≤ 5 na milník dle H5)

Jakýkoli jiný vstup člověka se započítává do metriky M20:

1. **`INTERVENTION_NUDGE` (M20 +1):** Agent se zacyklil (např. opakovaně spouští stejný nefunkční příkaz v terminálu nebo se ptá na upřesnění) a člověk mu pošle vysvětlující nebo naváděcí zprávu.

2. **`MILESTONE_REJECTED` (M20 +1, M21 +1):** Výstup milníku nesplňuje akceptační kritéria (např. chybí endpoint z `openAPI.yaml` nebo neprocházejí vlastní testy agenta). Člověk výstup zamítne a pošle seznam chyb k opravě.

3. **`TASK_SPLIT` (M20 +1):** Pokud agent nedokáže milník dokončit ani po korekčních zprávách (nebo se blíží limitu 5 zásahů), člověk ukončí konverzaci, otevře novou a zbývající část milníku rozdělí na menší podúkoly.

4. **`MANUAL_FIX` (M20 +1):** Pokud je agent zcela neschopný opravit triviální blokující chybu (např. chybný import nebo konfiguraci portu) a brání to pokračování, může člověk provést minimální opravu sám. V Gitu musí být tento zásah oddělen samostatným commitem s prefixem `[HUMAN-FIX]`.

### Pravidla pro formulaci zpráv při zásahu

Vývojář **nesmí agentovi napsat konkrétní kus kódu ani mu prozradit strukturu skrytých testů**. Zpráva musí vždy odkazovat pouze na `user-stories.md`, `openAPI.yaml` nebo chybovou hlášku z terminálu:

- **Správný příklad zprávy při `MILESTONE_REJECTED`:**

    > „Výstup milníku M3.2 zamítám. Při kontrole podle `openAPI.yaml` a `user-stories.md` byly zjištěny tyto dva nedostatky: 1) Endpoint `GET /api/v1/events/{eventId}/registrations/{registrationId}?categories=health` vrací pro roli `program_team` status 200 místo požadovaného 403 (`US-F6.1`). 2) Při odebrání nezletilého člena ze skupiny přes `DELETE /groups/{groupId}/members/{registrationId}` zůstane stav registrace `completed` místo přepnutí na `awaiting_group` (`US-F5.1`, AK 5). Oprav tyto dva body a znovu spusť unit testy.“

- **Špatný příklad (zakázáno):**
    > „V souboru `backend/routers/registrations.py` na řádku 84 přidej podmínku `if 'health' in categories and current_user.role == 'program_team': raise HTTPException(403)`...“

## 5. Kde a jak logovat spotřebu tokenů (Metrika M22)

Každý vývojář udržuje ve svém repozitáři dvě místa pro evidenci:

1. **Deník událostí a zásahů (`intervention-log.csv`):** Soubor musí být uchován tak, aby MAS/single agent neměl k němu přístup. Řádek se zapisuje okamžitě po každém kroku. Po dokončení M3.3 se všechny tři soubory zkopírují do centrálního repozitáře do složky `evaluation/logs/`.
2. **Surové logy spotřeby tokenů (`evaluation/runs/` v centrálním repozitáři):**

- **Varianta A (MetaGPT):** MetaGPT zapisuje spotřebu tokenů do složky `workspace/logs/` (nebo přes interní `CostManager` na konci běhu vypíše souhrn `Total tokens / Prompt tokens / Completion tokens`). Vývojář po každém milníku uloží u sebe výpis konzole a log soubor (mimo dosah agentů) a opíše součty do `intervention-log.csv`.
- **Varianta B (LangGraph):** Orchestrátor po každém kroku sčítá `response.usage_metadata["input_tokens"]` a `response.usage_metadata["output_tokens"]` a na konci běhu uloží JSON soubor s těmito údaji (mimo dosah agentů).
- **Varianta C (OpenHands):** Ve webovém rozhraní OpenHands po dokončení každého milníku klikne vývojář na export historie/trajektorie (_Export trajectory_ nebo JSON soubor v `.openhands-state/sessions/`), uloží ho mimo dosah agenta a z pole `metrics` / `token_usage` vyčte součet `prompt_tokens`, `completion_tokens` a počet kroků LLM.

## 6. Postup kontroly na konci každého milníku (Checklist)

Když agent ohlásí dokončení milníku (M2 až M3.3), vývojář provede tento přesný postup:

1. Zastaví měření času běhu agenta a uloží surový log spotřebovaných tokenů za daný běh (M22).

2. Provede v repozitáři commit stavu vygenerovaného agentem s jednotným formátem zprávy: `[AGENT][M3.1] Vygenerovana iterace 1`.
3. Ověří kvalitu výstupu podle checklistu milníku:

- U **M2**: Existuje návrh architektury, datový model pokrývá všechny entity z `openAPI.yaml` a wireframy respektují `user-stories.md`?

- U **M3.1–M3.3**: Jde aplikace sestavit a spustit přes `docker compose up`? Procházejí všechny unit testy napsané agentem (metrika M6 = 100 % zelených)? Odpovídají implementované endpointy souboru `openAPI.yaml`?

4. Rozhodne o výsledku kontroly:

- **Vše v pořádku:** Zapíše do `intervention-log.csv` událost `MILESTONE_APPROVED` a spustí další milník.
- **Nalezeny nedostatky:** Sepíše stručný a věcný výčet chyb (bez psaní konkrétního kódu), zapíše do `intervention-log.csv` událost `MILESTONE_REJECTED` (M20 +1, M21 +1) a vrátí úkol k dopracování.

## 7. Vzorový postup pro rozdělení milníku

Pokud agent například zvládl F4 (skupiny), ale opakovaně selhává při kombinaci F5 (pravidlo nezletilých) a F6 (matice oprávnění) v milníku M3.2, vývojář postupuje takto:

1. **Uložení funkčního stavu:** Provede commit dosud funkční části: `git commit -m "[AGENT][M3.2-part1] Implementace skupin F4"`.
2. **Zápis do deníku:** Zapíše do `intervention-log.csv` událost `TASK_SPLIT` (`pocita_se_m20 = 1`) s popisem rozdělení na Podúkol A (F5) a Podúkol B (F6).
3. **Podúkol A (nová čistá session – pouze F5):**

    > „Pokračuj v existujícím repozitáři (funkce F1–F4 jsou již hotové). V tomto kroku implementuj výhradně funkci **F5 (Pravidlo pro nezletilé)** podle `user-stories.md` (`US-F5.1`, `US-F5.2`) a `openAPI.yaml` (`POST /registrations`, `POST /groups`, `POST /groups/join`, `DELETE /groups/{groupId}/members/{registrationId}`). Zajisti výpočet věku k `event.startDate`, stav `awaiting_group`, `blockingReasons: ["MINOR_REQUIRES_GROUP"]` a chybový kód `LEADER_MUST_BE_ADULT`. Napiš pro F5 unit testy v `pytest` a ověř, že všechny testy v repozitáři projdou.“

4. **Podúkol B (po commitu Podúkolu A – nová čistá session – pouze F6 + UI):**
    > „V repozitáři jsou hotové funkce F1–F5. Nyní implementuj výhradně funkci **F6 (Role a oprávnění)** podle matice v `US-F6.1` a `US-F6.2` v `user-stories.md` a kontraktů v `openAPI.yaml` (`PUT /registrations/{registrationId}/roles` a filtrování kategorií `basic`, `contact`, `health`, `diet` na všech GET endpointech). Doplň i odpovídající prvky do React frontendu pro F4–F6. Napiš unit testy ověřující, že neoprávněný přístup ke kategorii vrací HTTP 403.“

## 8. Šablona Deníku zásahů

Níže je seznam sloupců, které budou definovat deník zásahů, viz `intervention-log.csv`, který obsahuje ukázkové řádky pro všechny typy událostí. Soubor používá čárku `,` jako oddělovač a pole obsahující čárku nebo uvozovky jsou uzavřena do uvozovek podle RFC 4180.

- **`timestamp`** – Datum a čas zaznamenané události.
- **`varianta`** – Identifikátor testované varianty, například `A-MetaGPT`, `B-LangGraph` nebo `C-OpenHands`.
- **`milnik`** – Milník, během kterého událost nastala (`M2`, `M3.1`, `M3.2` nebo `M3.3`).
- **`typ_udalosti`** – Typ události podle taxonomie, například `MILESTONE_START`, `MILESTONE_REJECTED` nebo `MANUAL_FIX`.
- **`pocita_se_m20`** – Indikátor, zda událost přispívá jedním bodem do metriky M20.
- **`pocita_se_m21`** – Indikátor, zda událost přispívá do metriky M21 jako zamítnutí milníku.
- **`popis_udalosti`** – Stručný popis toho, co se během události stalo.
- **`pouzity_prompt_nebo_akce`** – Použitý zásah, zadání nebo jiná lidská či systémová akce.
- **`cas_behu_min`** – Doba trvání běhu nebo části milníku v minutách.
- **`volani_llm`** – Počet volání jazykového modelu.
- **`tokeny_in`** – Počet vstupních tokenů spotřebovaných jazykovým modelem.
- **`tokeny_out`** – Počet výstupních tokenů vygenerovaných jazykovým modelem.
- **`git_commit_hash`** – Hash commitu odpovídajícího stavu repozitáře po události.

### Výpočet souhrnných metrik do závěrečné zprávy

- **M20 (Počet lidských zásahů):** Součet sloupce `pocita_se_m20` zvlášť pro každý milník (ověření hypotézy H5: ≤ 5) a celkem za celý běh (ověření hypotézy H7: porovnání MAS vs. Single Agent).

- **M21 (Míra přepracování):** Poměr počtu událostí `MILESTONE_REJECTED` (součet `pocita_se_m21`) k celkovému počtu odevzdání milníků.

- **M22 (Spotřeba zdrojů):** Součet `cas_behu_min`, `volani_llm`, `tokeny_in` a `tokeny_out` přes všechny řádky dané varianty, doplněný o počet událostí `RATE_LIMIT_PAUSE`.
