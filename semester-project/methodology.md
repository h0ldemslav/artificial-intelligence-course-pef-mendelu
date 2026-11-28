Níže je jednotná metodika pro všechny tři srovnávané varianty vycházející z [project-proposal.md](./project-proposal.md). Dokument je navržen tak, aby zajistil férové srovnání mezi Variantou A (MetaGPT), Variantou B (LangGraph) a Variantou C (OpenHands), umožnil objektivně vyhodnotit výzkumné otázky i hypotézy a zabránil zkreslení lidských zásahů.

## 1. Výchozí podmínky před spuštěním (Zmrazení vstupů)

Aby bylo možné výsledky všech tří variant objektivně porovnat, musí každá varianta před prvním spuštěním splnit následující podmínky:

1. **Identické vstupní podklady:** Všechny tři systémy vycházejí ze stejné sady specifikací: `user-stories.md` (odvozené uživatelské příběhy a akceptační kritéria pro F1–F9 bez důvěrného zadání Junáka), `openAPI.yaml` (závazný kontrakt REST API) a `initial-prompt.md` (jednotné zadání tech stacku, testovacích kotev a NFR). Po zahájení experimentu se tyto podklady nemění.
2. **Jednotná politika jazykových modelů (free-tier Gemini API):** Modely se konfigurují přes Google AI Studio API se stejnou teplotou (`temperature=0.2`):
    - **Plánování / uvažování / QA kontrola:** `gemini-3.8-flash` (pokud by při startu narážel na příliš přísné free-tier limity, přechází se jednotně na `gemini-3.5-flash-lite` a změna se zaprotokoluje).
    - **Generování kódu (worker / implementace):** `gemini-3.5-flash-lite`.
    - Pro zamezení burstům RPM se používá rate-limiting a exponenciální backoff při `429 RESOURCE_EXHAUSTED`.
3. **Přesný rozsah implementace:** Všechny tři varianty implementují 100 % příběhů s prioritou **Must** (22 příběhů) a **Should** (7 příběhů) dle `user-stories.md`, což odpovídá všem endpointům v `openAPI.yaml`. Volitelné příběhy **Could** (`US-X.1`, `US-X.2`) se neimplementují.
4. **Povinný tech stack a technické kotvy pro automatické testy:**
    - **Backend:** Python 3.11+ (FastAPI, SQLAlchemy/SQLModel, Pydantic v2) vystavený na `http://localhost:8080/api/v1`.
    - **Frontend:** React 18+ (Vite, TypeScript, TailwindCSS) s uživatelským rozhraním v češtině (NFR-7).
    - **Databáze:** PostgreSQL 16+ (atomická transakční kontrola kapacity při souběžné zátěži v `US-F7.4`, metriky M11–M14).
    - **Spuštění a testovací endpointy:** Celý systém musí jít spustit jedním příkazem (`docker compose up --build` dle NFR-8). Při `APP_ENV=test` musí být dostupné všechny endpointy ze sekce `test-support` (`/health`, `/test/reset`, `/test/login-as`, `/test/bulk-users`) včetně fixního UUID výchozí akce `11111111-1111-4111-8111-111111111111`.
5. **Čistý repozitář:** Každá varianta běží ve svém izolovaném repozitáři se stejnou výchozí strukturou (`/backend`, `/frontend`, `/docs`, `.github/workflows/ci.yml`).
6. **Aktivní měření spotřeby (M22):** Před prvním dotazem na LLM musí být zapnuté logování počtu volání modelu, vstupních a výstupních tokenů a času běhu.

## 2. Společná struktura přírůstků a kontrolních bodů (Milníky / Vertikální řezy)

Hypotéza H5 v project-proposalu stanovuje hranici **nejvýše 5 lidských zásahů na milník / kontrolovaný přírůstek** (metrika M20). Každá varianta postupuje po logicky oddělených kontrolovaných krocích zakončených lidskou revizí (HITL bránou), které dohromady pokrývají celé MVP (F1–F9):

