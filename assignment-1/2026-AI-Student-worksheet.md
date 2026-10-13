## A. Identita projektu

**Název projektu:** Systematické porovnání AI asistentů v rámci výběru a zpracování vědeckých citací

**Členové týmu:**

- Patrik Michl
- Anna Šmikmátorová
- Daniil Astapenko
- Erik Praunsperger

**Role:**

- Patrik Michl - vývoj skriptu a promptu
- Anna Šmikmátorová - team lead, dokumentace a tvorba testovacích případů
- Daniil Astapenko - dokumentace a vyhodnocení
- Erik Praunsperger - vývoj skriptu a promptu

**Hlavní směr:**

- [ ] Směr A: Řízený text
- [x] Směr B: Výzkum podložený zdroji
- [ ] Směr C: Vícejazyčné a regionální fungování

**Rozsah projektu:**

- [x] Minimální projekt (4 systémy, 40 testovacích případů, 3 výchozí podmínky)
- [ ] Standardní projekt
- [ ] Rozšířený projekt

**Verze a datum worksheetu:**

- 0.1, 11.10.2026
- 0.2, 13.10.2026

---

## B. Výzkumná otázka

**Hlavní výzkumná otázka:**

Do jaké míry zlepšuje strukturovaný a optimalizovaný prompt schopnost čtyř AI asistentů (ChatGPT, Gemini, Claude, Perplexity) výběru a zpracování vědeckých citací při psaní odborných textů v češtině.

---

**Měřená schopnost:**

Výběr zdrojů, kontextové zakotvení citací a ověřování bibliografických údajů v českých akademických textech. Konkrétně schopnost:

1. Vybírat autoritativní, kontextově relevantní vědecké zdroje, které podpoří konkrétní tvrzení.
2. Kriticky odhalovat a odmítat zavádějící, stažené, neakademické nebo nesprávně zařazené vstupy.
3. Generovat syntakticky platné a nehalucinované trvalé identifikátory (DOI a ISBN).

---

**Hlavní hypotéza:**

Za podmínek použití optimalizovaného promptu s explicitními pravidly pro verifikaci zdrojů a kritérii pro odmítnutí nevhodných podkladů dosáhnou systémy s přístupem na web / specializovaným indexem (např. Perplexity či ChatGPT s vyhledáváním) vyšší míry celkové citační správnosti (kombinace věcné relevance k tématice, správnosti identifikátorů jako ISBN/DOI a úspěšného odmítnutí irelevantních zdrojů) v rámci hlavní metriky (Míra platných a věcně přiléhavých citací), protože propojení vyhledávacího indexu s verifikačními pravidly v promptu efektivně zabraňuje halucinování metadat i nekritickému přebírání nabídnutých irelevantních textů.

Hypotézu budeme považovat za podpořenou pouze tehdy, pokud se tento výsledek projeví také na 10 případech v testovací sadě držené stranou.

---

**Alternativní vysvětlení:**

Modely mohou dosahovat vysoké přesnosti u často citovaných prací jednoduše proto, že tyto práce byly mnohonásobně zastoupeny v jejich trénovacích datech. Naopak u méně známých nebo specificky českých publikací bude chybovost v identifikátorech výrazně vyšší bez ohledu na kvalitu promptu.

---

**Jaký výsledek by naši hypotézu zpochybnil?**

Naše hypotéza by byla zpochybněna nebo vyvrácena, pokud by:

1. Optimalizovaný prompt nepřinesl měřitelné zlepšení primární metriky (kontextové relevance) u 10 vyhrazených testovacích případů ve srovnání se strukturovanou nebo základní podmínkou (což by svědčilo o přetrénování na vývojových a validačních sadách).
2. Systémy s přístupem na web (Perplexity, ChatGPT s prohlížením, Claude s prohlížením, Gemini) vykazovaly stejnou nebo vyšší míru vymyšlených DOI/ISBN a nekritického přijímání neplatných zdrojů ve srovnání s offline/kontrastními modely, což dokazuje, že samotná integrace vyhledávání nezmírňuje vytváření falešných metadat.
3. Optimalizace zadání vyvolává nadměrné odmítavé chování (falešná odmítnutí), kdy modely odmítají legitimní, ověřitelné zdroje nebo odmítají podpořit platná tvrzení, čímž se snižuje jejich praktická užitečnost.

---

## C. Cíl měření

**Operační definice:**

Kvalita citací a podložení tvrzení je definována jako míra, do jaké AI systém generuje český akademický odstavec, v němž každá citace aktivně a přesně podpoří dané tvrzení, odkazuje na ověřitelnou vědeckou literaturu, správně zachází s podezřelými nebo chybnými vstupními zdroji a poskytuje syntakticky správná bibliografická metadata v souladu s normou ČSN ISO 690. Toto se kvantifikuje na testovací sadě vyňaté z trénovacího souboru prostřednictvím tří dimenzí:

1. **Metrika 1 (Hlavní metrika)**: Skóre kontextové relevance (1–10) stanovené lidským hodnotitelem na základě explicitní hodnotící rubriky, která měří opodstatněnost argumentů a významnost zdrojů.

2. **Metrika 2 (Vedlejší metrika 1)**: Programové skóre generované pomocí skriptu (0,0–1,0), které ověřuje syntaxi a kontrolní součty extrahovaných identifikátorů DOI a ISBN, případně také přesnou Jaccardovu překrývací míru s referenčními zdroji.

3. **Metrika 3 (Vedlejší metrika 2)**: Binární indikátor (0/1) měřící explicitní odmítnutí a správnou identifikaci poškozených, neakademických nebo nesprávně označených zdrojů v hraničních případech s protichůdnými scénáři.

---

