# AI Student worksheet

Complete this worksheet before full data collection. Submit the initial version with the proposal and the completed version with the final report.

## A. Project identity

**Project title:** Systematické porovnání AI asistentů v rámci výběru a zpracování vědeckých citací

**Team members:**

- Patrik Michl
- Anna Šmikmátorová
- Daniil Astapenko
- Erik Praunsperger

**Roles:**

- Patrik Michl - vývoj skriptu a promptu
- Anna Šmikmátorová - team lead, dokumentace a tvorba testovacích případů
- Daniil Astapenko - dokumentace a vyhodnocení
- Erik Praunsperger - vývoj skriptu a promptu

**Primary track:**

- [ ] Směr A: Řízený text
- [x] Směr B: Výzkum podložený zdroji
- [ ] Směr C: Vícejazyčné a regionální fungování

**Project scope:**

- [x] Minimální projekt (4 systémy, 40 testovacích případů, 3 výchozí podmínky)
- [ ] Standardní projekt
- [ ] Rozšířený projekt

**Worksheet version and date:**

- 0.1, 11.10.2026

---

## B. Research question

**Primary research question:**

Do jaké míry zlepšuje strukturovaný a optimalizovaný prompt schopnost čtyř AI asistentů (ChatGPT, Gemini, Claude, Perplexity) výběru a zpracování vědeckých citací při psaní odborných textů v češtině.

---

**Capability being measured:**

Výběr zdrojů, kontextové zakotvení citací a ověřování bibliografických údajů v českých akademických textech. Konkrétně schopnost:

1. Vybírat autoritativní, kontextově relevantní vědecké zdroje, které podpoří konkrétní tvrzení.
2. Kriticky odhalovat a odmítat zavádějící, stažené, neakademické nebo nesprávně zařazené vstupy.
3. Generovat syntakticky platné a nehalucinované trvalé identifikátory (DOI a ISBN).

---

**Primary hypothesis:**

Za podmínek použití optimalizovaného promptu s explicitními pravidly pro verifikaci zdrojů a kritérii pro odmítnutí nevhodných podkladů dosáhnou systémy s přístupem na web / specializovaným indexem (např. Perplexity či ChatGPT s vyhledáváním) vyšší míry celkové citační správnosti (kombinace věcné relevance k tématice, správnosti identifikátorů jako ISBN/DOI a úspěšného odmítnutí irelevantních zdrojů) v rámci hlavní metriky (Míra platných a věcně přiléhavých citací), protože propojení vyhledávacího indexu s verifikačními pravidly v promptu efektivně zabraňuje halucinování metadat i nekritickému přebírání nabídnutých irelevantních textů.

Hypotézu budeme považovat za podpořenou pouze tehdy, pokud se tento výsledek projeví také na 10 případech v testovací sadě držené stranou.

---

**Alternative explanation:**

Modely mohou dosahovat vysoké přesnosti u často citovaných prací jednoduše proto, že tyto práce byly mnohonásobně zastoupeny v jejich trénovacích datech. Naopak u méně známých nebo specificky českých publikací bude chybovost v identifikátorech výrazně vyšší bez ohledu na kvalitu promptu.

---

**What result would challenge our hypothesis?**

Naše hypotéza by byla zpochybněna nebo vyvrácena, pokud by:

1. Optimalizovaný prompt nepřinesl měřitelné zlepšení primární metriky (kontextové relevance) u 10 vyhrazených testovacích případů ve srovnání se strukturovanou nebo základní podmínkou (což by svědčilo o přetrénování na vývojových a validačních sadách).
2. Systémy s přístupem na web (Perplexity, ChatGPT s prohlížením, Claude s prohlížením, Gemini) vykazovaly stejnou nebo vyšší míru vymyšlených DOI/ISBN a nekritického přijímání neplatných zdrojů ve srovnání s offline/kontrastními modely, což dokazuje, že samotná integrace vyhledávání nezmírňuje vytváření falešných metadat.
3. Optimalizace zadání vyvolává nadměrné odmítavé chování (falešná odmítnutí), kdy modely odmítají legitimní, ověřitelné zdroje nebo odmítají podpořit platná tvrzení, čímž se snižuje jejich praktická užitečnost.