- **Fáze plánování (`PLAN`):** Dekompozice `user-stories.md` a `openAPI.yaml` do architektury / backlogu funkčních celků a schválení plánu člověkem před zahájením implementace.
- **Implementační přírůstky (`SLICE-1` .. `SLICE-N` nebo ekvivalentní milníky):** Každý přírůstek tvoří end-to-end celek (backend + frontend + automatizované testy) pokrývající část funkcí F1–F9:
    - přihlášení přes mock skautIS a ochrana relace (F1), správa akcí (US-F8.1) a testovací podpora,
    - registrace jednotlivce, validace a unikátní identifikační kód (F2, F3),
    - skupiny, pravidlo pro nezletilé a matice RBAC oprávnění (F4, F5, F6),
    - programy se souběžností, administrace, CSV export a auditní log (F7, US-F8.2–F8.4, F9).

Díky tomu lze porovnávat jak varianty pracující v pevných milnících (Varianta A / C), tak hierarchickou orchestraci po vertikálních řezech (Varianta B).

## 3. Specifika ovládání: MAS (Varianty A, B) vs. Single Agent (Varianta C)

Aby se ze žádné varianty nestalo interaktivní párové programování s člověkem, platí pro řízení běhu tato pravidla:

- **Varianta A (MetaGPT):** Multiagentní tým běží autonomně uvnitř zadaného kroku/fáze se svými předdefinovanými rolemi. Člověk nezasahuje, dokud agentní tým nepředloží výstup ke kontrole nebo se nezastaví chybou.
- **Varianta B (LangGraph – Hierarchický Orchestrator-Workers):** Orchestrátor vede běh v jediném stavovém `StateGraph` s perzistencí v `SqliteSaver`:
    1. `team_lead_plan` rozbije `user-stories.md`, `openAPI.yaml` a `initial-prompt.md` do 3–5 vertikálních řezů (`backlog.json`), poté se zastaví na `hitl_plan_review`.
    2. `team_lead_dispatch` vybírá další `pending` řez podle priority a deleguje jej izolovanému `fullstack_worker` (omezenému na `allowed_paths` daného řezu).
    3. `local_test_runner` deterministicky spouští testy (max. 3 pokusy o opravu), následně `team_lead_handoff_to_qa` předá změny nezávislému `qa_reviewer` (`team_lead_route_qa`, max. `MAX_QA_CYCLES=3`).
    4. `team_lead_report` sestaví zprávu pro člověka a pozastaví graf v `hitl_browser_review`. Člověk komunikuje **výhradně s Team Leadem** (`approve`, `feedback`, nebo `manual_override`).
- **Varianta C (OpenHands – Single Agent):** Delegování na subagenty musí být vypnuto. Vývojář nezadává drobné kroky v chatu: zadá souhrnný úkol přírůstku (včetně napsání a spuštění testů) a nechá agenta pracovat autonomně až do ohlášení výsledku nebo zaseknutí. Každá dodatečná naváděcí zpráva člověka se započítává jako zásah.

## 4. Pravidla pro lidské zásahy a taxonomie událostí (Metriky M20 a M21)

Člověk vystupuje výhradně jako kontrolor na HITL branách / kontrolních bodech a sám produkční kód nepíše (kromě nouzového `MANUAL_FIX`). Každou událost zapisujeme do `intervention-log.csv`:

### A. Běžný průchod (Nepočítá se jako zásah, M20 +0)

- **`MILESTONE_START`:** Zahájení fáze plánování nebo implementačního přírůstku (`PLAN`, `SLICE-1`..`SLICE-N` / milník).
- **`MILESTONE_APPROVED`:** Člověk ověří výstup v prohlížeči/testech a na kontrolní bráně jej schválí (`approve` v HITL bráně).
- **`RATE_LIMIT_PAUSE`:** Pád nebo pozastavení běhu čistě kvůli limitu Gemini API (`429 RESOURCE_EXHAUSTED` / denní RPD kvóta) nebo síťové chybě. Po obnovení kvóty se běh obnoví z checkpointu beze změny zadání. Zapíše se jen ztracený čas, nikoli zásah (M20 +0).

### B. Započítávaný lidský zásah (M20 +1, cíl ≤ 5 na přírůstek/milník dle H5)