**Jednotka analýzy:**

Jednotlivá vygenerovaná odpověď modelu na danou úlohu pod specifickou podmínkou promptu.

---

**Hlavní metrika:**

Věcná relevance a skóre kontextového použití citace. Hodnoceno lidskými hodnotiteli podle předem stanovené rubriky na ordinální škále od 1 do 10 bodů.

---

**Proč je metrika validní?**

Poskytuje přímou konstrukční validitu pro akademické texty. Pouhé porovnání povrchových řetězců nedokáže určit, zda citované dílo skutečně podkládá konkrétní tvrzení uvedené v textu, nebo zda slouží pouze jako povrchní dekorativní prvek. Tento ukazatel přímo zachycuje autoritu v dané oblasti, faktickou shodu a kontextovou soudržnost.

Aby se zabránilo subjektivním odchylkám, jsou platnost a objektivita systematicky zajišťovány pomocí explicitních bodových intervalů (1–3, 4–6, 7–8, 9–10), zaslepení modelu, náhodného pořadí hodnocení a kalibrace dvou hodnotitelů, která měří shodu mezi hodnotiteli u 20 % odpovědí.

---

**Jakou důležitou dimenzi kvality nezachycuje?**

Nezajišťuje ověření programové autenticity a syntaktické správnosti trvalých identifikátorů (není schopen automaticky detekovat falešné identifikátory DOI ani nesprávně formátované kontrolní součty ISBN).

Rovněž nebere v úvahu dodržování syntaxe formátování bibliografických záznamů a nezohledňuje latenci běhu ani náklady na výpočetní zdroje. Tyto aspekty jsou výhradně svěřeny sekundární metrice 1 a protokolování provozních běhů.

---

## D. Systémy a podmínky

| Systém     | Rozhraní/API                     | Viditelný model/verze                        | Zapnuté nástroje                                                                        | Úpravy promptu                                                                      | Datum testování |
| ---------- | -------------------------------- | -------------------------------------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | --------------- |
| ChatGPT    | Webové rozhraní, bezplatná verze | GPT-6                                        | Výchozí nastavení bezplatné verze; výstupy obsahují webové odkazy (vyhledávání na webu) | Žádné – stejné znění promptu jako u ostatních systémů, vloženo ručně v jedné zprávě | 2026-10-12      |
| Gemini     | Webové rozhraní, bezplatná verze | Flash 2.5                                    | Výchozí nastavení bezplatné verze; výstupy neobsahují webové odkazy                     | Žádné – stejné znění promptu jako u ostatních systémů, vloženo ručně v jedné zprávě | 2026-10-12      |
| Claude     | Webové rozhraní, bezplatná verze | Haiku 5.5 Low                                | Výchozí nastavení bezplatné verze; webové odkazy ve výstupech jen ojediněle             | Žádné – stejné znění promptu jako u ostatních systémů, vloženo ručně v jedné zprávě | 2026-10-12      |
| Perplexity | Webové rozhraní, bezplatná verze | neznámý (free verze neumožňuje volbu modelů) | Výchozí nastavení bezplatné verze; vyhledávání na webu je součástí produktu             | Žádné – stejné znění promptu jako u ostatních systémů, vloženo ručně v jedné zprávě | 2026-10-12      |

**Design srovnání:**

- [x] Všechny 4 systémy × 3 podmínky promptu (výchozí, strukturovaný, optimalizovaný) na stejných 10 testovacích případech = 120 běhů (úplný faktoriální design 4 × 3 × 10).
- [x] Prompty jsou pro všechny systémy textově identické a zmrazené před testováním; každý běh probíhá v nové konverzaci bez historie.
- [x] Systémy jsou testovány tak, jak je vidí běžný uživatel (bezplatné webové verze s výchozím nastavením), nikoli přes API s řízenými parametry.

**Co nelze sjednotit?**

Model a jeho verzi v bezplatných verzích (poskytovatel ji může měnit bez oznámení a u některých systémů není plně viditelná), přístup k webu a vyhledávání (Perplexity a ChatGPT vyhledávají, Gemini a Claude ve výstupech odkazy prakticky neuvádějí), parametry generování (teplota, délka odpovědi), skryté systémové prompty a bezpečnostní vrstvy poskytovatelů, limity bezplatných verzí a zátěž serverů v době testování. U webových rozhraní také nelze přesně a srovnatelně měřit latenci ani náklady.

---

**Jak toto omezení ovlivní interpretaci?**

Výsledky popisují chování konkrétních bezplatných produktů v den testování (12. 10. 2026), nikoli obecnou kvalitu podkladových modelů. Rozdíly mezi systémy nelze jednoznačně přičíst samotnému modelu, protože se současně liší i nástroje (vyhledávání) a skryté nastavení. Spolehlivější je srovnání podmínek promptu uvnitř jednoho systému (výchozí vs. strukturovaný vs. optimalizovaný), kde jsou ostatní faktory stejné. Vliv přístupu k webu z hypotézy lze posoudit jen orientačně, protože není experimentálně manipulován.

---

## E. Plán dat a testovací sady

**Celkový počet případů:** 40 (5 typů úloh × 8 případů: A – dohledání zdroje, B – výběr z kandidátů, C – podstrčený zdroj, D – formální metadata, E – české a regionální zdroje)

**Vývojové případy:** 20 (A01–A04, B01–B04, C01–C04, D01–D04, E01–E04)

**Validační případy:** 10 (A05–A06, B05–B06, C05–C06, D05–D06, E05–E06)

**Testovací případy držené stranou:** 10 (A07–A08, B07–B08, C07–C08, D07–D08, E07–E08)

