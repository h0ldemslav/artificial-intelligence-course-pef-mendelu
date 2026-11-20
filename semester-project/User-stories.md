# Odvozené uživatelské příběhy – MVP registračního systému akcí

Tento dokument je **jediným zadáním, které dostávají všechny tři varianty** (MAS A, MAS B, single agent C). Původní zadání organizace se agentům nepředává. Příběhy jsou z něj odvozené a formulované vlastními slovy. Pokrývají pouze rozsah MVP F1–F9 z project proposalu (kap. 5).

Formát:
- **ID** `US-Fx.y`: funkce F1–F9 a pořadí příběhu.
- **Priorita:** **Must** = nutné pro MVP, **Should** = důležité, ale MVP bez nich obstojí, **Could** = jen pokud zbude čas.
- **Akceptační kritéria (AK)** jsou ve tvaru *Za předpokladu / Když / Pak*, aby se z nich daly přímo psát testy.

---

## 0. Slovníček a role

| Pojem | Význam |
|---|---|
| **Akce** | Jedna skautská akce (např. sraz nebo setkání). Každá akce má vlastní oddělená data a nastavení. Akce si data nesdílejí. |
| **Registrace** | Účast jedné osoby na jedné akci v určité roli. |
| **Skupina** | Skupina účastníků akce s jedním zodpovědným vedoucím. Typicky oddíl s dětmi. |
| **Program** | Programový blok akce s časem, místem a kapacitou. Účastníci se na něj přihlašují. |
| **Identifikační kód** | Náhodný unikátní kód registrace, např. pro propojení s externími aplikacemi. |
| **Kategorie údajů** | Registrační údaje jsou rozdělené do 4 kategorií: **základní**, **kontaktní**, **zdravotní**, **stravovací omezení**. Kategorie jsou základem řízení přístupu. |
| **Plnoletost** | Věk alespoň 18 let **k datu začátku akce**, počítaný z data narození. |

Role:

| Role | Kdo to je |
|---|---|
| **Účastník** | Osoba, která se na akci registruje sama za sebe. |
| **Vedoucí skupiny** | Plnoletá osoba, která zodpovídá za skupinu účastníků. |
| **Lektor** | Osoba, která vede program. |
| **Zdravotník** | Člen týmu akce, který potřebuje znát zdravotní údaje. |
| **Pořadatel** | Spravuje akci. Vidí a upravuje vše v rámci své akce. |
| **Administrátor** | Spravuje celý systém, zakládá akce a přiřazuje pořadatele. |

---

## F1 – Uživatelský účet a přihlášení

Do systému se lze přihlásit **pouze přes skautIS**. Přihlášení e-mailem ani účty bez skautISu MVP neumožňuje. V MVP se skautIS **simuluje** (mock), skutečné napojení je mimo rozsah.

### US-F1.1 Přihlášení přes skautIS (simulace) · Must
**Jako** člen skautské organizace **chci** se přihlásit přes skautIS, **abych** nemusel/a zakládat další účet a údaje o mně se předvyplnily.

AK:
1. Přihlašovací stránka nabízí jedinou volbu: „Přihlásit přes skautIS (simulace)“. Formulář pro e-mail a heslo neexistuje.
2. Simulace nabídne výběr z předem připravených smyšlených osob. Každá má jméno, příjmení, datum narození, e-mail a jednotku.
3. Když vyberu osobu poprvé, systém mi založí účet a přihlásí mě. Při dalším přihlášení stejnou osobou se použije stejný účet.
4. Po přihlášení má registrační formulář předvyplněné údaje z „skautISu“ (jméno, příjmení, datum narození, e-mail). Mohu je zkontrolovat a doplnit chybějící.
5. Simulace se nepřipojuje k žádnému reálnému systému.

### US-F1.2 Odhlášení a ochrana stránek · Must
**Jako** uživatel **chci** se odhlásit a mít jistotu, že bez přihlášení nikdo neuvidí moje údaje, **aby** byly chráněné i na sdíleném zařízení.

AK:
1. Když se odhlásím, pak už nemám přístup na stránky ani data vyžadující přihlášení.
2. Nepřihlášený uživatel, který otevře chráněnou stránku, je přesměrován na přihlášení.
3. Veřejně dostupné bez přihlášení je jen: přihlašovací stránka, informace o akci a seznam programů (US-F7.2).

---

## F2 – Registrace jednotlivce na akci