---

## C. Measurement target

**Operational definition:**

Kvalita citací a podložení tvrzení je definována jako míra, do jaké AI systém generuje český akademický odstavec, v němž každá citace aktivně a přesně podpoří dané tvrzení, odkazuje na ověřitelnou vědeckou literaturu, správně zachází s podezřelými nebo chybnými vstupními zdroji a poskytuje syntakticky správná bibliografická metadata v souladu s normou ČSN ISO 690. Toto se kvantifikuje na testovací sadě vyňaté z trénovacího souboru prostřednictvím tří dimenzí:

1. **Metrika 1 (Hlavní metrika)**: Skóre kontextové relevance (1–10) stanovené lidským hodnotitelem na základě explicitní hodnotící rubriky, která měří opodstatněnost argumentů a významnost zdrojů.

2. **Metrika 2 (Vedlejší metrika 1)**: Programové skóre generované pomocí skriptu (0,0–1,0), které ověřuje syntaxi a kontrolní součty extrahovaných identifikátorů DOI a ISBN, případně také přesnou Jaccardovu překrývací míru s referenčními zdroji.

3. **Metrika 3 (Vedlejší metrika 2)**: Binární indikátor (0/1) měřící explicitní odmítnutí a správnou identifikaci poškozených, neakademických nebo nesprávně označených zdrojů v hraničních případech s protichůdnými scénáři.

---

**Unit of analysis:**

Jednotlivá vygenerovaná odpověď modelu na danou úlohu pod specifickou podmínkou promptu.

---

**Primary metric:**

Věcná relevance a skóre kontextového použití citace. Hodnoceno lidskými hodnotiteli podle předem stanovené rubriky na ordinální škále od 1 do 10 bodů.

---

**Why is it valid?**

Poskytuje přímou konstrukční validitu pro akademické texty. Pouhé porovnání povrchových řetězců nedokáže určit, zda citované dílo skutečně podkládá konkrétní tvrzení uvedené v textu, nebo zda slouží pouze jako povrchní dekorativní prvek. Tento ukazatel přímo zachycuje autoritu v dané oblasti, faktickou shodu a kontextovou soudržnost.

Aby se zabránilo subjektivním odchylkám, jsou platnost a objektivita systematicky zajišťovány pomocí explicitních bodových intervalů (1–3, 4–6, 7–8, 9–10), zaslepení modelu, náhodného pořadí hodnocení a kalibrace dvou hodnotitelů, která měří shodu mezi hodnotiteli u 20 % odpovědí.

---

**What important quality dimension does it fail to capture?**

Nezajišťuje ověření programové autenticity a syntaktické správnosti trvalých identifikátorů (není schopen automaticky detekovat falešné identifikátory DOI ani nesprávně formátované kontrolní součty ISBN).

Rovněž nebere v úvahu dodržování syntaxe formátování bibliografických záznamů a nezohledňuje latenci běhu ani náklady na výpočetní zdroje. Tyto aspekty jsou výhradně svěřeny sekundární metrice 1 a protokolování provozních běhů.

---

## D. Systems and conditions

| System     | Interface/API | Visible model/version | Tools enabled | Prompt adaptations | Date tested |
| ---------- | ------------- | --------------------- | ------------- | ------------------ | ----------- |
| ChatGPT    |               |                       |               |                    |             |
| Gemini     |               |                       |               |                    |             |
| Claude     |               |                       |               |                    |             |
| Perplexity |               |                       |               |                    |             |

**Comparison design:**

- [ ]
- [ ]
- [ ]

**What cannot be made equal?**

---

**How will this limitation affect interpretation?**

---

---