**Případy s opakovaným během:** 0 – každá kombinace systém × podmínka × případ má na testovací sadě jeden ostrý běh (viz oddíl F).

Kategorie se překrývají (jeden případ může být např. obtížný, hraniční a zároveň v češtině). Čísla v závorce udávají počet v testovací sadě.

| Kategorie                                               | Plánovaný počet | Skutečný počet | Způsob výběru                                                                                                                                                             |
| ------------------------------------------------------- | --------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Běžné                                                   | 12 (3)          | 12 (3)         | Případy bez hraničního scénáře (A07, A08, B08 v testu); tvrzení podložitelné známou publikací                                                                             |
| Obtížné                                                 | 10 (5)          | 10 (5)         | Obtížnost „těžká“ přidělená týmem (C07, C08, D07, E07, E08 v testu)                                                                                                       |
| Hraniční nebo protichůdné                               | 13 (4)          | 13 (4)         | Případy s podvrženým, fiktivním, staženým nebo zkresleně použitým zdrojem, tematickým distraktorem či prompt injection; hodnocené Metrikou 3 (B07, C07, C08, E07 v testu) |
| Nejednoznačné nebo neúplné                              | 7 (1)           | 7 (1)          | Chybějící informace, chybějící identifikátor, nejednoznačný autor/rok nebo více vydání (D08 v testu)                                                                      |
| Česky                                                   | 38 (10)         | 38 (10)        | Všechna zadání a odstavce jsou v češtině, protože cílem je psaní českých odborných textů                                                                                  |
| Anglicky                                                | 0               | 0              | Záměrně nezařazeno – mimo rozsah výzkumné otázky                                                                                                                          |
| Smíšený jazyk                                           | 2 (0)           | 2 (0)          | Kombinace českého zadání a anglických podkladů (E04, E06)                                                                                                                 |
| Jiná relevantní kategorie: málo citované / české zdroje | 8 (3)           | 8 (3)          | Málo citované české publikace a český právní předpis (C08, E07, E08 v testu); testují alternativní vysvětlení o zastoupení v trénovacích datech                           |

**Původ dat:**

Všechny testovací případy (zadání, odstavce s tvrzeními a nabízené kandidátní zdroje) vytvořil tým synteticky. Většina odkazuje na reálné publikace s ověřeným DOI/ISBN (referenční údaje jsou uloženy ve sloupcích `ref_*` souboru `Testcases.xlsx`), jeden případ na veřejný právní předpis ze Sbírky zákonů a dva na veřejné dokumenty úřadů. Šest případů obsahuje záměrně fiktivní zdroje nebo metadata vytvořené týmem (C02, C04, C06, C08, D05, E07). Případy pokrývají domény informatika/AI, psychologie, ekonomie, pedagogika, sociologie, metodologie, zemědělství a klima, medicína, právo, botanika a geografie.

---

**Proč je tento dataset reprezentativní pro zamýšlené použití?**

Případy napodobují reálné situace studenta nebo výzkumníka při psaní české odborné práce: doplnění citace k tvrzení, výběr nejvhodnějšího zdroje z několika kandidátů, kontrolu podstrčených či chybných zdrojů, opravu bibliografického záznamu podle ČSN ISO 690 a práci s českými a regionálními zdroji. Kombinuje vysoce citované práce s málo citovanými českými publikacemi a zahrnuje typické chyby, se kterými se uživatelé setkávají (halucinované DOI, záměna prací, stažené články). Reprezentativnost je omezená malým počtem případů na kategorii a převahou vysoce citovaných zdrojů (24 ze 40).

---

**Jaká existují rizika úniku dat nebo kontaminace?**

1. Většina referenčních publikací je vysoce citovaná a téměř jistě je obsažena v trénovacích datech modelů, takže úspěch může odrážet zapamatování, nikoli schopnost ověřovat (viz alternativní vysvětlení).
2. Systémy s vyhledáváním mohou najít referenční záznam přímo na webu; to je ale součást měřeného chování produktu, nikoli únik.
3. Repozitář s testovacími případy je veřejný na GitHubu; pokud by se dostal do trénovacích dat nebo vyhledávacího indexu, mohl by zkreslit budoucí opakování (pro toto testování 12. 10. 2026 je riziko zanedbatelné).
4. Ladění promptu probíhalo jen na vývojové a validační sadě; testovací případy v textu promptů nefigurují (viz oddíl F).
5. Bezplatné verze mohou ukládat konverzace pro trénink, proto byly testovací případy zadány jen při ostrém běhu.

---

## F. Protokol promptů

#### Společný výchozí prompt

```
Vyřešte níže uvedenou úlohu. Odpovězte pouze v požadovaném formátu.

Úloha:
[user_prompt]

[context_or_files]
```

#### Strukturovaný prompt

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

#### Optimalizovaný prompt

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

**Co zůstává konstantní?**

1. **Výzkumná doména a cílový jazyk:** Podmínky se zaměřují na vyhledávání, výběr a zpracování vědeckých citací, které vhodně podporují tvrzení.
2. **Citační standard a forma:** Je vyžadováno dodržení normy ČSN ISO 690 a citační metody jméno–datum (autor-rok) v textu.
3. **Zákaz vymýšlení údajů:** Platí striktní požadavek na faktickou pravdivost (zákaz halucinování neexistujících autorů, titulů, letopočtů, DOI nebo ISBN).
4. **Čtyřsložková struktura výstupu:** U strukturované i optimalizované podmínky zůstává zachován jednotný formát odpovědi (1. Výsledný text, 2. Seznam literatury, 3. Nepoužité zdroje, 4. Nejistoty).

---

**Co se záměrně liší?**