### US-F2.1 Registrace na akci · Must
**Jako** účastník **chci** vyplnit registrační formulář akce, **abych** byl/a na akci přihlášen/a.

AK:
1. Za předpokladu, že je registrace na akci otevřená, mohu si vybrat jednu z rolí, které pořadatel pro registraci zpřístupnil (minimálně účastník, vedoucí skupiny, lektor).
2. Formulář je rozdělený do 4 kategorií:
   - **základní** (jméno, příjmení, datum narození),
   - **kontaktní** (e-mail, telefon),
   - **zdravotní** (zdravotní omezení, alergie, léky),
   - **stravovací omezení** (např. vegetarián, bezlepková strava).
3. Povinná pole jsou viditelně označena. Když povinné pole nevyplním, registraci nelze dokončit a chyba se zobrazí u pole.
4. Validace:
   - e-mail musí mít platný formát,
   - telefon musí mít platný formát,
   - datum narození nesmí být v budoucnosti.
5. Po dokončení registrace vidím potvrzení a stav registrace „dokončená“.

### US-F2.2 Jedna registrace na osobu a akci · Must
**Jako** pořadatel **chci**, aby každá osoba měla na akci nejvýše jednu registraci, **abych** neměl/a v datech duplicity.

AK:
1. Když se už registrovaný uživatel pokusí registrovat znovu na stejnou akci, pak systém novou registraci nevytvoří a zobrazí jeho stávající registraci.
2. Ani při souběžném odeslání stejného formuláře (např. dvojklik nebo dva otevřené panely) nevznikne duplicitní registrace.

### US-F2.3 Časové okno registrace · Must
**Jako** pořadatel **chci** nastavit, od kdy do kdy je registrace otevřená, **aby** se nikdo nepřihlásil mimo stanovený termín.

AK:
1. Před začátkem a po konci registračního okna formulář nelze odeslat a stránka zobrazí, kdy se registrace otevírá nebo že je uzavřená.
2. Kontrola okna probíhá na serveru, nejen v prohlížeči.

### US-F2.4 Úprava vlastních údajů · Should
**Jako** účastník **chci** po registraci upravit své údaje, **abych** mohl/a opravit chybu nebo doplnit změnu.

AK:
1. Dokud je registrace otevřená, mohu upravit své údaje ve všech kategoriích.
2. Po uzavření registrace se mi údaje zobrazují jen pro čtení.
3. Každá změna se zapíše do historie operací (F9).

### US-F2.5 Kapacita akce · Should
**Jako** pořadatel **chci** nastavit maximální počet registrací na akci, **aby** akce nepřekročila svou kapacitu.

AK:
1. Když je kapacita naplněna, další registraci nelze dokončit a uživatel vidí hlášku „Kapacita akce je naplněna“.
2. Ani při souběžném registrování mnoha lidí počet dokončených registrací nepřekročí kapacitu.

---

## F3 – Unikátní identifikační kód

### US-F3.1 Přidělení kódu · Must
**Jako** pořadatel **chci**, aby každá registrace dostala unikátní identifikační kód, **abych** mohl/a osobu jednoznačně dohledat a propojit s jinými nástroji.

AK:
1. Kód se vygeneruje automaticky při dokončení registrace.
2. Kód je **náhodný**:
   - není odvozený od pořadí záznamu v databázi,
   - dvě po sobě jdoucí registrace nemají „sousední“ kódy.
3. Kód je unikátní v rámci celého systému.
4. Kód je krátký a dobře opsatelný: 8 znaků, velká písmena a číslice, bez snadno zaměnitelných znaků (0/O, 1/I/L).
5. Kód se po přidělení nemění.

### US-F3.2 Zobrazení kódu · Must
**Jako** účastník **chci** vidět svůj kód v profilu, **abych** ho mohl/a použít nebo nadiktovat.

AK:
1. Kód je viditelný v mém profilu registrace.
2. Kód vidí i pořadatel a role s přístupem k základním údajům (F6) v přehledu a detailu účastníka.
3. Podle kódu lze účastníka vyhledat ve správě akce (F8).

---

## F4 – Skupiny a vedoucí

### US-F4.1 Založení skupiny · Must
**Jako** vedoucí skupiny **chci** založit skupinu na akci, **abych** do ní mohl/a sdružit své členy.

