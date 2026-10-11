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

```

#### Structured prompt

```

```

#### Optimized prompt

```

```

**What remains constant?**

---

**What is intentionally different?**

---

**When will prompts be frozen?**

---

**How will held-out cases remain protected?**

---

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