1. **Baseline vs. Strukturovaný prompt:**
    - _Baseline prompt_ obsahuje pouze minimalistickou instrukci bez vymezení role, bez explicitních kritérií kvality a bez strukturování výstupu.
    - _Strukturovaný prompt_ definuje roli akademického asistenta, explicitní cíl, základní pětici pravidel a povinné rozčlenění výstupu na 4 sekce, čímž odděluje výsledný text od metadat a reflexe nejistot.
2. **Strukturovaný vs. Optimalizovaný prompt (výběr Kandidáta A):**
    - _Epistemická kontrola a argumentační síla (Pravidla 3, 4 a 5):_ Optimalizovaný prompt zavádí povinné posouzení zkoumané populace, podmínek, rozlišení přímého důkazu od obecného teoretického rámce a striktní zákaz záměny korelace za kauzalitu či zobecnění jedné studie na univerzální pravidlo.
    - _Aktivní zpřesnění výsledného textu (Pravidlo 4):_ Klíčová změna: pokud zdroj podporuje tvrzení jen částečně či podmíněně, model nesmí nechat nepřesnou větu a pouze ji okomentovat v Nejistotách, ale musí přímo formulačně zpřesnit generovaný odstavec. To přímo maximalizuje skóre hlavní Metriky 1.
    - _Kritické odmítnutí zavádějících zdrojů a obrana proti manipulaci (Pravidla 7, 8 a 9):_ Explicitní pravidla pro detekci podstrčených, fiktivních či opačných tezí a prompt injection útoků (klíčové pro Metriku 3).
    - _Odůvodnění zamítnutí Kandidáta B:_ Kandidát B byl v pilotním srovnání zaměřen na mikromanagement metadat a generování přehledů změn (`Původní údaj -> Opravený údaj`). Tento administrativní přístup jednak nepřinesl zlepšení věcné relevance, a jednak paradoxně zvýšil chybovost v identifikátorech (halucinace číslice v DOI a obalování odkazů do vyhledávání Google). Optimalizovaný prompt (Kandidát A) ponechává modelu dostatek pozornostní kapacity pro věcnou a faktickou přesnost trvalých identifikátorů (100% úspěšnost v pilotu).

---

**Kdy budou prompty zmrazeny?**

Prompty jsou definitivně zmrazeny po ukončení pilotního vyhodnocení na validační sadě a výběru vítězného optimalizovaného promptu (Kandidát A). K tomuto zmrazení dochází **před zahájením jakéhokoliv testování na vyhrazené testovací sadě**.

Od okamžiku spuštění ostrého sběru dat na 10 testovacích případech pro všechny 4 AI asistenty (ChatGPT, Gemini, Claude, Perplexity) je jakákoliv další modifikace promptů, dovažování pravidel či dodatečné ladění přísně zakázáno, aby nedošlo ke zkreslení výsledků a porušení experimentálního protokolu.

---

**Jak budou chráněny testovací případy držené stranou?**

1. **Striktní oddělení datových splitů:** 10 testovacích případů (`split == 'test'`: A07, A08, B07, B08, C07, C08, D07, D08, E07, E08) bylo drženo odděleně od fáze návrhu a ladění promptu.
2. **Zákaz kontaminace znalostmi:** V textu žádného z promptů nejsou obsaženy žádné konkrétní názvy děl, autoři, ISBN/DOI ani oborové specifické nápovědy pocházející z testovací sady.
3. **Jednorázové ostré spuštění:** Každý model pod každou podmínkou absolvuje na testovací sadě pouze jeden ostrý běh (žádné opakované pokusy či ladění promptu podle chyb pozorovaných na testovacích datech).
4. **Zaslepené a nezávislé vyhodnocení:** Hodnocení proběhne až post-hoc – u Metriky 2 plně automatizovaným skriptem `metrika2.py` vůči zamčeným referencím a u Metrik 1 a 3 zaslepeným posouzením hodnotiteli s měřením shody, bez zpětné vazby do textu promptů.

---

## G. Záznam změn promptu