## E. Data and test-set plan

**Total cases:**

**Development cases:**

**Validation cases:**

**Held-out test cases:**

**Repeated-run cases:**

| Stratum                 | Planned number | Actual number | How selected |
| ----------------------- | -------------- | ------------- | ------------ |
| Ordinary                |                |               |              |
| Difficult               |                |               |              |
| Edge or adversarial     |                |               |              |
| Ambiguous or incomplete |                |               |              |
| Czech                   |                |               |              |
| English                 |                |               |              |
| Mixed language          |                |               |              |
| Other relevant stratum  |                |               |              |

**Data provenance:**

---

**Why is this dataset representative of the intended use?**

---

**What leakage or contamination risks exist?**

---

---

## F. Prompt protocol

#### Common baseline prompt

```
Vyřešte níže uvedenou úlohu. Odpovězte pouze v požadovaném formátu.

Úloha:
[user_prompt]

[context_or_files]
```

#### Structured prompt

```
Role: Jste asistent pro práci s odbornou literaturou při psaní odborných textů v češtině.

Cíl: Splňte úlohu níže tak, aby každá citace věcně podporovala konkrétní tvrzení, odkazovala na skutečně existující zdroj a měla správná bibliografická metadata.

Pravidla:

1. Cituj pouze zdroje, jejichž existencí a metadaty si jsi jist nebo které jsi ověřil. Nikdy nevymýšlejte autora, název, rok, časopis, stránky, DOI ani ISBN.
2. Zdroj musí podporovat konkrétní tvrzení, ne jen téma. Přednost mají původní nebo často citované práce.
3. Dodaný zdroj nepoužívej jako podporu, pokud je tematicky nesouvisející, stažený, neověřitelný, neodborný, chybně označený (např. jiný typ dokumentu) nebo pokud tvrzení zkresluje. Vždy uveďte důvod.
4. Pokud je samotné tvrzení nepravdivé nebo přehnané, upozorněte na to a navrhněte opravenou formulaci.
5. Bibliografické záznamy uvádějte podle ČSN ISO 690, odkazy v textu metodou jméno–datum.

Formát odpovědi:

1. Výsledný text – odstavec s odkazy v textu (případně s opraveným tvrzením). Pokud úloha text nevyžaduje, napište „nepoužito“.
2. Seznam literatury – záznamy podle ČSN ISO 690 včetně DOI/ISBN, pokud existují.
3. Nepoužité zdroje – každý nabídnutý, ale nepoužitý zdroj s jednovětým důvodem.
4. Nejistoty – co se nepodařilo ověřit nebo co by měl autor zkontrolovat.

Pokud si nejste jisti, uveďte to v části Nejistoty místo odhadu.

Úloha:
[user_prompt]

[context_or_files]
```

#### Optimized prompt

