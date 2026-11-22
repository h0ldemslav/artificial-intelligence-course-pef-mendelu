# Systémové zadání: MVP registračního systému akcí pro Junák

## 1. Cíl a závazné vstupní dokumenty

Tvým úkolem je navrhnout, otestovat a implementovat funkční, bezpečné a převzatelné MVP registračního systému akcí pro organizaci Junák – český skaut, z. s.

Před jakýmkoli návrhem nebo psaním kódu si **pečlivě přečti a analyzuj obě přiložené specifikace v adresáři repozitáře**:

1. `user-stories.md` – definuje slovníček pojmů, role, uživatelské příběhy, akceptační kritéria a nefunkční požadavky.
2. `openAPI.yaml` – definuje závazný kontrakt REST API, včetně přesných URL cest, JSON schémat, formátu chyb, testovacích endpointů atd. Implementace musí přesně dodržovat tento kontrakt (datové typy, stavové kódy atd.)

Oba dokumenty jsou závazným **zdrojem pravdy**.

## 2. Přesný rozsah implementace

**Implementuj:** Všechny příběhy s prioritou **Must** (22 příběhů) a **Should** (7 příběhů) v rozsahu funkcí **F1 až F9** dle `user-stories.md` a **100 % endpointů** definovaných v `openAPI.yaml`.

**Neimplementuj:** Volitelné příběhy s prioritou **Could** (`US-X.1` a `US-X.2`) ani položky uvedené v sekci „Mimo rozsah MVP“ v `user-stories.md`.

## 3. Technologický stack a infrastruktura

Dodržuj přesně tento technologický stack a strukturu repozitáře:

- **Backend (`/backend`):** Python 3.11+, FastAPI, SQLAlchemy (nebo SQLModel), Pydantic v2, Alembic pro migrace. API musí běžet na adrese `http://localhost:8080/api/v1`.
- **Databáze:** PostgreSQL 16+ (kvůli nutnosti atomického transakčního zamykání při souběžném přihlašování na programy).
- **Frontend (`/frontend`):** React 18+, TypeScript, Vite, TailwindCSS. Celé uživatelské rozhraní musí být v **češtině** (`NFR-7`), responzivní pro mobil, tablet i desktop (`NFR-3`) a splňovat zásady přístupnosti WCAG úrovně A/AA (popisky formulářových polí `<label>`, sémantické HTML, ovládání klávesnicí, dostatečný kontrast dle `NFR-4`).
- **Spuštění jedním příkazem (`NFR-8`):** V kořeni repozitáře vytvoř `docker-compose.yml`, který přes `docker compose up --build` spustí databázi, backend (port `8080`) i frontend (port `3000`) včetně automatického nahrání ukázkových dat.

## 4. Metodika vývoje

Při práci dodržuj cyklus vývoje softwaru (SDLC) a testováním řízený vývoj (TDD):

### Fáze 1: Analýza a architektonický návrh (Design-First)

- Navrhni relační databázové schéma pokrývající všechny entity a omezení z `user-stories.md` a `openAPI.yaml`.
- Zaznamenej klíčová architektonická a bezpečnostní rozhodnutí do souboru `docs/ADR.md` (Architecture Decision Records – např. způsob autentizace, transakční zamykání kapacit, řízení přístupu RBAC).
- Architektonický popis systému ulož do `docs/ARCHITECTURE.md`.
- Navrhi uživatelské rozhraní pro všechny klíčové obrazovky. U každé obrazovky uveď:
    - jednoduchý ASCII náčrt rozvržení (wireframe),
    - seznam komponent a jejich hierarchii,
    - zobrazovaná data a uživatelské interakce,
    - stavy komponent a obrazovky (prázdná, načítání, chyba, vyplněná, `disabled`, `hover`),
    - responzivní chování (mobil vs. desktop).

### Fáze 2: Iterativní implementace metodou TDD (Red → Green → Refactor)

Každou funkci implementuj v přísném cyklu TDD:

1. **RED:** Pro každé akceptační kritérium (`US-Fx.y`) a API endpoint z `openAPI.yaml` napiš nejprve automatizované testy v `pytest` (unit i integrační testy proti FastAPI a PostgreSQL). Ověř, že selhávají.
2. **GREEN:** Napiš funkční kód v `/backend` a `/frontend`, dokud všechny testy neprojdou.
3. **REFACTOR:** Udržuj nízkou cyklomatickou složitost funkcí (průměr ≤ 10), odstraň duplicity kódu (< 5 %) a dodržuj typovou kontrolu a linter (`ruff`). Výsledkem je čistý a modulární kód.
4. **Spustitelnost v CI:** Všechny testy musí běžet neinteraktivně a končit návratovým kódem 0. Pokrytí backendu testy musí dosáhnout alespoň **70 % řádků** a **60 % větví** (`pytest --cov`).

### Fáze 3: Trasovatelnost požadavků (RTM) a dokumentace

- Vytvoř a průběžně aktualizuj **Matici trasovatelnosti požadavků** v souboru `docs/RTM.md` (tabulka mapující každé ID příběhu `US-F1.1` až `US-F9.2` -> konkrétní endpoint a soubor v `/backend` -> komponentu v `/frontend` -> konkrétní testovací soubor a název test funkce). Každý příběh `Must` i `Should` musí mít alespoň jeden test.
- Udržuj aktuální `docs/README.md` s přesným návodem na lokální spuštění (`docker compose up`), popisem proměnných prostředí, přihlašovacími údaji/postupem pro testovací role a popisem spuštění testů.

## 5. Disciplína milníků

Pracuj striktně v rozsahu aktuálně zadaného milníku (`M2`, `M3.1`, `M3.2` nebo `M3.3`). Pokud jsi ve fázi `M2` (Návrh), nevytvářej aplikační kód, ale pouze návrhové dokumenty (`docs/ARCHITECTURE.md`, `docs/ADR.md`, návrh DB schématu, strukturu obrazovek a počáteční kostru `docs/RTM.md`).
