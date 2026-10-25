# Project Proposal: Multiagentní systém pro vývoj registračního systému akcí Junáka

**Tým:** Anna Šmikmátorová, Patrik Michl, Erik Praunsperger, Daniil Astapenko

**Uživatel / partner:** Junák – český skaut, z. s.

**Typ projektu:** semestrální týmový projekt

**Výstup:** MVP registračního systému akcí vytvořené multiagentním systémem + vyhodnocení postupu

---

## 1. Shrnutí

Junák – český skaut dnes pro registrace na velké akce používá dva různé systémy a každá akce si musí vybrat jeden z nich. Žádný nepokrývá všechny potřeby, takže pořadatelé vždy dělají kompromis. Nad jedním z obou systémů navíc organizace nemá kontrolu. Junák proto připravuje výběrové řízení na nový registrační systém.

V našem projektu ověříme, zda multiagentní systém (MAS) postavený na volně dostupných nástrojích dokáže z takto komplexního, reálného zadání vytvořit funkční MVP. Člověk v tomto procesu jen kontroluje a schvaluje milníky. Cílem není produkční systém. Chceme **změřit, jak dobře MAS zvládne komplikované zadání**, a vytvořit **převzatelný základ**, na kterém lze dál stavět.

---

## 2. Začínáme u uživatele

### 2.1 Kdo má daný problém?

**Junák – český skaut**, největší výchovná organizace pro děti a mládež v Česku, konkrétně:

- **pořadatelské týmy akcí**, které spravují přihlášky, skupiny, programy a platby,
- **vedoucí skupin (oddílů)**, kteří zodpovídají za své nezletilé členy,
- **účastníci akcí**, často nezletilí, a jejich rodiče,
- **organizace jako celek**, která odpovídá za ochranu osobních údajů svých členů.

### 2.2 S čím se potýká?

- **Nucená volba mezi dvěma systémy.** Každá akce si musí vybrat jeden ze dvou systémů. Jeden umí registrovat jednotlivce a přihlašovat je na programy. Druhý umí registrovat skupiny. Akce, která potřebuje obojí, musí část svých potřeb obětovat nebo je řešit mimo systém (tabulky, formuláře, ruční evidence).
- **Kompromis u skupin a nezletilých.** U členů mladších 18 let musí být jednoznačně dohledatelné, kdo je jejich zodpovědný vedoucí. Pokud akce zvolí systém pro jednotlivce kvůli programům, ztrácí práci se skupinami, a tím i tuto vazbu v systému.
- **Šedá zóna v datech.** Systém pro skupinové registrace není pod správou Junáka. Organizace neví, jak systém s daty pracuje ani kde je ukládá. Každá akce, která potřebuje skupiny, tak předává osobní a často i zdravotní údaje nezletilých do prostředí, které organizace nekontroluje.
- **Nárazová zátěž.** Při otevření registrace nebo výběru programů na velkých akcích se během několika minut přihlásí stovky až tisíce lidí. Kapacity programů se přitom nesmí přečerpat.

### 2.3 Proč na tom záleží?

- **Bezpečnost dětí:** na akci musí být u každého nezletilého jasné, kdo za něj zodpovídá.
- **Ochrana osobních údajů (GDPR):** organizace musí mít data svých členů pod kontrolou. Systém mimo správu Junáka je právní i reputační riziko.
- **Čas dobrovolníků:** pořadatelé jsou dobrovolníci. Obcházení chybějících funkcí zvoleného systému (vlastní tabulky, další formuláře, ruční dohledávání) jim bere čas, který by mohli věnovat programu.
- **Cena vývoje:** neziskové organizace mají omezený rozpočet. Pokud MAS dokáže levně vytvořit kvalitní základ nebo prototyp, může zlevnit a zpřesnit budoucí vývoj (např. ujasnit požadavky ještě před zadáním zakázky).

### 2.4 Jaké je nejmenší řešení, které můžeme otestovat?

Řešení testujeme ve dvou krocích:

1. **Pilot (spike):** všechny tři navržené varianty MAS (kap. 6) necháme vytvořit tutéž malou funkci, tedy registraci jednotlivce s připojením do skupiny. Podle zjednodušené sady metrik vybereme variantu pro celé MVP.
2. **MVP:** vybraná varianta vytvoří MVP v rozsahu z kap. 5, které nabízí registraci jednotlivců, skupiny i programy v **jednom** systému pod správou Junáka, takže akce už nemusí volit mezi dvěma systémy.

### 2.5 Jaké důkazy nám řeknou, že to funguje?

- MVP projde **akceptačními testy**, které tým napíše nezávisle na agentech (kap. 8.1).
- Systém pod souběžnou zátěží **nepřečerpá kapacitu** ani nevytvoří duplicitní registrace (kap. 8.3).
- Žádný nezletilý účastník nedokončí registraci bez přiřazení k vedoucímu.
- Kód splní stanovené prahy kvality a pokrytí testy (kap. 8.2).
- UI obstojí v hodnocení podle návrhových guidelines a v uživatelském testu se skauty (kap. 8.4).
- Junák na ukázce MVP potvrdí, že řešení míří správným směrem (kap. 8.6).
- Člověk zvenku dokáže projekt podle dokumentace spustit a pokračovat v něm (kap. 8.5).

---

## 3. Project pitch: proč si iniciativa zaslouží podporu

Generativní AI slibuje, že zlevní a zrychlí vývoj software. Většina ukázek ale stojí na jednoduchých, umělých zadáních. **My testujeme MAS na reálném, komplexním zadání** od skutečné organizace. To zadání obsahuje role a oprávnění, citlivá data nezletilých, souběžnou zátěž i integraci s externím systémem.

Projekt přinese:

- **měřitelnou odpověď** na otázku, kolik z reálného zadání zvládne MAS s minimálním lidským zásahem a kde selhává,
- **srovnání tří volně dostupných přístupů** k MAS, použitelné i pro jiné neziskové organizace bez rozpočtu na vývoj,
- **převzatelný základ registračního systému** s dokumentací, testy a záznamem rozhodnutí agentů,
- **metodiku hodnocení** (metriky a skripty), kterou lze znovu použít na další projekty.

## 4. Product pitch: proč by systém uživatel potřeboval a používal

> **Jeden registrační systém pod správou Junáka, který zvládne jednotlivce, skupiny i programy, takže akce už nemusí vybírat mezi dvěma systémy a dělat kompromisy.**

- **Pro pořadatele:** nemusí volit systém podle toho, kterou funkci obětují. Mají jeden přehled všech osob na akci, filtry, exporty a jistotu, že programy nepřetečou.
- **Pro vedoucí skupin:** vidí své členy na jednom místě a mají za ně jasnou odpovědnost.
- **Pro účastníky:** jednoduchá registrace a výběr programů na mobilu, včetně přehledu vlastního harmonogramu.
- **Pro organizaci:** data zůstávají pod její kontrolou, přístup k citlivým údajům je řízený podle rolí a lze ho dohledat.

---

## 5. Rozsah MVP

Kompletní zadání je rozsáhlé. Po konzultaci s vyučujícím se zaměřujeme na MVP, které řeší jádro problému: **jednotlivci, skupiny a programy v jednom systému**. To jsou přesně ty funkce, mezi kterými dnes akce musí volit.

### 5.1 V rozsahu MVP

| # | Funkce | Klíčová akceptační kritéria |
|---|--------|------------------------------|
| F1 | **Uživatelský účet a přihlášení** | přihlášení e-mailem; přihlášení přes skautIS jen jako **simulace (mock)** s předvyplněním údajů |
| F2 | **Registrace jednotlivce na akci** | registrační formulář s kategoriemi údajů (základní, kontaktní, zdravotní, stravovací omezení), validace, povinná pole |
| F3 | **Unikátní identifikační kód** | náhodně generovaný, neodvozený od pořadí v databázi, viditelný v profilu |
| F4 | **Skupiny a vedoucí** | vedoucí založí skupinu; účastník se připojí zadáním kódu skupiny; vedoucí vidí a spravuje členy skupiny |
| F5 | **Pravidlo pro nezletilé** | účastník mladší 18 let **nemůže dokončit registraci bez přiřazení do skupiny s plnoletým vedoucím**; vedoucí musí být plnoletý |
| F6 | **Role a oprávnění** | předdefinované role (účastník, vedoucí skupiny, lektor, zdravotník, pořadatel, administrátor); přístup k datům podle kategorií (např. zdravotní údaje vidí jen zdravotník a pořadatel) |
| F7 | **Programy s kapacitou** | vytvoření programu (název, čas, místo, kapacita); přihlášení s kontrolou kapacity a časové kolize; **žádné přečerpání kapacity při souběžném přihlašování** |
| F8 | **Administrace akce** | přehled účastníků a skupin, filtrování, vyhledávání; export CSV s výběrem sloupců |
| F9 | **Historie operací (základ)** | log změn registrací, rolí a exportů (kdo, kdy, co) |