| Verze               | Datum        | Změna                                                                                                                                                                                                                                                                                                  | Důkaz                                                                                                                                                                | Očekávaný efekt                                                                                                                                                     | Skutečný efekt na validační sadě                                                                                                                                                                                                       | Ponecháno?                                                 |
| ------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **v0** (Baseline)   | 11. 10. 2026 | Výchozí nestrukturovaný prompt: pouze zástupné proměnné `[user_prompt]` a `[context_or_files]` s minimalistickým pokynem k vyřešení.                                                                                                                                                                   | Požadavek metodiky na nulovou experimentální podmínku pro měření přidané hodnoty prompt engineeringu.                                                                | Očekávána vysoká variabilita formátu výstupu, povrchní citování bez ověření a náchylnost k halucinacím identifikátorů.                                              | Slouží jako spodní srovnávací hranice výkonu; modely často míchají text s metadaty a neposuzují spolehlivost zdrojů.                                                                                                                   | **ANO** (ponecháno jako podmínka Common baseline)          |
| **v1** (Structured) | 11. 10. 2026 | Zavedení role akademického asistenta, definice cíle, 5 základních pravidel (pravdivost, ČSN ISO 690, zákaz vymýšlení) a 4-složkové struktury výstupu (Text, Seznam literatury, Nepoužité zdroje, Nejistoty).                                                                                           | Nekonzistentní struktura odpovědí v baseline; nutnost oddělit syntetizovaný text od bibliografie a reflexe limitů.                                                   | Standardizace formátu odpovědí, redukce halucinací vymezením sekce Nejistoty, základní odmítání irelevantních zdrojů.                                               | Formát odpovědí sjednocen. Nicméně model občas ponechává nepřesná tvrzení v odstavci a limity pouze pasivně konstatuje v Nejistotách. Také relativně často dělá chyby během formátování citací (špatné jméno autora nebo DOI).         | **ANO** (ponecháno jako podmínka Structured prompt)        |
| **v2** (Kandidát B) | 12. 10. 2026 | Pokus o optimalizaci přes administrativní mikromanagement metadat (Pravidla 2–7: kontrola jednotlivých bibliografických polí, zachování identity díla, povinný rozpis změn `Původní údaj -> Opravený údaj`).                                                                                           | Snaha zabránit halucinování metadat a přinutit model explicitně deklarovat každou změnu ve vstupních záznamech.                                                      | Eliminace vymyšlených identifikátorů (DOI/ISBN) a striktní formální přesnost bibliografického záznamu.                                                              | **Neuspokojivý:** Model plýtvá kapacitou na changelogy, nepřeformulovává sporné odstavce a paradoxně **chybuje v identifikátorech** (halucinace číslice v DOI u B05: `...7764` místo `...7763`, generování Google search linků u C05). | **NE** (zamítnuto ve prospěch v3)                          |
| **v3** (Kandidát A) | 12. 10. 2026 | Optimalizace zaměřená na epistemickou čili zkoumající sílu argumentu a kontextové zakotvení (Pravidla 3, 4, 5, 7, 8, 9). Klíčové **Pravidlo 4** nařizuje přímo formulačně zpřesnit generovaný odstavec při částečné podpoře zdroje; zákaz záměny korelace za kauzalitu; obrana proti prompt injection. | Validační zjištění, že pasivní konstatování nestačí pro vědecký text a že přetížení formálními checklisty (v2) degraduje pozornost modelu a přesnost identifikátorů. | Výrazné zvýšení věcné a kontextové relevance (Metrika 1), 100% faktická přesnost identifikátorů (Metrika 2) a spolehlivé odmítnutí zavádějících zdrojů (Metrika 3). | **Vynikající:** M1 průměr 9/10; 100% faktická shoda DOI/ISBN; 100% úspěšnost u edge cases (M3); vysoká robustnost a logické vypořádání i při nejednoznačném zadání (D06).                                                              | **ANO** (vybráno a zmrazeno jako finální Optimized prompt) |

---

## H. Plán vyhodnocení

| Metrika                                          | Hlavní/vedlejší | Automatická/lidská/LLM soudce            | Výpočet                                                                                                                                                                                                   | Kalibrace nebo validace                                                                                                          | Omezení                                                                                          |
| ------------------------------------------------ | --------------- | ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| M1 – věcná relevance a kontextové použití citace | Hlavní          | Lidská (2 hodnotitelé)                   | Skóre 1–10 podle rubriky s pásmy 1–3, 4–6, 7–8, 9–10; průměr a medián za kombinaci systém × podmínka (N = 10)                                                                                             | Společná kalibrace na vývojových případech; dvojí nezávislé hodnocení 20 % odpovědí (24 ze 120) a výpočet shody                  | Subjektivita i při rubrice; nepostihuje formální správnost identifikátorů                        |
| M2a – formální přesnost DOI/ISBN                 | Vedlejší        | Automatická (`metrika2.py`)              | Počet platných unikátních identifikátorů / počet všech extrahovaných unikátních kandidátů (0,0–1,0); odpověď bez identifikátoru má stav BEZ_IDENTIFIKATORU a vykazuje se samostatně                       | Ověřeno na zkušebních výstupech; detailní CSV `identifikatory_metrika2.csv` ručně zkontrolováno kvůli falešně rozpoznaným číslům | Kontroluje jen syntaxi DOI a kontrolní součet ISBN, ne existenci záznamu ani autora, rok a název |
| M2b – shoda s referencí                          | Vedlejší        | Automatická (`metrika2.py --references`) | Jaccardova shoda nalezených a očekávaných identifikátorů (průnik / sjednocení) podle `ref_doi` a `ref_isbn` v `Testcases.xlsx`; jen u případů v režimu `match_ref`                                        | Reference ověřeny týmem ručně (Crossref, DataCite, katalogy knihoven) před během                                                 | Penalizuje i jiné správné zdroje při volné volbě literatury; ISBN-10 a ISBN-13 se nepřevádějí    |
| M3 – odmítnutí nevhodného zdroje                 | Vedlejší        | Lidská (2 hodnotitelé)                   | 0/1: model explicitně odmítl podvržený, fiktivní, stažený nebo zkresleně použitý zdroj a uvedl správný důvod; podíl úspěchů na 4 testovacích případech s `Metrics3_applicable = ANO` (B07, C07, C08, E07) | Předem stanovené `candidate_verdicts` a `should_use_source` v `Testcases.xlsx`; shoda dvou hodnotitelů                           | Malý počet případů (4 na kombinaci); binární hodnota nerozlišuje částečné odmítnutí              |

**Lidští hodnotitelé:** Daniil Astapenko a Erik Praunsperger.

**Postup zaslepení:** Odpovědi se před hodnocením zkopírují bez zadání a promptu do anonymizovaných souborů s náhodným kódem. Odstraní se zmínky prozrazující systém (název asistenta, styl odkazů typický pro produkt, kde to jde bez zásahu do obsahu). Klíč přiřazení kódů k `run_id` drží člen týmu, který nehodnotí.

**Randomizace pořadí odpovědí:** Pořadí 120 anonymizovaných odpovědí se náhodně zamíchá tak, aby se systémy ani podmínky neobjevovaly v blocích.

**Měření shody mezi hodnotiteli:** Vážený Cohenův koeficient pro ordinální M1 a Cohenův koeficient pro binární M3, počítaný na 20 % odpovědí hodnocených oběma hodnotiteli. Neshody o více než 2 body u M1 se rozhodnou diskusí.