- **`INTERVENTION_NUDGE` (M20 +1):** Agent se zacyklil mimo standardní bránu a člověk musí dodat upřesňující/naváděcí zprávu.
- **`MILESTONE_REJECTED` (M20 +1, M21 +1):** Člověk na kontrolní bráně výstup zamítne a pošle zpětnou vazbu k opravě (v LangGraph volba `feedback` v `hitl_plan_review` nebo `hitl_browser_review`).
- **`MANUAL_FIX` (M20 +1):** Agent nedokáže vyřešit blokující chybu ani po korekcích a člověk zasáhne ručně (v LangGraph volba `manual_override`, která automaticky inkrementuje `human_intervention_score`, případně ruční Git commit s prefixem `[HUMAN-FIX]`).
- **`TASK_SPLIT` (M20 +1, manuální záchrana / fallback):** Pokud je některý přírůstek nebo milník pro daný nástroj stále příliš velký a agent jej nezvládá ani po korekcích, člověk ručně rozdělí zbývající rozsah na menší podúkoly (viz sekce 7).

### Pravidla pro formulaci zpětné vazby při zásahu

Vývojář **nesmí agentovi psát konkrétní kód ani prozrazovat skryté akceptační testy**. Zpětná vazba se vždy odkazuje pouze na `user-stories.md`, `openAPI.yaml`, chování v prohlížeči nebo chybovou hlášku z testů:

- **Správný příklad (`MILESTONE_REJECTED`):**
    > „Výstup řezu zamítám. Při kontrole podle `openAPI.yaml` a `user-stories.md` byly zjištěny dva nedostatky: 1) `GET /api/v1/events/{eventId}/registrations/{registrationId}?categories=health` vrací pro roli `program_team` status 200 místo 403 (`US-F6.1`). 2) Po odebrání nezletilého člena ze skupiny (`DELETE /groups/{groupId}/members/{registrationId}`) zůstává status `completed` místo `awaiting_group` (`US-F5.1`).“
- **Špatný příklad (zakázáno):**
    > „V `backend/routers/registrations.py` na řádku 84 přidej `if 'health' in categories: raise HTTPException(403)`...“

## 5. Kde a jak logovat spotřebu tokenů (Metrika M22)

Každá varianta udržuje odděleně od kódu generovaného agenty dvě evidence:

1. **Deník událostí a zásahů (`intervention-log.csv`):** Záznam se doplňuje po každém dokončeném kroku / HITL bráně / pauze na kvótu. Po dokončení MVP se soubory ze všech tří variant uloží do centrálního repozitáře do `evaluation/logs/`.
2. **Surové logy spotřeby (`evaluation/runs/` v centrálním repozitáři):**
    - **Varianta A (MetaGPT):** Logy z `workspace/logs/` / `CostManager` (`Total tokens`, `Prompt tokens`, `Completion tokens`).
    - **Varianta B (LangGraph):** Orchestrátor průběžně sčítá `total_llm_calls`, `total_input_tokens`, `total_output_tokens` a dobu běhu ze všech volání LLM (včetně retry a opravných cyklů) a ukládá souhrn po každé HITL bráně do `orchestrator/runs/<thread_id>_metrics.json`.
    - **Varianta C (OpenHands):** Export trajektorie z UI nebo `.openhands-state/sessions/` (`metrics` / `token_usage`).

## 6. Postup kontroly na konci každého přírůstku

Po zastavení na kontrolní bráně (dokončení plánu, vertikálního řezu nebo milníku) vývojář provede:

1. Zaznamená dobu běhu a kumulativní spotřebu tokenů / volání LLM (M22).
2. Vytvoří Git commit stavu vygenerovaného agenty, např. `[AGENT][SLICE-1] Implementace prihlaseni a akci`.
3. Ověří výstup:
    - **Plán (`PLAN`):** Pokrývá návrh / `backlog.json` všechny požadavky F1–F9 a `openAPI.yaml`?
    - **Implementační přírůstek (`SLICE-*` / milník):** Jde aplikace spustit přes `docker compose up --build`? Procházejí všechny testy agentů (M6 = 100 % zelených)? Odpovídají implementované endpointy `openAPI.yaml` a UI v češtině `user-stories.md`?