**Volitelně, pokud zbude čas:** výzva k platbě s variabilním symbolem a QR kódem (bez napojení na banku), e-mailové notifikace přes testovací službu.

### 5.2 Mimo rozsah MVP

Reálné napojení na skautIS a Fio banku, párování plateb a vratky, stravování, merch, podakce, převody registrací, vlastní otázky ve formuláři, vizuální přizpůsobení akcí, plný zátěžový test na 2 000 uživatelů v produkčním prostředí, nasazení do cloudu Junáka.

### 5.3 Důvěrnost zadání

Kompletní zadání Junáka není veřejné, proto **není součástí veřejného repozitáře**. Repozitář obsahuje jen z něj odvozené uživatelské příběhy a akceptační kritéria MVP. Volné úrovně některých LLM služeb mohou vstupní data využívat k trénování. Agentům proto předáváme **jen odvozené, neutrální uživatelské příběhy**, nikoli původní dokument. Případně použijeme lokální modely (viz kap. 6).

---

## 6. Navrhované varianty multiagentního systému

Všechny varianty jsou postavené na **volně dostupných (open-source) nástrojích** a **bezplatných LLM**. Bezplatné LLM znamenají lokální modely přes Ollama nebo volné úrovně API, např. Google Gemini, GitHub Models nebo OpenRouter. Limity volných úrovní se často mění, proto je ověříme na začátku projektu.

Ve všech variantách je **člověk pouze kontrolor milníků**. Schvaluje výstup každé fáze (požadavky → návrh → implementace → testy), ale sám kód nepíše. Každý zásah evidujeme jako metriku.

### Varianta A: Hotový „softwarový tým“ (MetaGPT nebo ChatDev)

Open-source frameworky, které simulují softwarovou firmu s předdefinovanými rolemi (produktový manažer, architekt, programátor, tester).

- **+** rychlý start, role i proces jsou připravené, výstupem jsou i dokumenty (PRD, návrh architektury)
- **−** méně kontroly nad procesem, horší zvládání velkých projektů a iterací, výstup může být spíš demo než udržovatelný kód

### Varianta B: Vlastní orchestrace (CrewAI nebo LangGraph)

Vlastní MAS, ve kterém sami definujeme agenty (analytik, architekt, backend, frontend, tester, reviewer), jejich nástroje a tok práce, včetně bodů pro schválení člověkem.

- **+** plná kontrola nad rolemi a procesem, snadno se do něj vloží kontrolní body a měření
- **−** nejvíc vlastní práce na začátku; kvalitu výsledku ovlivňuje i kvalita našeho návrhu orchestrace

### Varianta C: Agentní vývojové prostředí (např. OpenHands)

Open-source agentní platforma, ve které agent pracuje přímo v repozitáři: spouští kód, testy a příkazy, přičemž dílčí úkoly může delegovat dalším agentům.

- **+** agent si vlastní výstup ověřuje spuštěním testů, pracuje s reálným repozitářem a gitem
- **−** spíše jeden silný agent než pestrý tým rolí; spotřebuje víc volání modelu a rychle narazí na limity volných úrovní

**Výběr:** o variantě rozhodne pilot (kap. 2.4) podle těchto metrik: podíl splněných akceptačních kritérií pilotní funkce, počet lidských zásahů, úspěšnost testů a spotřeba volání modelu.

---

## 7. Výzkumná otázka a hypotézy

