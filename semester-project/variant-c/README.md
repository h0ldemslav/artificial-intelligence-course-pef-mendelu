# Varianta C – OpenHands, příprava prostředí

Tato složka obsahuje reprodukovatelné skripty a stav nastavení single agenta.
Neobsahuje implementaci MVP. Ostrý experiment dosud nezačal a úkol nastavení
prostředí ještě není dokončený.

## Aktuální stav k 22. 11. 2026

- Docker Desktop 4.99.0 / Engine 29.9.3, WSL 3.0.5.0, Windows x64.
- OpenHands Agent Canvas 1.43.0; agent-server a SDK 1.63.1; LiteLLM 1.108.13.
- Model `gemini/gemini-3.8-flash` přes Google AI Studio, Free tier.
- Limity projektu: 5 RPM, 250 000 TPM, 20 RPD. Při zkoušce nastalo přetížení
  HTTP 503 a později potvrzené vyčerpání denního limitu HTTP 429.
- Pracovní repozitář je samostatný lokální Git repozitář na větvi `variant-c`.
  Git byl ověřený jako čistý z Windows i kontejneru. Vývoj MVP ještě nezačal.
- Zákaz vestavěných delegovacích nástrojů je ověřený přes API, po otevření UI
  i na skutečném exportu. Založení session musí probíhat přiloženým launcherem.
- Úspěšné dokončení celé zkušební session a zachování dat po restartu ještě
  zbývají. Do obnovy denní kvóty se další požadavky modelu neposílají.

Číselné důkazy bez klíčů a obsahu konverzací: [evidence](evidence/setup-2026-11-22.json).

## Oddělení od ostatních variant

Toto je sdílená konfigurace přípravy, nikoli pracovní adresář ostrého agenta.
Do kontejneru připojit pouze samostatný repozitář varianty C, nikdy kořen tohoto
školního repozitáře, řešení jiných variant, deník hodnotitele nebo skryté testy.
Surové exporty, provozní stav a klíče uchovávat mimo agentův workspace i veřejný Git.
Další vývoj a zveřejnění implementace varianty C se nastaví zvlášť před ostrým během.

## Spuštění prostředí na Windows

Vyžaduje Docker Desktop s běžícím Linux enginem, Git a pro skripty Python 3.10+
(ověřeno na hostitelském Pythonu 3.14.6; bez externích Python závislostí).

V **cmd**, z této složky, předej skutečnou cestu k již připravenému samostatnému
repozitáři varianty C, např.:

```cmd
Start-OpenHands-C.cmd "C:\projects\variant-c-workspace"
```

Skript nic neinstaluje a existující kontejner nepřepisuje. Připojí zadaný
repozitář do `/projects/variant-c`, port pouze na `127.0.0.1:8000` a trvalý
svazek `openhands-c-state` do `/home/openhands/.openhands`. Používá digest
ověřeného obrazu 1.43.0, nikoli `latest`. Nový týmový počítač musí pracovní
repozitář nejprve připravit podle společně schválené struktury v metodice.

Existující zastavený kontejner lze z **cmd**, v libovolném adresáři, obnovit:

```cmd
docker start openhands-c-setup
```

Otevři `http://localhost:8000/canvas`. Nastav OpenHands jako agenta a LLM profil
`gemini-3.8-flash` s Custom Model `gemini/gemini-3.8-flash`; Base URL ponech
prázdné. Klíč zadávej jen do lokálního formuláře, nikdy do commitu ani chatu.

V profilu `default` vyber přesně `file_editor`, `task_tracker`, `terminal`
a `browser_tool_set`. `task_tool_set` a `switch_llm` musí být vypnuté,
Model Router Off, souběžnost nástrojů 1. Pro krátkou zkoušku byly vypnuté
Condenser a Critic. Jejich finální nastavení sladit pro všechny varianty.

Při problému Gitu s vlastnictvím povol pouze konkrétní workspace uvnitř
kontejneru, z **cmd** v libovolném adresáři:

```cmd
docker exec openhands-c-setup git config --global --add safe.directory /projects/variant-c
```

Pokud `git diff` ukazuje pouze změny módů souborů `100644`/`100755` způsobené
Windows bind mountem, nastav lokálně v tomto pracovním repozitáři
`git config --local core.fileMode false`. Nezaměňovat za skutečné změny obsahu.

## Vytvoření session bez delegování

Samotné vypnutí `task_tool_set` nestačí. Canvas 1.43.0 přidává nezávisle
klientský nástroj `launch_child_conversation`. Launcher používá podporované
`POST /api/conversations` s `client_tools: []`, `agent_definitions: []`,
vypnutým automatickým názvem a bez úvodní zprávy. Nemění oficiální Docker obraz.

V **cmd**, z této složky:

```cmd
python tools\create_single_agent_trial.py --output local\trial-proof-01.json
```