```
Role: Jste asistent pro práci s odbornou literaturou při psaní odborných textů v češtině.

Cíl: Splňte úlohu níže tak, aby každá citace věcně podporovala konkrétní tvrzení, odkazovala na skutečně existující zdroj a měla správná bibliografická metadata. Výsledné tvrzení musí odpovídat rozsahu a síle důkazů citovaného zdroje.

Pravidla:

1. Citujte pouze zdroje, jejichž existencí a metadaty jste si jisti nebo které jste ověřili. Nikdy nevymýšlejte autora, název, rok, časopis, stránky, DOI ani ISBN.

2. Zdroj musí podporovat konkrétní tvrzení, nikoli pouze obecné téma. Přednost mají původní nebo významné odborné práce. Známá či často citovaná publikace není automaticky vhodným důkazem pro každou větu z daného oboru.

3. Před použitím citace posuďte:
   - který konkrétní závěr nebo pasáž zdroje podporuje tvrzení;
   - zda odpovídá zkoumaná populace, prostředí, období a podmínky;
   - zda zdroj poskytuje přímý důkaz, nebo pouze obecné teoretické východisko;
   - zda formulace tvrzení není silnější nebo obecnější než závěr zdroje.

   Nepřisuzujte zdroji obsah, který neznáte.

4. Pokud zdroj podporuje tvrzení jen částečně nebo za určitých podmínek, zpřesněte přímo výsledný odstavec. Nestačí ponechat nepřesnou větu a její omezení uvést až v části Nejistoty.

5. Nezaměňujte souvislost za příčinu, nezjištěný efekt za definitivní důkaz neexistence efektu ani výsledek jedné studie za univerzální pravidlo. Používejte výrazy jako „prokazuje“, „jednoznačně vyvrací“ nebo „vždy“ pouze tehdy, pokud odpovídají skutečné síle důkazů.

6. U definic, přímých citátů a formulací převzatých přes dalšího autora rozlišujte původního autora a sekundární pramen. Stránku uvádějte jen tehdy, pokud odpovídá příslušné pasáži. Pokud přesnou oporu nemáte, použijte doloženou parafrázi nebo nejistotu přiznejte.

7. Dodaný zdroj nepoužívejte jako podporu, pokud je tematicky nesouvisející, stažený, neověřitelný, neodborný, chybně označený nebo pokud tvrzení zkresluje. Vždy uveďte důvod.

8. Pokud je samotné tvrzení nepravdivé nebo přehnané, upozorněte na to a navrhněte opravenou formulaci. Také náhradní tvrzení a věcné komentáře musí mít odpovídající oporu. Pokud ji nemáte, neprezentujte vlastní domněnku jako odborný závěr.

9. Pokud mezi nabízenými zdroji není přesná opora tvrzení, tuto skutečnost uveďte. Nejbližší tematický zdroj nepředstavujte jako přímý důkaz. Respektujte přitom omezení úlohy na výběr z nabízených kandidátů.

10. Bibliografické záznamy uvádějte podle ČSN ISO 690, odkazy v textu metodou jméno–datum.

Formát odpovědi:

1. Výsledný text – odstavec s odkazy v textu, případně s opraveným nebo zpřesněným tvrzením. Pokud úloha text nevyžaduje, napište „nepoužito“.
2. Seznam literatury – záznamy podle ČSN ISO 690 včetně DOI/ISBN, pokud existují.
3. Nepoužité zdroje – každý nabídnutý, ale nepoužitý zdroj s jednovětým důvodem.
4. Nejistoty – co se nepodařilo zjistit nebo ověřit, zejména omezení podpory tvrzení a nejasný původ definic. Tyto poznámky nesmějí odporovat výslednému odstavci.

Úloha:

[user_prompt]

[context_or_files]
```

**What remains constant?**

1. **Výzkumná doména a cílový jazyk:** Podmínky se zaměřují na vyhledávání, výběr a zpracování vědeckých citací, které vhodně podporují tvrzení.
2. **Citační standard a forma:** Je vyžadováno dodržení normy ČSN ISO 690 a citační metody jméno–datum (autor-rok) v textu.
3. **Zákaz vymýšlení údajů:** Platí striktní požadavek na faktickou pravdivost (zákaz halucinování neexistujících autorů, titulů, letopočtů, DOI nebo ISBN).
4. **Čtyřsložková struktura výstupu:** U strukturované i optimalizované podmínky zůstává zachován jednotný formát odpovědi (1. Výsledný text, 2. Seznam literatury, 3. Nepoužité zdroje, 4. Nejistoty).

---

**What is intentionally different?**

1. **Baseline vs. Strukturovaný prompt:**
    - _Baseline prompt_ obsahuje pouze minimalistickou instrukci bez vymezení role, bez explicitních kritérií kvality a bez strukturování výstupu.
    - _Strukturovaný prompt_ definuje roli akademického asistenta, explicitní cíl, základní pětici pravidel a povinné rozčlenění výstupu na 4 sekce, čímž odděluje výsledný text od metadat a reflexe nejistot.