### 7.1 Výzkumná otázka

> **Do jaké míry dokáže multiagentní systém postavený na volně dostupných nástrojích, s člověkem pouze v roli kontrolora milníků, vytvořit z reálného komplexního zadání MVP registračního systému, které je funkční, chrání data a je převzatelné k dalšímu vývoji?**

Dílčí otázky:

- **VO1:** Která ze tří variant MAS je pro tento typ zadání nejvhodnější?
- **VO2:** Ve kterých typech požadavků MAS selhává nejčastěji (např. souběžnost, oprávnění, business pravidla)?
- **VO3:** Jak velký lidský zásah je k dosažení funkčního MVP potřeba?

### 7.2 Hypotézy

Ke každé hypotéze uvádíme nulovou (H0) a alternativní (H1) hypotézu. Prahy vycházejí z běžných doporučení pro kvalitu kódu a z požadavků zadání.

| # | H0 (nulová) | H1 (alternativní) | Metrika |
|---|-------------|-------------------|---------|
| **H1** | MAS splní **méně než 80 %** akceptačních kritérií MVP. | MAS splní **alespoň 80 %** akceptačních kritérií MVP. | M1 |
| **H2** | Při souběžném přihlašování dojde **alespoň k jednomu** přečerpání kapacity nebo duplicitní registraci. | Při souběžném přihlašování dojde k **nulovému** přečerpání kapacity a duplicitám. | M11, M12 |
| **H3** | Kód vytvořený MAS **nedosáhne** pokrytí testy ≥ 70 % a hodnocení udržovatelnosti A. | Kód vytvořený MAS **dosáhne** pokrytí ≥ 70 % a hodnocení udržovatelnosti A. | M4, M7 |
| **H4** | Systém **umožní** neoprávněný přístup k chráněné kategorii údajů v alespoň jednom testovacím scénáři. | Systém **zablokuje 100 %** neoprávněných přístupů v testovacích scénářích. | M3 |
| **H5** | K dosažení MVP je potřeba **více než 5** lidských zásahů na milník. | K dosažení MVP stačí **nejvýše 5** lidských zásahů na milník. | M20 |
| **H6** | Výběr varianty MAS **neovlivňuje** výsledek pilotu (rozdíl v M1 < 15 p. b.). | Výběr varianty MAS **ovlivňuje** výsledek pilotu (rozdíl v M1 ≥ 15 p. b.). | M1, M20, M22 (pilot) |

*Poznámka k H6:* pilot má jen tři varianty a jedno opakování, proto výsledky hodnotíme popisně, nikoli statistickým testem. Pokud to limity dovolí, pilot zopakujeme 2–3× a uvedeme rozptyl výsledků.

---

## 8. Metriky a způsob hodnocení

Metriky dělíme do šesti oblastí. Pokud to jde, měříme je **automaticky a opakovatelně** (skripty a CI v GitHub Actions). Manuální hodnocení provádějí **alespoň dva hodnotitelé nezávisle** a uvádíme jejich shodu.

### 8.1 Funkčnost a splnění požadavků

| ID | Metrika | Jak měříme | Cíl |
|----|---------|------------|-----|
| M1 | Podíl splněných akceptačních kritérií | **Skryté** akceptační testy (E2E v Playwright), které napíše tým a agenti je neuvidí; počet prošlých / celkem | ≥ 80 % |
| M2 | Trasovatelnost požadavků | matice požadavek → kód → test; podíl požadavků s alespoň jedním testem | 100 % funkcí F1–F9 |
| M3 | Správnost oprávnění | automatizované scénáře „role X zkouší číst kategorii Y“; podíl správně zablokovaných pokusů | 100 % |
| M3b | Pravidlo pro nezletilé | testovací scénáře registrace osoby < 18 let bez skupiny nebo s nezletilým vedoucím | 0 úspěšných porušení |

### 8.2 Kvalita kódu (automatizovaně)