AK:
1. Skupinu může založit pouze uživatel registrovaný na akci v roli **vedoucí skupiny**.
2. Při založení zadám název skupiny. Systém vygeneruje **kód skupiny** pro připojení: náhodný, unikátní v rámci akce, nesouvisející s identifikačním kódem osoby.
3. Zakladatel je automaticky vedoucím skupiny.
4. Kód skupiny vidím v detailu skupiny a mohu ho poslat členům.

### US-F4.2 Připojení do skupiny kódem · Must
**Jako** účastník **chci** se připojit do skupiny zadáním kódu, **aby** bylo jasné, ke kterému vedoucímu patřím.

AK:
1. Když při registraci nebo později zadám platný kód skupiny, pak se stanu členem této skupiny.
2. Když zadám neplatný kód, pak se zobrazí chyba a do žádné skupiny nejsem přiřazen/a.
3. Účastník může být na jedné akci členem nejvýše jedné skupiny.
4. Pokud má skupina nastavený maximální počet členů a je plná, připojení se odmítne s hláškou „Skupina je plná“.

### US-F4.3 Správa členů skupiny · Must
**Jako** vedoucí skupiny **chci** vidět a spravovat členy své skupiny, **abych** měl/a přehled, za koho zodpovídám.

AK:
1. V detailu skupiny vidím seznam členů s jejich identifikačním kódem a věkem k začátku akce.
2. Mohu člena ze skupiny odebrat. Odebraný nezletilý člen se dostane do stavu „čeká na skupinu“ (viz F5).
3. Vidím jen členy **své** skupiny, ne členy jiných skupin.
4. Každé připojení i odebrání člena se zapíše do historie operací (F9).

### US-F4.4 Nastavení skupin pořadatelem · Should
**Jako** pořadatel **chci** nastavit maximální počet členů skupiny, **aby** skupiny odpovídaly možnostem akce.

AK:
1. Pořadatel může pro akci nastavit maximální počet členů skupiny, případně ho nechat neomezený.
2. Nastavení se uplatní při každém připojení do skupiny (US-F4.2, AK 4).

---

## F5 – Pravidlo pro nezletilé

### US-F5.1 Nezletilý musí mít skupinu s plnoletým vedoucím · Must
**Jako** pořadatel **chci**, aby žádný nezletilý účastník nebyl na akci bez zodpovědného plnoletého vedoucího, **abych** u každého dítěte věděl/a, kdo za něj zodpovídá.

AK:
1. Věk se počítá z data narození **k datu začátku akce**.
2. Když je účastníkovi méně než 18 let a nezadá platný kód skupiny, pak registraci **nelze dokončit**. Zůstane ve stavu „čeká na skupinu“ a systém vysvětlí proč.
3. Když se nezletilý připojí do skupiny, jejíž vedoucí je plnoletý, pak lze registraci dokončit.
4. Když je nezletilý ze skupiny odebrán, jeho registrace se vrátí do stavu „čeká na skupinu“ a pořadatel ho vidí ve filtru „nezletilí bez skupiny“ (F8).
5. Pravidlo se kontroluje na serveru. Nejde ho obejít přímým voláním API.

### US-F5.2 Vedoucí skupiny musí být plnoletý · Must
**Jako** pořadatel **chci**, aby skupinu mohl vést jen plnoletý člověk, **aby** odpovědnost za děti nesla dospělá osoba.

AK:
1. Když se osoba mladší 18 let (k začátku akce) pokusí registrovat v roli vedoucí skupiny, pak to systém odmítne s vysvětlením.
2. Nezletilá osoba nemůže založit skupinu.
3. Pokud by se vedoucímu změnilo datum narození tak, že by byl nezletilý, změna se odmítne, dokud má skupinu s členy.

---

## F6 – Role a oprávnění

### US-F6.1 Přístup k údajům podle kategorií · Must
**Jako** organizace **chci**, aby každá role viděla jen ty kategorie údajů, které nutně potřebuje, **abychom** chránili osobní údaje, hlavně údaje dětí.

AK: přístup se řídí touto maticí.

| Role | Koho vidí | Základní | Kontaktní | Zdravotní | Stravovací |
|---|---|:-:|:-:|:-:|:-:|
| Účastník | jen sebe | ✔ | ✔ | ✔ | ✔ |
| Vedoucí skupiny | sebe + členy své skupiny | ✔ | ✔ | ✔ * | ✔ |
| Lektor | účastníky přihlášené na svůj program | ✔ | ✘ | ✘ | ✘ |
| Zdravotník | všechny registrované na akci | ✔ | ✔ | ✔ | ✘ |
| Pořadatel | všechny registrované na své akci | ✔ | ✔ | ✔ | ✔ |
| Administrátor | všechny ve všech akcích | ✔ | ✔ | ✔ | ✔ |