2. **Strukturovaný vs. Optimalizovaný prompt (výběr Kandidáta A):**
    - _Epistemická kontrola a argumentační síla (Pravidla 3, 4 a 5):_ Optimalizovaný prompt zavádí povinné posouzení zkoumané populace, podmínek, rozlišení přímého důkazu od obecného teoretického rámce a striktní zákaz záměny korelace za kauzalitu či zobecnění jedné studie na univerzální pravidlo.
    - _Aktivní zpřesnění výsledného textu (Pravidlo 4):_ Klíčová změna: pokud zdroj podporuje tvrzení jen částečně či podmíněně, model nesmí nechat nepřesnou větu a pouze ji okomentovat v Nejistotách, ale musí přímo formulačně zpřesnit generovaný odstavec. To přímo maximalizuje skóre hlavní Metriky 1.
    - _Kritické odmítnutí zavádějících zdrojů a obrana proti manipulaci (Pravidla 7, 8 a 9):_ Explicitní pravidla pro detekci podstrčených, fiktivních či opačných tezí a prompt injection útoků (klíčové pro Metriku 3).
    - _Odůvodnění zamítnutí Kandidáta B:_ Kandidát B byl v pilotním srovnání zaměřen na mikromanagement metadat a generování přehledů změn (`Původní údaj -> Opravený údaj`). Tento administrativní přístup jednak nepřinesl zlepšení věcné relevance, a jednak paradoxně zvýšil chybovost v identifikátorech (halucinace číslice v DOI a obalování odkazů do vyhledávání Google). Optimalizovaný prompt (Kandidát A) ponechává modelu dostatek pozornostní kapacity pro věcnou a faktickou přesnost trvalých identifikátorů (100% úspěšnost v pilotu).

---

**When will prompts be frozen?**

Prompty jsou definitivně zmrazeny po ukončení pilotního vyhodnocení na validační sadě a výběru vítězného optimalizovaného promptu (Kandidát A). K tomuto zmrazení dochází **před zahájením jakéhokoliv testování na vyhrazené testovací sadě**.

Od okamžiku spuštění ostrého sběru dat na 10 testovacích případech pro všechny 4 AI asistenty (ChatGPT, Gemini, Claude, Perplexity) je jakákoliv další modifikace promptů, dovažování pravidel či dodatečné ladění přísně zakázáno, aby nedošlo ke zkreslení výsledků a porušení experimentálního protokolu.

---

**How will held-out cases remain protected?**

1. **Striktní oddělení datových splitů:** 10 testovacích případů (`split == 'test'`: A07, A08, B07, B08, C07, C08, D07, D08, E07, E08) bylo drženo odděleně od fáze návrhu a ladění promptu.
2. **Zákaz kontaminace znalostmi:** V textu žádného z promptů nejsou obsaženy žádné konkrétní názvy děl, autoři, ISBN/DOI ani oborové specifické nápovědy pocházející z testovací sady.
3. **Jednorázové ostré spuštění:** Každý model pod každou podmínkou absolvuje na testovací sadě pouze jeden ostrý běh (žádné opakované pokusy či ladění promptu podle chyb pozorovaných na testovacích datech).
4. **Zaslepené a nezávislé vyhodnocení:** Hodnocení proběhne až post-hoc – u Metriky 2 plně automatizovaným skriptem `metrika2.py` vůči zamčeným referencím a u Metrik 1 a 3 zaslepeným posouzením hodnotiteli s měřením shody, bez zpětné vazby do textu promptů.

---

## G. Prompt-change log

| Version | Date | Change | Evidence | Expected effect | Actual validation effect | Retained? |
| ------- | ---- | ------ | -------- | --------------- | ------------------------ | --------- |
| v0      |      |        |          |                 |                          |           |
| v1      |      |        |          |                 |                          |           |
| v2      |      |        |          |                 |                          |           |
| v3      |      |        |          |                 |                          |           |

---