| ID | Metrika | Nástroj | Cíl |
|----|---------|---------|-----|
| M4 | Pokrytí kódu testy (řádky / větve) | coverage nástroj podle zvoleného jazyka (např. Istanbul/c8, coverage.py) | ≥ 70 % řádků, ≥ 60 % větví |
| M5 | Mutační skóre (jestli testy opravdu něco testují) | Stryker / mutmut | ≥ 50 % |
| M6 | Úspěšnost testů vytvořených agenty | CI běh | 100 % zelených |
| M7 | Udržovatelnost, chyby, code smells, duplicita | SonarQube Cloud (zdarma pro veřejné repozitáře) | hodnocení A, duplicita < 5 % |
| M8 | Cyklomatická složitost | SonarQube / lizard | průměr na funkci ≤ 10 |
| M9 | Bezpečnostní nálezy v kódu | Semgrep (statická analýza) + audit závislostí (Dependabot / npm audit / pip-audit) | 0 kritických a vysokých |
| M10 | Bezpečnostní sken běžící aplikace | OWASP ZAP baseline scan | 0 vysokých nálezů |

### 8.3 Výkon a integrita dat při zátěži

| ID | Metrika | Jak měříme | Cíl |
|----|---------|------------|-----|
| M11 | Přečerpání kapacity programu | k6: např. 300 virtuálních uživatelů se během 60 s hlásí na program s kapacitou 20; kontrola počtu záznamů v databázi | 0 |
| M12 | Duplicitní registrace | stejný test, kontrola unikátnosti záznamů | 0 |
| M13 | Doba odezvy pod zátěží | k6: 95. percentil (p95) | < 1 s (požadavek zadání) |
| M14 | Chybovost pod zátěží | k6: podíl HTTP chyb 5xx | < 1 % |

*Poznámka:* zátěžový test probíhá v naší omezené infrastruktuře, nejde tedy o plný produkční test na 2 000 uživatelů. Ověřuje hlavně **integritu dat**, ne škálování.

### 8.4 Uživatelské rozhraní a přístupnost

| ID | Metrika | Jak měříme | Cíl |
|----|---------|------------|-----|
| M15 | Lighthouse skóre (Performance, Accessibility, Best Practices, SEO) | Lighthouse CI na klíčových obrazovkách, mobil i desktop | každá kategorie ≥ 90 |
| M16 | Porušení přístupnosti | axe-core v E2E testech; počet porušení WCAG úrovně A/AA | 0 kritických a závažných |
| M17 | Shoda s návrhovými guidelines | **manuální checklist** podle Google Material Design 3 a Apple Human Interface Guidelines (např. min. velikost dotykových prvků 48 dp / 44 pt, kontrast textu ≥ 4,5 : 1, čitelná velikost písma, konzistentní navigace, zpětná vazba na akce, srozumitelné chybové hlášky); 2 hodnotitelé nezávisle, každá položka splněno / nesplněno | ≥ 85 % položek; shoda hodnotitelů (Cohenovo kappa) ≥ 0,6 |
| M18 | Úspěšnost úkolů v uživatelském testu | 5 testerů (skauti, ideálně vedoucí i účastník) plní scénáře (registrace, připojení do skupiny, výběr programu); podíl úspěšně dokončených úkolů a čas na úkol | ≥ 80 % úkolů bez pomoci |
| M19 | System Usability Scale (SUS) | standardizovaný dotazník po uživatelském testu | ≥ 68 (nadprůměr) |

### 8.5 Proces multiagentního systému a převzatelnost

| ID | Metrika | Jak měříme | Cíl |
|----|---------|------------|-----|
| M20 | Počet lidských zásahů | evidence v deníku milníků: každé vrácení, oprava zadání nebo ruční úprava | ≤ 5 na milník |
| M21 | Míra přepracování | podíl výstupů agentů vrácených při kontrole milníku | sledujeme, bez pevného cíle |
| M22 | Spotřeba zdrojů | počet volání modelu a tokenů, čas běhu; náklady v Kč (u volných úrovní 0 Kč, ale sledujeme narážení na limity) | sledujeme a porovnáváme varianty |
| M23 | Úplnost dokumentace | checklist: README, návod na lokální spuštění, popis architektury, záznamy rozhodnutí (ADR), provozní dokumentace, popis API | 100 % položek |
| M24 | Čas do prvního spuštění pro člověka zvenku | vývojář mimo tým spustí projekt jen podle README; měříme čas a počet dotazů | ≤ 30 min, 0 dotazů |