**Byl použit LLM jako soudce?** Ne

---

## I. Pravidla pro selhání a opakování

**Co se počítá jako neúspěšný běh?**

Běh, který nevrátí použitelnou odpověď kvůli produktu nebo infrastruktuře: chybová hláška, výpadek služby, vyčerpaný limit bezplatné verze, přerušená či neúplná odpověď nebo prázdný výstup. Odpověď, která je obsahově špatná (halucinovaný zdroj, chybné DOI, převzetí podvrženého zdroje), **není** neúspěšný běh, ale řádný výsledek, který se hodnotí. Stejně tak odmítnutí úlohy modelem se hodnotí jako výsledek.

---

**Jsou opakování povolena?**

Ano, ale pouze u neúspěšných běhů z technických důvodů. Opakování probíhá v nové konverzaci se stejným promptem. Opakovat běh kvůli nespokojenosti s obsahem odpovědi je zakázáno.

---

**Maximální počet opakování:**

2 opakování (celkem nejvýše 3 pokusy). Pokud ani třetí pokus nevrátí použitelnou odpověď, běh se zaznamená jako neúspěšný a do výsledků se započítá s nulovým skóre.

---

**Jak bude vykázána úspěšnost na první pokus a celková úspěšnost?**

U každého běhu se zaznamená číslo pokusu. Ve výsledkové tabulce se uvádí podíl běhů úspěšných na první pokus a zvlášť počet běhů, které vyžadovaly opakování nebo skončily neúspěchem. Skóre metrik se počítá z prvního použitelného pokusu.

---

**Která selhání produktu nebo infrastruktury budou vyloučena a proč?**

Výpadky serveru, chyby sítě a vyčerpání limitu bezplatné verze, protože nevypovídají o schopnosti modelu pracovat s citacemi. Tato selhání se zaznamenají do logu, ale do skóre se nepromítají, pokud byl běh úspěšně zopakován. Nevylučují se odmítnutí odpovědět ani obsahové chyby.

---

### J. Kontrolní seznam logování

- [x] `run_id` ve tvaru `Systém/podmínka/číslo` (např. `ChatGPT/strukturovany/01`)
- [x] Identifikátor testovacího případu (`task_id`)
- [x] Systém (ChatGPT, Gemini, Claude, Perplexity)
- [x] Viditelný model a verze
- [x] Rozhraní (webové, bezplatná verze)
- [x] Podmínka promptu (výchozí, strukturovaný, optimalizovaný)
- [x] Úplné znění odeslaného promptu včetně úlohy a podkladů
- [x] Úplný text odpovědi modelu bez úprav
- [x] Datum testování
- [ ] Čas odeslání a přijetí odpovědi (pro odhad latence)
- [ ] Zapnuté nástroje (vyhledávání na webu, přílohy)
- [ ] Číslo pokusu a důvod případného opakování
- [ ] Chybové hlášky a technická selhání
- [x] Výsledky Metriky 2 ze skriptu (`vysledky_metrika2.csv`, `identifikatory_metrika2.csv`)
- [ ] Hodnocení Metriky 1 a 3 od obou hodnotitelů
- [ ] Anonymizační klíč (kód odpovědi ↔ `run_id`)
- [ ] Poznámky hodnotitelů a kategorie chyb pro analýzu chyb

**Místo uložení:**

GitHub repozitář `h0ldemslav/artificial-intelligence-course-pef-mendelu`, složka `assignment-1`: výstupy jako textové soubory UTF-8 ve struktuře `Systém/podmínka/číslo.txt` (např. `ChatGPT/strukturovany/01.txt`), testovací případy v `Testcases.xlsx`, kandidátní prompty ve složce `CandidatePrompts`, skript `metrika2.py` a návod `NAVOD_metrika2.txt`. Centrální tabulka s hodnocením včetně poznámek hodnocení je v souboru `models_evaluation.xlsx`.

---

**Postup anonymizace a ochrany dat:**

Testovací případy ani výstupy neobsahují osobní údaje – jde o syntetická zadání a veřejně dostupné publikace. Do promptů se nevkládají žádné osobní ani citlivé informace členů týmu. Pro hodnocení se odpovědi anonymizují (viz zaslepení v oddílu H) a klíč k anonymizaci je uložen odděleně od souborů pro hodnotitele. Účty použité k testování bezplatných verzí se v repozitáři neuvádějí.

---

## K. Pilotní ověření

**Velikost pilotu:** Validační sada 10 případů (A05–A06, B05–B06, C05–C06, D05–D06, E05–E06), na které byly porovnány kandidátní prompty A a B se strukturovaným promptem; vývoj probíhal na 20 vývojových případech.

**Co v pilotu selhalo?**

Strukturovaný prompt (v1) ponechával nepřesná tvrzení v odstavci a omezení jen konstatoval v části Nejistoty, a občas chyboval ve jméně autora nebo DOI. Kandidát B (v2) zahlcoval odpověď přehledy změn, nepřeformulovával sporné odstavce a chyboval v identifikátorech (halucinovaná číslice v DOI u B05, odkazy na vyhledávání Google místo DOI u C05).

---

**Které případy byly přepsány nebo odstraněny?**

Žádný případ nebyl odstraněn nebo přeformulován uveďte.

---

**Jaké změny metrik nebo rubriky byly provedeny?**

U Metriky 2 bylo stanoveno, že odpovědi bez identifikátoru (stav BEZ_IDENTIFIKATORU) se vykazují samostatně, a byl zaveden volitelný referenční režim s Jaccardovou shodou vůči ověřeným referencím. Pro každý případ byl v `Testcases.xlsx` určen režim hodnocení (`match_ref`, `consistency`, `no_invention`) a u Metriky 3 předem zapsány očekávané verdikty ke kandidátním zdrojům.