Otevři URL vypsanou skriptem, případně použij `localhost` místo `127.0.0.1`.
Nové session nevytvářej standardním tlačítkem UI: delegovací nástroj by se vrátil.
Po změně verze nebo nastavení znovu ověř skutečné nástroje session/exportu.
Vyloučení delegovacích nástrojů není OS-level zákaz všech možných procesů
nebo síťových požadavků přes terminál.

Pro diagnostiku dlouhého čekání je připravený režim:

```cmd
python tools\create_single_agent_trial.py --fail-fast --output local\diagnostic-proof-01.json
```

Ten materializuje stejný profil, ale spouští explicitní `agent_settings`, protože
SDK při `agent_profile_id` vynucuje streamování. Nastaví `stream=false`,
`num_retries=0`, `timeout=45 s`, `stream_idle_timeout=30 s`; zachová model
i `reasoning_effort=high`. Ve skutečném testu zobrazil denní limit za 3,53 s.
Klíč používá pouze v paměti a v autentizovaném localhost API, důkazový soubor
jej neobsahuje. Existující důkazový soubor nepřepisuje; zvol nové jméno.

Oba režimy jsou pouze příprava: `max_iterations=20`, bez autotitle a LLM
security analyzátoru. Krátký timeout může přerušit i legitimní delší odpověď.
Před ostrým během sladit tyto odchylky, pravidla potvrzování a rozpočty s týmem.
Žádný z těchto příkazů sám neodesílá úvodní zprávu modelu.

## Export a metriky

Ověřený postup v UI: tři tečky u názvu konverzace → **Download conversation data**.
Stažený ZIP obsahuje `base_state.json`, `meta.json`, JSON události v `events/`
a zvláštní protokol terminálu `bash_events/`. Export uložit mimo agentův workspace.
Obsah exportu nepublikovat bez kontroly: může obsahovat tajné údaje.

V **cmd**, z této složky:

```cmd
python tools\analyze_openhands_export.py "C:\private-runs\conversation.zip" --output local\summary-01.json
```

Skript nic nerozbaluje do souborového systému a nevypisuje prompty ani klíče.

| Veličina | Ověřený zdroj / omezení |
| --- | --- |
| Akce agenta | Počet `ActionEvent`; není to počet shell příkazů ani modelových volání. |
| Lidské zprávy | `MessageEvent` se `source=user`; doplnit oddělené InterruptEvent/PauseEvent. |
| M20 | Klasifikace v deníku milníků podle společné metodiky, nikoli prostý počet zpráv. Přípravu nezapočítávat do ostrého běhu. |
| Zaznamenané odpovědi modelu | Unikátní `response_id` v `base_state.stats.usage_to_metrics.*.token_usages`; neobsahuje nutně všechny neúspěšné pokusy. |
| Tokeny | Jeden konečný snapshot `accumulated_token_usage` pro každé usage ID. Nepřičítat k němu kumulativní snapshoty z událostí. Reasoning tokeny automaticky nepřičítat podruhé. |
| Čas | Rozsah timestampů a odděleně intervaly `execution_status=running`; není to čistý čas generování. |
| Náklady | `accumulated_cost` je reportovaná hodnota, nikoli účtenka poskytovatele; na Free tieru může ukazovat ceníkový odhad. |
| Limity/chyby | Chybové události a deník. Dva chybové záznamy nejsou automaticky dva API pokusy. |

Nezjištěné hodnoty zůstávají `null`, nikoli nula. Nulové interní čítače po
přerušeném požadavku nedokládají nulovou spotřebu poskytovatele.

## Co ještě dokončit před uzavřením Planner úkolu

1. Po obnově kvóty úspěšně dokončit read-only test repozitáře a odpověď agenta.
2. Ověřit zachování session, konfigurace a logů po restartu kontejneru.
3. Doplnit úplné logování API pokusů včetně opakování a pomocných volání pro M22.
4. Sladit ostrou konfiguraci se společnou metodikou (včetně parametrů modelu,
   rozpočtů, výchozí struktury repozitáře a pravidel lidských zásahů).
5. Zapsat finální důkazy a omezení do Planneru. Zatím neoznačovat za hotové.

## Zdroje

- [OpenHands 1.43.0 – Docker](https://github.com/OpenHands/OpenHands/blob/v1.43.0/README.md)
- [Registrace klientských nástrojů v Canvasu](https://github.com/OpenHands/OpenHands/blob/v1.43.0/src/api/agent-server-adapter.ts#L1167)
- Běžící lokální API: `http://localhost:8000/openapi.json` (ověřeno s agent-server 1.63.1).
- [LiteLLM Gemini](https://docs.litellm.ai/docs/providers/gemini)
- [Gemini limity a reset denní kvóty](https://aistudio.google.com/docs/rate-limits)