### 8.6 Validace s uživatelem

| ID | Metrika | Jak měříme | Cíl |
|----|---------|------------|-----|
| M25 | Hodnocení zástupcem Junáka | ukázka MVP + krátký strukturovaný dotazník (škála 1–5: pokryl by potřeby akce bez kompromisu mezi dvěma systémy? je jasná vazba nezletilý ↔ vedoucí? je to dobrý základ pro další vývoj?) | průměr ≥ 3,5 |

---

## 9. Harmonogram

Harmonogram je v týdnech od schválení proposalu. Upravíme ho podle termínů semestru.

| Týden | Milník | Výstup | Kontrola člověkem |
|-------|--------|--------|-------------------|
| 1 | **M0 – Příprava** | odvozené uživatelské příběhy a akceptační kritéria MVP, skryté akceptační testy, repozitář s CI, ověření volných LLM služeb | schválení rozsahu |
| 2–3 | **M1 – Pilot** | tři varianty MAS vytvoří pilotní funkci; vyhodnocení a výběr varianty | výběr varianty (H6) |
| 4 | **M2 – Návrh** | MAS vytvoří architekturu, datový model a wireframy | schválení návrhu |
| 5–7 | **M3 – Implementace** | MAS implementuje F1–F9 v iteracích | průběžné milníky po funkcích |
| 8 | **M4 – Testování** | automatizované metriky (M1–M16), zátěžový test | kontrola výsledků |
| 9 | **M5 – Uživatelská validace** | uživatelský test se skauty (M17–M19), ukázka Junáku (M25), test převzatelnosti (M24) | – |
| 10 | **M6 – Vyhodnocení** | závěrečná zpráva: odpovědi na výzkumné otázky, vyhodnocení hypotéz, doporučení pro Junák | odevzdání |

---

## 10. Tým a role

Konkrétní obsazení rolí ještě není rozděleno. Projekt potřebuje tyto role:

| Role | Náplň |
|------|-------|
| **Product owner / kontakt s Junákem** | správa požadavků, akceptační kritéria, ukázka a validace s Junákem |
| **Orchestrátor MAS** | nastavení a provoz multiagentního systému, kontrola milníků, deník zásahů |
| **QA a metriky** | skryté akceptační testy, CI, nástroje pro automatické metriky, zátěžový test |
| **UX a dokumentace** | hodnocení UI podle guidelines, uživatelský test, SUS, závěrečná zpráva |

Členové týmu: Anna Šmikmátorová, Patrik Michl, Erik Praunsperger, Daniil Astapenko.

---

## 11. Rizika

| Riziko | Dopad | Opatření |
|--------|-------|----------|
| Limity volných LLM služeb nestačí | MAS se zastaví uprostřed práce | kombinace více poskytovatelů, lokální modely (Ollama), menší úkoly pro agenty |
| Únik důvěrného zadání přes volné API | porušení důvěry Junáka | agentům předáváme jen odvozené uživatelské příběhy, nikdy původní dokument |
| MAS vytvoří neudržovatelný kód | MVP nelze převzít | průběžné měření kvality (M4–M10) v CI, kontrola na milnících |
| Agenti „optimalizují na testy“ | zkreslené výsledky | akceptační testy jsou před agenty skryté |
| Malý vzorek pro uživatelský test | slabší vypovídací hodnota | standardizované nástroje (SUS, úspěšnost úkolů), výsledky prezentujeme jako orientační |
| Lidé zasahují víc, než přiznávají | zkreslení M20 | povinný deník zásahů, každý commit od člověka označený |

---

## 12. Očekávané výstupy

1. **MVP registračního systému** ve veřejném repozitáři (bez původního zadání).
2. **Konfigurace multiagentního systému** a deník milníků a zásahů.
3. **Sada metrik a skriptů** pro automatické hodnocení (CI v GitHub Actions).
4. **Závěrečná zpráva:** odpověď na výzkumnou otázku, vyhodnocení hypotéz H1–H6, srovnání variant a doporučení pro Junák a další vývoj.