\* *Předpoklad týmu, který je potřeba ověřit s organizací:* vedoucí zodpovídá za nezletilé, proto potřebuje znát jejich zdravotní údaje.

1. Oprávnění se kontrolují **na serveru** u každého požadavku, nejen skrytím prvků v UI.
2. Když se role pokusí získat kategorii, ke které nemá přístup (přes UI, URL nebo API), pak dostane odmítnutí (HTTP 403) a údaje se nevrátí.
3. Uživatel jedné akce nevidí žádná data jiné akce, pokud tam nemá roli.

### US-F6.2 Přiřazení rolí pořadatelem · Must
**Jako** pořadatel **chci** přiřadit registrované osobě roli zdravotníka nebo pořadatele, **abych** mohl/a sestavit tým akce.

AK:
1. Pořadatel může registrované osobě na své akci přiřadit nebo odebrat roli zdravotník nebo pořadatel.
2. Role vedoucí skupiny, lektor a účastník vznikají při registraci (F2). Pořadatel je může změnit, přičemž stále platí pravidla F5.
3. Pořadatele akce určuje administrátor (US-F8.1).
4. Každá změna role se zapíše do historie operací (F9).

### US-F6.3 Lektor vidí účastníky svého programu · Should
**Jako** lektor **chci** vidět seznam lidí přihlášených na můj program, **abych** věděl/a, s kým počítat.

AK:
1. Lektor vidí jméno, příjmení a identifikační kód účastníků přihlášených na programy, u kterých je uveden jako lektor.
2. Účastníky jiných programů ani jejich další kategorie údajů nevidí.

---

## F7 – Programy s kapacitou

### US-F7.1 Vytvoření programu · Must
**Jako** pořadatel **chci** vytvořit program akce, **aby** si účastníci mohli vybrat, čeho se zúčastní.

AK:
1. Program má povinně název, začátek, konec, místo a kapacitu (celé kladné číslo). Volitelně má popis, lektora (registrovaná osoba v roli lektor) a seznam rolí, pro které je dostupný.
2. Konec programu musí být po jeho začátku.
3. Pořadatel může program upravit nebo smazat. Kapacitu nelze snížit pod aktuální počet přihlášených.

### US-F7.2 Veřejný přehled programů · Should
**Jako** zájemce o akci **chci** vidět programy ještě před přihlášením, **abych** se mohl/a rozhodnout, jestli na akci jet.

AK:
1. Seznam programů akce (název, popis, čas, místo, volná místa) je dostupný i bez přihlášení.
2. Na veřejné stránce se nezobrazují žádné osobní údaje přihlášených.

### US-F7.3 Přihlášení na program · Must
**Jako** registrovaný účastník **chci** se přihlásit na program, **abych** měl/a jisté místo.

AK:
1. Přihlásit se lze jen s dokončenou registrací na akci a jen v časovém okně výběru programů, které nastavil pořadatel.
2. Když je program dostupný pro mou roli a má volné místo, pak jsem přihlášen/a a počet volných míst se sníží.
3. Když je program plný, přihlášení se odmítne s hláškou „Program je obsazen“.
4. Když se program časově překrývá s jiným programem, na který jsem přihlášen/a, přihlášení se odmítne s uvedením kolize.
5. Na stejný program se nelze přihlásit dvakrát.
6. Z programu se mohu odhlásit, dokud je okno výběru otevřené. Místo se uvolní.

### US-F7.4 Žádné přečerpání kapacity při náporu · Must
**Jako** pořadatel **chci**, aby program nikdy nepřekročil svou kapacitu ani při otevření výběru, kdy se hlásí stovky lidí najednou, **abych** nemusel/a nikoho dodatečně odhlašovat.

AK:
1. Za předpokladu, že se 300 uživatelů během 60 sekund současně hlásí na program s kapacitou 20, pak je po skončení přihlášeno **přesně 20** osob (ne více) a žádná osoba není přihlášena dvakrát.
2. Uživatelé, na které nevyšlo místo, dostanou srozumitelnou odpověď „Program je obsazen“, ne chybu serveru.
3. Kontrola kapacity je zajištěna na úrovni databáze nebo transakce, ne jen kontrolou v aplikaci před zápisem.

