# Systémové zadání: MVP registračního systému akcí pro Junák

## 1. Cíl a závazné vstupní dokumenty

Tvým úkolem je vytvořit funkční, bezpečné a převzatelné MVP registračního systému akcí pro organizaci Junák – český skaut, z. s.

Závazným **zdrojem pravdy** jsou obě přiložené specifikace:

1. `user-stories.md` – definuje slovníček pojmů, role, uživatelské příběhy, akceptační kritéria a nefunkční požadavky.
2. `openAPI.yaml` – definuje závazný kontrakt REST API, včetně přesných URL cest, JSON schémat, formátu chyb a testovacích endpointů. Implementace musí přesně dodržovat tento kontrakt (datové typy, stavové kódy, chybové kódy `ErrorCode`).

## 2. Přesný rozsah MVP

**Implementuj:** Všechny příběhy s prioritou **Must** (22 příběhů) a **Should** (7 příběhů) v rozsahu funkcí **F1 až F9** dle `user-stories.md` a **100 % endpointů** definovaných v `openAPI.yaml` (včetně testovacích endpointů `/health`, `/test/reset`, `/test/login-as`, `/test/bulk-users` při `APP_ENV=test` a fixního UUID výchozí akce `11111111-1111-4111-8111-111111111111`).

**Neimplementuj:** Volitelné příběhy s prioritou **Could** (`US-X.1` a `US-X.2`) ani položky uvedené v sekci „Mimo rozsah MVP“ v `user-stories.md`.

## 3. Technologický stack a infrastruktura

Dodržuj přesně tento technologický stack a strukturu repozitáře:

- **Backend (`/backend`):** Python 3.11+, FastAPI, SQLAlchemy (nebo SQLModel), Pydantic v2, Alembic pro migrace. API musí běžet na adrese `http://localhost:8080/api/v1`.
- **Databáze:** PostgreSQL 16+ (kvůli nutnosti atomického transakčního zamykání při souběžném přihlašování na programy).
- **Frontend (`/frontend`):** React 18+, TypeScript, Vite, TailwindCSS. Celé uživatelské rozhraní musí být v **češtině** (`NFR-7`), responzivní pro mobil, tablet i desktop (`NFR-3`) a splňovat zásady přístupnosti WCAG úrovně A/AA (popisky formulářových polí `<label>`, sémantické HTML, ovládání klávesnicí, dostatečný kontrast dle `NFR-4`).
- **Spuštění jedním příkazem (`NFR-8`):** V kořeni repozitáře vytvoř `docker-compose.yml`, který přes `docker compose up --build` spustí databázi, backend (port `8080`) i frontend (port `3000`) včetně automatického nahrání ukázkových dat.

## 4. Požadavky na kvalitu kódu, testy a dokumentaci

- **Testy a TDD:** Každé akceptační kritérium (`US-Fx.y`) a API endpoint musí mít automatizované testy v `pytest` (unit i integrační testy), které běží neinteraktivně a končí návratovým kódem 0. Cílové pokrytí backendu je alespoň **70 % řádků** a **60 % větví** (`pytest --cov`).
- **Kvalita kódu:** Udržuj nízkou cyklomatickou složitost funkcí (průměr ≤ 10), minimální duplicity (< 5 %) a čistou typovou i statickou kontrolu (`ruff` pro Python, `tsc` pro TypeScript).
- **Bezpečnost:** Kontrola oprávnění RBAC a pravidel pro nezletilé vždy na serveru, ochrana proti SQL injection / XSS, žádné citlivé klíče ani hodnoty zdravotních údajů v logách.
- **Dokumentační výstupy MVP (v `/docs`):**
    - `docs/ARCHITECTURE.md` – přehled architektury a datového modelu,
    - `docs/ADR.md` – klíčová architektonická a bezpečnostní rozhodnutí (autentizace, transakční zamykání kapacit, RBAC),
    - `docs/RTM.md` – matice trasovatelnosti mapující `US-F1.1`–`US-F9.2` na backend, frontend a testy,
    - `docs/README.md` – návod na lokální spuštění (`docker compose up`), proměnné prostředí, testovací role a spuštění testů.