4. Zaznamená rozhodnutí do `intervention-log.csv`:
    - **Schváleno:** Zapíše `MILESTONE_APPROVED` (`M20=0`, `M21=0`).
    - **Vráceno s výhradami:** Zapíše `MILESTONE_REJECTED` (`M20=1`, `M21=1`).
    - **Ruční oprava:** Zapíše `MANUAL_FIX` (`M20=1`, `M21=0`) a ruční commit označí `[HUMAN-FIX]`.

## 7. Manuální záchrana: Rozdělení úkolu (`TASK_SPLIT` fallback)

Ačkoliv v hierarchické orchestraci (Varianta B) rozděluje zadání na řezy již Team Lead při plánování, v situaci kdy jakákoliv ze tří variant (A, B nebo C) opakovaně selhává na příliš velkém milníku nebo řezu:

1. **Uložení funkčního stavu:** Commit dosud funkční části (`git commit -m "[AGENT][PARTIAL] ..."`).
2. **Zápis do deníku:** Do `intervention-log.csv` se zapíše událost `TASK_SPLIT` (`pocita_se_m20 = 1`) s popisem rozdělení.
3. **Zúžené zadání:** Zbytek rozsahu se rozdělí na menší podúkoly (u Variant A/C v nové session; u Varianty B úpravou/rozdělením zbývajícího `pending` řezu v `backlog.json` nebo přeplánováním na bráně `hitl_plan_review`), přičemž zadání vždy odkazuje pouze na `user-stories.md` a `openAPI.yaml`.

## 8. Šablona Deníku zásahů (`intervention-log.csv`)

Soubor `intervention-log.csv` používá oddělovač `,` (RFC 4180) a následující sloupce:

- **`timestamp`** – Datum a čas události (`YYYY-MM-DD HH:MM`).
- **`varianta`** – Identifikátor varianty (`A-MetaGPT`, `B-LangGraph`, `C-OpenHands`).
- **`milnik`** – Fáze, vertikální řez nebo milník (`PLAN`, `SLICE-1`..`SLICE-N`, případně `M1`..`M*`).
- **`typ_udalosti`** – `MILESTONE_START`, `MILESTONE_APPROVED`, `MILESTONE_REJECTED`, `INTERVENTION_NUDGE`, `MANUAL_FIX`, `TASK_SPLIT`, `RATE_LIMIT_PAUSE`.
- **`pocita_se_m20`** – `1` pokud se událost počítá do M20, jinak `0`.
- **`pocita_se_m21`** – `1` pokud jde o zamítnutí na kontrolní bráně (`MILESTONE_REJECTED`), jinak `0`.
- **`popis_udalosti`** – Stručný věcný popis situace.
- **`pouzity_prompt_nebo_akce`** – Zvolená akce (`approve` / `feedback` / `manual_override`) nebo souhrn zprávy.
- **`cas_behu_min`** – Trvání běhu v minutách.
- **`volani_llm`** – Počet volání LLM za daný krok (nebo přírůstek od posledního záznamu).
- **`tokeny_in`** – Počet vstupních tokenů.
- **`tokeny_out`** – Počet výstupních tokenů.
- **`git_commit_hash`** – Hash Git commitu po dané události.

### Výpočet souhrnných metrik do závěrečné zprávy

- **M20 (Počet lidských zásahů):** Součet `pocita_se_m20` pro jednotlivé kontrolované přírůstky/milníky (ověření hypotézy H5: ≤ 5) i celkem za variantu (ověření H7).
- **M21 (Míra přepracování):** Poměr počtu `MILESTONE_REJECTED` (součet `pocita_se_m21`) k celkovému počtu odevzdaných kontrolních bran (`MILESTONE_APPROVED` + `MILESTONE_REJECTED`).
- **M22 (Spotřeba zdrojů):** Součet `cas_behu_min`, `volani_llm`, `tokeny_in` a `tokeny_out` přes všechny řádky varianty, doplněný o počet událostí `RATE_LIMIT_PAUSE`.