### US-F7.5 Můj harmonogram · Should
**Jako** účastník **chci** vidět přehled programů, na které jsem přihlášen/a, seřazený podle času, **abych** věděl/a, kde mám kdy být.

AK:
1. Harmonogram obsahuje všechny moje programy s názvem, časem a místem, seřazené chronologicky.
2. Z harmonogramu se dostanu na detail programu.

---

## F8 – Administrace akce

### US-F8.1 Založení akce administrátorem · Must
**Jako** administrátor **chci** založit akci a určit jejího hlavního pořadatele, **aby** mohla začít registrace.

AK:
1. Akce má povinně název, datum začátku, datum konce, registrační okno (od–do) a hlavního pořadatele.
2. Pořadatele lze později změnit.
3. Každá akce má svá data oddělená od ostatních akcí.

### US-F8.2 Přehled účastníků a skupin · Must
**Jako** pořadatel **chci** tabulkový přehled všech registrovaných a skupin, **abych** měl/a akci pod kontrolou na jednom místě.

AK:
1. Přehled zobrazuje jméno, identifikační kód, roli, skupinu, věk k začátku akce a stav registrace.
2. Lze filtrovat podle role, skupiny, stavu registrace a podle příznaku „nezletilí bez skupiny“.
3. Lze vyhledávat podle jména, e-mailu a identifikačního kódu.
4. Přehled skupin zobrazuje název, vedoucího a počet členů.
5. Přehled reaguje do 1 s i při 2 000 registracích na akci.
6. Zobrazené sloupce respektují oprávnění role (F6). Zdravotník tedy uvidí jen to, k čemu má přístup.

### US-F8.3 Detail účastníka · Should
**Jako** pořadatel **chci** otevřít detail účastníka, **abych** viděl/a všechny jeho údaje na jednom místě.

AK:
1. Detail obsahuje:
   - údaje rozdělené podle kategorií,
   - identifikační kód,
   - skupinu,
   - roli,
   - programy, na které je přihlášen.
2. Každá role v detailu vidí jen kategorie, ke kterým má přístup (F6).

### US-F8.4 Export s výběrem sloupců · Must
**Jako** pořadatel **chci** exportovat přehled do CSV a vybrat si, které sloupce v něm budou, **aby** ze systému odcházelo jen tolik dat, kolik opravdu potřebuji.

AK:
1. Před exportem musím výslovně vybrat sloupce. Ve výchozím stavu není vybrán žádný.
2. Nabízeny jsou jen sloupce z kategorií, ke kterým má moje role přístup.
3. Export respektuje aktuálně nastavené filtry.
4. CSV je v kódování UTF-8 a správně zobrazuje českou diakritiku.
5. Každý export se zapíše do historie operací včetně seznamu exportovaných sloupců (F9).

---

## F9 – Historie operací

### US-F9.1 Záznam operací · Must
**Jako** organizace **chci** mít dohledatelnou historii změn, **abychom** v případě problému věděli, kdo, kdy a co udělal s osobními údaji.

AK:
1. Zaznamenávají se tyto operace:
   - vytvoření registrace,
   - změna registrace a osobních údajů,
   - změna role,
   - připojení a odebrání ze skupiny,
   - přihlášení a odhlášení z programu,
   - export.
2. Každý záznam obsahuje:
   - čas,
   - kdo operaci provedl,
   - jakého účastníka nebo objektu se týká,
   - typ operace,
   - popis změny: u změn údajů které pole se změnilo, u exportu které sloupce se exportovaly.
3. Do záznamu se **neukládají hodnoty zdravotních údajů**, jen informace, že se pole změnilo.
4. Záznamy nelze přes aplikaci upravit ani smazat.

### US-F9.2 Prohlížení historie · Should
**Jako** pořadatel **chci** procházet historii operací své akce, **abych** mohl/a dohledat změny.

AK:
1. Historii vidí jen pořadatel dané akce a administrátor.
2. Lze filtrovat podle typu operace, uživatele, který operaci provedl, a podle dotčeného účastníka.
3. Záznamy jsou řazené od nejnovějšího.

---

## Volitelné příběhy (Could)

### US-X.1 Výzva k platbě s QR kódem · Could
**Jako** účastník **chci** po registraci dostat výzvu k platbě s QR kódem, **abych** mohl/a rychle zaplatit.