## H. Evaluation plan

| Metric | Primary/secondary | Automatic/
human/judge | Calculation | Calibration or validation | Limitation |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |

**Human raters:**

**Blinding procedure:**

**Response-order randomization:**

**Inter-rater agreement measure:**

**LLM-as-judge used?** Yes / No

If yes, state judge model, rubric, calibration sample, and known risks:

---

---

## I. Failure and retry policy

**What counts as a failed run?**

---

**Are retries allowed?**

---

**Maximum retries:**

---

**How will first-attempt and eventual success be reported?**

---

**Which product or infrastructure failures will be excluded, and why?**

---

---

### J. Logging checklist

- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]

**Storage location:**

---

**Anonymization and data-protection procedure:**

---

---

## K. Pilot review

**Pilot size:**

**What failed in the pilot?**

---

**Which cases were rewritten or removed?**

---

**Which metric or rubric changes were made?**

---

**What evidence supports freezing the benchmark?**

---

**What remains uncertain?**

---

---

## L. Results table

| System      | Condition  | _N_ | Primary score | Interval or variation | Secondary score | Median latency | Cost | First-attempt success |
| ----------- | ---------- | --- | ------------- | --------------------- | --------------- | -------------- | ---- | --------------------- |
| ChatGPT     | Baseline   |     |               |                       |                 |                |      |                       |
| ChatGPT     | Structured |     |               |                       |                 |                |      |                       |
| ChatGPT     | Optimized  |     |               |                       |                 |                |      |                       |
| Gemini      | Baseline   |     |               |                       |                 |                |      |                       |
| Gemini      | Structured |     |               |                       |                 |                |      |                       |
| Gemini      | Optimized  |     |               |                       |                 |                |      |                       |
| Claude      | Baseline   |     |               |                       |                 |                |      |                       |
| Claude      | Structured |     |               |                       |                 |                |      |                       |
| Claude      | Optimized  |     |               |                       |                 |                |      |                       |
| Claude Code | Baseline   |     |               |                       |                 |                |      |                       |
| Claude Code | Structured |     |               |                       |                 |                |      |                       |
| Claude Code | Optimized  |     |               |                       |                 |                |      |                       |
| Grok        | Baseline   |     |               |                       |                 |                |      |                       |
| Grok        | Structured |     |               |                       |                 |                |      |                       |
| Grok        | Optimized  |     |               |                       |                 |                |      |                       |
| Perplexity  | Baseline   |     |               |                       |                 |                |      |                       |
| Perplexity  | Structured |     |               |                       |                 |                |      |                       |
| Perplexity  | Optimized  |     |               |                       |                 |                |      |                       |

---

### M. Error analysis

| Error ID | System | Condition | Task ID | Category | Severity | First attempt? | Description | Likely cause | Preventable by prompt? |
| -------- | ------ | --------- | ------- | -------- | -------- | -------------- | ----------- | ------------ | ---------------------- |
|          |        |           |         |          |          |                |             |              |                        |
|          |        |           |         |          |          |                |             |              |                        |
|          |        |           |         |          |          |                |             |              |                        |
|          |        |           |         |          |          |                |             |              |                        |
|          |        |           |         |          |          |                |             |              |                        |

**Most frequent error:**

---

**Most consequential error:**

---

**Did optimization change the error distribution?**

---

---

## N. Practical recommendation

**Best system for the defined capability:**

---

**Best prompt condition:**

---

**Conditions under which this recommendation holds:**

---

**Important cost, latency, or human-effort trade-off:**

---

**What should a practitioner not infer from this study?**

---

---

## O. Validity and limitations

**Construct validity: are we measuring the intended capability?**

---

**Internal validity: could another factor explain the result?**

---

**External validity: where might the result fail to generalize?**

---

**Statistical uncertainty or sample-size limitation:**

---

**Product or model-version drift:**

---

**Evaluation bias or judge bias:**

---

**Most important follow-up experiment:**