---

**Jaké důkazy podporují zmrazení benchmarku?**

Kandidát A dosáhl na validační sadě průměru M1 9/10, 100% správnosti DOI/ISBN a 100% úspěšnosti u hraničních případů (M3), zatímco kandidát B vykázal chyby v identifikátorech, pravděpodobně kvůli příliš striktnímu checklistu. Testovací sada zůstala během ladění nedotčena a skript pro Metriku 2 pracuje offline a deterministicky.

---

**Co zůstává nejisté?**

- Zda se výsledek pilotu přenese na testovací sadu a na všechny čtyři systémy
- Malý počet případů pro Metriku 3 (4 na kombinaci systém × podmínka)
- Stabilita modelů v bezplatných verzích a to, nakolik výsledek ovlivňuje vyhledávání na webu, které není mezi systémy sjednoceno

---

---

## L. Tabulka výsledků

| Systém     | Podmínka       | _N_ | Hlavní skóre | Interval nebo variabilita  | Vedlejší skóre                                                 | Medián latence | Náklady             | Úspěch na první pokus |
| ---------- | -------------- | --- | ------------ | -------------------------- | -------------------------------------------------------------- | -------------- | ------------------- | --------------------- |
| ChatGPT    | Výchozí        | 10  | 7,10         | SD 2,48; min–max 2–9,50    | M2 formální 1,00 (bez identifikátoru 2×); M2 ref. 1,00; M3 1/4 | neměřeno       | 0 (bezplatná verze) | 10/10                 |
| ChatGPT    | Strukturovaný  | 10  | 9,05         | SD 0,44; min–max 8,50–9,50 | M2 formální 1,00 (bez identifikátoru 1×); M2 ref. 0,86; M3 4/4 | neměřeno       | 0 (bezplatná verze) | 10/10                 |
| ChatGPT    | Optimalizovaný | 10  | 9,45         | SD 0,55; min–max 8,50–10   | M2 formální 1,00 (bez identifikátoru 2×); M2 ref. 0,83; M3 4/4 | neměřeno       | 0 (bezplatná verze) | 10/10                 |
| Gemini     | Výchozí        | 10  | 6,45         | SD 2,43; min–max 1,50–9,50 | M2 formální 1,00 (bez identifikátoru 3×); M2 ref. 0,64; M3 1/4 | neměřeno       | 0 (bezplatná verze) | 10/10                 |
| Gemini     | Strukturovaný  | 10  | 7,85         | SD 2,14; min–max 2,50–9,50 | M2 formální 1,00 (bez identifikátoru 1×); M2 ref. 0,93; M3 3/4 | neměřeno       | 0 (bezplatná verze) | 10/10                 |
| Gemini     | Optimalizovaný | 10  | 7,70         | SD 2,24; min–max 2,50–10   | M2 formální 0,94 (bez identifikátoru 1×); M2 ref. 0,86; M3 3/4 | neměřeno       | 0 (bezplatná verze) | 10/10                 |
| Claude     | Výchozí        | 10  | 6,90         | SD 2,49; min–max 2–9,50    | M2 formální 1,00 (bez identifikátoru 5×); M2 ref. 0,71; M3 2/4 | neměřeno       | 0 (bezplatná verze) | 10/10                 |
| Claude     | Strukturovaný  | 10  | 8,65         | SD 0,97; min–max 7–10      | M2 formální 1,00 (bez identifikátoru 3×); M2 ref. 0,93; M3 3/4 | neměřeno       | 0 (bezplatná verze) | 10/10                 |
| Claude     | Optimalizovaný | 10  | 9,20         | SD 1,51; min–max 5–10      | M2 formální 1,00 (bez identifikátoru 3×); M2 ref. 1,00; M3 4/4 | neměřeno       | 0 (bezplatná verze) | 10/10                 |
| Perplexity | Výchozí        | 10  | 6,80         | SD 2,36; min–max 2–9,50    | M2 formální 1,00 (bez identifikátoru 4×); M2 ref. 0,71; M3 1/4 | neměřeno       | 0 (bezplatná verze) | 10/10                 |
| Perplexity | Strukturovaný  | 10  | 8,50         | SD 0,71; min–max 7,50–9,50 | M2 formální 1,00 (bez identifikátoru 2×); M2 ref. 0,90; M3 4/4 | neměřeno       | 0 (bezplatná verze) | 10/10                 |
| Perplexity | Optimalizovaný | 10  | 9,15         | SD 0,71; min–max 7,50–10   | M2 formální 1,00 (bez identifikátoru 1×); M2 ref. 0,93; M3 4/4 | neměřeno       | 0 (bezplatná verze) | 10/10                 |

- Hlavní skóre = průměr M1 (m1_final, průměr dvou hodnotitelů, škála 1–10) přes 10 testovacích případů
- M2 formální = průměrný podíl platných DOI/ISBN u odpovědí, které identifikátor obsahují. Odpovědi bez identifikátoru jsou vykázány zvlášť
- M2 ref. = průměrná Jaccardova shoda s referenčními DOI u případů v režimu match_ref
- M3 = počet správně odmítnutých nebo rozpoznaných nevhodných zdrojů ze 4 hraničních případů (B07, C07, C08, E07)
- Latenci webová rozhraní neumožňují srovnatelně měřit
- Všechny běhy proběhly na první pokus. Shoda hodnotitelů M1: kvadraticky vážený Cohenův kappa 0,56

---

### M. Analýza chyb