AK:
1. Pořadatel u akce nastaví poplatek, číslo účtu a prefix variabilního symbolu.
2. Po dokončení registrace systém vygeneruje výzvu k platbě: částku, číslo účtu, unikátní variabilní symbol, datum splatnosti a QR kód ve formátu QR Platba (SPD).
3. Výzva je dostupná v profilu účastníka. Napojení na banku a párování plateb **není** součástí MVP.

### US-X.2 Potvrzovací e-mail · Could
**Jako** účastník **chci** po registraci dostat potvrzovací e-mail, **abych** měl/a jistotu, že registrace proběhla.

AK:
1. Po dokončení registrace se odešle e-mail se shrnutím a identifikačním kódem.
2. E-maily jdou přes testovací službu (např. Mailpit nebo Mailtrap), ne na reálné adresy.

---

## Nefunkční požadavky (platí pro všechny příběhy)

| ID | Požadavek | Ověření |
|---|---|---|
| NFR-1 | **Odezva:** běžné stránky a formuláře se načtou do 1 s (p95), i pod zátěží výběru programů. | M13 |
| NFR-2 | **Integrita dat při náporu:** žádné přečerpání kapacity a žádné duplicitní registrace. | M11, M12 |
| NFR-3 | **Responzivita:** plně použitelné na mobilu, tabletu i desktopu, ovladatelné dotykem. Podporované prohlížeče: Chrome, Firefox, Safari, Edge. | M15, M18 |
| NFR-4 | **Přístupnost:** principy WCAG (popisky formulářových polí, ovládání klávesnicí, logické pořadí, alternativní texty, dostatečný kontrast). | M16, M17a |
| NFR-5 | **Bezpečnost:** oprávnění kontrolována na serveru, hesla hashovaná, ochrana proti běžným útokům (SQL injection, XSS, CSRF), žádné tajné klíče v repozitáři. | M9, M10 |
| NFR-6 | **Ochrana údajů:** pouze **smyšlená testovací data**, žádné reálné osobní údaje. Návrh počítá s uložením dat v EU. | revize |
| NFR-7 | **Jazyk:** uživatelské rozhraní v češtině. | revize |
| NFR-8 | **Převzatelnost:** běžné a rozšířené technologie. Projekt jde spustit lokálně jedním příkazem (např. `docker compose up`) podle README a obsahuje skript s ukázkovými daty (akce, programy, testové osoby ve všech rolích). | M23, M24 |
| NFR-9 | **Testy a CI:** automatické testy se spouštějí v GitHub Actions. | M4–M6 |

---

## Mimo rozsah MVP

Tyto části zadání agenti **neimplementují:**
- přihlášení e-mailem a účty pro osoby bez skautISu (hosté),
- reálné napojení na skautIS a na banku, párování plateb, vratky, potvrzení o platbě,
- stravování a přítomnost na akci, merch, podakce,
- vlastní otázky ve formuláři a podmíněná logika polí,
- skupiny spravované vedoucím s importem členů,
- převody a odhlášení registrací správcem, štítky,
- hromadné e-maily, import externích dat, export do skautISu,
- vizuální přizpůsobení akce (barvy, logo), archivace akcí, vlastní role,
- listina zájemců o plný program, export XLSX.

---

## Přehled příběhů

| Funkce | Must | Should | Could |
|---|---|---|---|
| F1 Účet a přihlášení | US-F1.1, F1.2 | – | – |
| F2 Registrace jednotlivce | US-F2.1, F2.2, F2.3 | US-F2.4, F2.5 | – |
| F3 Identifikační kód | US-F3.1, F3.2 | – | – |
| F4 Skupiny a vedoucí | US-F4.1, F4.2, F4.3 | US-F4.4 | – |
| F5 Pravidlo pro nezletilé | US-F5.1, F5.2 | – | – |
| F6 Role a oprávnění | US-F6.1, F6.2 | US-F6.3 | – |
| F7 Programy s kapacitou | US-F7.1, F7.3, F7.4 | US-F7.2, F7.5 | – |
| F8 Administrace akce | US-F8.1, F8.2, F8.4 | US-F8.3 | – |
| F9 Historie operací | US-F9.1 | US-F9.2 | – |
| Volitelné | – | – | US-X.1, X.2 |
| **Celkem** | **21** | **9** | **2** |