| ID chyby | Systém | Podmínka | ID úlohy | Kategorie | Závažnost | První pokus? | Popis | Pravděpodobná příčina | Lze předejít promptem? |
| -------- | ------ | -------- | -------- | --------- | --------- | ------------ | ----- | --------------------- | ---------------------- |
|          |        |          |          |           |           |              |       |                       |                        |
|          |        |          |          |           |           |              |       |                       |                        |
|          |        |          |          |           |           |              |       |                       |                        |
|          |        |          |          |           |           |              |       |                       |                        |
|          |        |          |          |           |           |              |       |                       |                        |

Plánované kategorie chyb: halucinovaný zdroj, halucinované nebo chybné DOI/ISBN, chybná metadata (autor, rok, název, časopis), převzetí podvrženého nebo staženého zdroje, zdroj nepodporuje konkrétní tvrzení, nadměrně silné tvrzení, chybný formát podle ČSN ISO 690, falešné odmítnutí legitimního zdroje, poslechnutí prompt injection. Závažnost: vysoká (vymyšlený zdroj nebo převzetí podvrženého zdroje), střední (chybné metadato či identifikátor u existujícího zdroje), nízká (formátování).

**Nejčastější chyba:**

Doplní se po vyhodnocení.

---

**Nejzávažnější chyba:**

Doplní se po vyhodnocení.

---

**Změnila optimalizace rozložení chyb?**

Doplní se po vyhodnocení.

---

## N. Praktické doporučení

**Nejlepší systém pro definovanou schopnost:**

Doplní se po vyhodnocení.

---

**Nejlepší podmínka promptu:**

Doplní se po vyhodnocení.

---

**Podmínky, za kterých doporučení platí:**

Bezplatné webové verze systémů ve stavu k 12. 10. 2026, české odborné texty, úlohy typu doplnění, výběr a kontrola citací podle ČSN ISO 690, prompt v neměněném znění z oddílu F.

---

**Důležitý kompromis mezi náklady, latencí a lidskou prací:**

Všechny testované verze jsou bezplatné, takže hlavní náklad představuje lidská práce. Delší strukturovaný a optimalizovaný prompt vede k delším odpovědím, které se déle čtou, ale oddělují nejistoty a nepoužité zdroje, a tím usnadňují kontrolu. Žádný systém neodstraňuje potřebu ručně ověřit každou citaci v databázi (Crossref, katalog knihovny) před použitím v práci.

---

**Co by si z této studie praktik neměl vyvozovat?**

Že AI asistent může citace ověřovat místo člověka; že výsledek platí pro placené verze, API nebo pozdější verze modelů; že platí pro jiné jazyky, obory nebo citační normy; že pořadí systémů je statisticky průkazné (N = 10 na kombinaci); že syntakticky platné DOI znamená existující a správně přiřazený zdroj.

---

## O. Validita a omezení

**Konceptuální validita: Měříme zamýšlenou schopnost?**

Úlohy pokrývají tři složky schopnosti (výběr zdroje, kritické odmítnutí, správné identifikátory) a každé odpovídá samostatná metrika. Metrika 2 však měří jen formální platnost identifikátorů, nikoli existenci zdroje a správnost dalších metadat. Referenční režim to zmírňuje jen u případů s jednoznačně očekávaným zdrojem. Metrika 1 závisí na kvalitě rubriky a úsudku hodnotitelů.

---

**Vnitřní validita: mohl výsledek způsobit jiný faktor?**

Rozdíly mezi systémy mohou být způsobeny přístupem k webu, skrytými systémovými prompty nebo rozdílnou délkou odpovědí, nikoli samotnou schopností modelu. Rozdíly mezi podmínkami mohou částečně odrážet pouze delší a strukturovanější výstup, který hodnotitelé vnímají příznivěji. Zapamatování vysoce citovaných prací (alternativní vysvětlení) může překrýt vliv promptu.

---

**Vnější validita: kde se výsledek nemusí zobecnit?**

Na placené verze a API, na jiné jazyky a citační normy, na delší texty s mnoha citacemi, na obory nezastoupené v datasetu a na reálné případy s méně známými zdroji (v datasetu převažují vysoce citované práce).

---

**Statistická nejistota nebo omezení velikosti vzorku:**

Na každou kombinaci systém × podmínka připadá jen 10 testovacích případů a u Metriky 3 jen 4. Rozdíly o 1–2 body na škále M1 nebudou statisticky průkazné. Výsledky proto budou uváděny s rozptylem nebo intervalem a interpretovány jako orientační; každý běh je jednorázový, takže nezachycujeme variabilitu odpovědí téhož modelu.

---

**Posun verzí produktu nebo modelu:**

Bezplatné verze mohou měnit model bez oznámení; testování proběhlo v jediném dni (12. 10. 2026) a zaznamenali jsme viditelnou verzi modelu, kde to bylo možné. Opakování studie v jiném termínu může přinést jiné výsledky.

---

**Zkreslení hodnocení nebo soudce:**

Hodnotitelé jsou zároveň autory testovacích případů a promptů, a mohou proto nevědomky zvýhodňovat optimalizovaný prompt. Zmírňujeme to zaslepením, náhodným pořadím a měřením shody dvou hodnotitelů. Úplné zaslepení není možné, protože strukturovaný a optimalizovaný prompt mají rozpoznatelný formát odpovědi (čtyři části).

---

**Nejdůležitější navazující experiment:**

Zopakovat test přes API se sjednoceným nastavením (pevná teplota, vyhledávání na webu záměrně zapnuté a vypnuté u všech systémů), aby bylo možné oddělit vliv přístupu k webu od vlivu modelu.

Současně rozšířit sadu o více málo citovaných českých zdrojů a provést opakované běhy pro odhad variability.
