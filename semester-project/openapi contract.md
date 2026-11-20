# Společný API kontrakt – MVP registračního systému akcí

Tento kontrakt je **povinnou součástí vstupu pro všechny tři varianty** (MAS A, MAS B, single agent C) spolu s dokumentem `user-stories.md`. Každá varianta si může zvolit vlastní technologie, databázi i UI. **Backend ale musí dodržet tento kontrakt přesně**: cesty, metody, názvy polí, stavové kódy a kódy chyb.

Proč kontrakt existuje:
- **Skryté akceptační testy** (M1, M3, M3b) a **zátěžový test** (M11–M14) se píšou proti tomuto kontraktu, takže poběží beze změny na všech třech verzích.
- **Férové srovnání:** všechny varianty dostanou stejně přesné zadání rozhraní.

Strojově čitelná verze je v souboru `openapi.yaml` (OpenAPI 3.1). Pokud se oba dokumenty liší, platí `openapi.yaml`.

---

## 1. Obecné konvence

| Oblast | Pravidlo |
|---|---|
| **Základní cesta** | Všechny endpointy začínají `/api/v1`. |
| **Formát** | JSON (`Content-Type: application/json; charset=utf-8`). Výjimkou je export (CSV). |
| **Názvy polí** | `camelCase`, anglicky. |
| **Identifikátory** | UUID v textové podobě (`"3f2c..."`). |
| **Datum** | `YYYY-MM-DD`, např. datum narození nebo datum akce. |
| **Datum a čas** | ISO 8601 s časovou zónou, např. `2027-06-01T09:00:00+02:00`. Server ukládá a porovnává v UTC. |
| **Věk** | Celé dokončené roky **k datu začátku akce** (`event.startDate`). Nezletilý = věk < 18. |
| **Prázdné hodnoty** | Nevyplněné nepovinné pole = `null`. Pole, ke kterému volající nemá oprávnění, **v odpovědi úplně chybí** (viz kap. 4). |
| **Jazyk** | Kódy chyb jsou anglicky (strojově zpracovatelné), texty `detail` česky. |
| **Frontend** | Frontend a API běží na stejném originu (frontend volá `/api/v1/...`), nebo je API dostupné přes proxy na stejném originu. |

### 1.1 Autentizace

- Jediný způsob přihlášení je simulace skautISu (`POST /auth/skautis-mock/login`). Po přihlášení vrátí API **token**. Je na variantě, zda jde o neprůhledný token, nebo JWT.
- Klient token posílá v hlavičce `Authorization: Bearer <token>`.
- Token platí minimálně 24 hodin. Po odhlášení (`POST /auth/logout`) je neplatný.
- Chybějící, neplatný nebo expirovaný token → `401 UNAUTHENTICATED`.

### 1.2 Stránkování

Seznamy, které můžou být dlouhé, se stránkují parametry `?page=1&pageSize=50`. `page` začíná od 1, `pageSize` je maximálně 200, výchozí 50.

```json
{
  "items": [ ... ],
  "page": 1,
  "pageSize": 50,
  "total": 1834
}
```

### 1.3 Chyby

Všechny chyby se vracejí ve formátu podle RFC 9457 (`Content-Type: application/problem+json`):

```json
{
  "type": "about:blank",
  "status": 409,
  "code": "PROGRAM_FULL",
  "title": "Program je obsazen",
  "detail": "Program „Lanové centrum“ už nemá volné místo.",
  "errors": []
}
```

U chyb validace (`422`) obsahuje `errors` seznam problémů u jednotlivých polí:

```json
{
  "status": 422,
  "code": "VALIDATION_ERROR",
  "title": "Neplatné údaje",
  "errors": [
    { "field": "data.contact.email", "code": "INVALID_FORMAT", "message": "Neplatný formát e-mailu." },
    { "field": "data.basic.birthDate", "code": "IN_FUTURE", "message": "Datum narození nesmí být v budoucnosti." }
  ]
}
```

**Testy kontrolují `status` a `code`. Text `title` a `detail` je volný.**

### 1.4 Stavové kódy

| Kód | Kdy |
|---|---|
| `200 OK` | Úspěšné čtení nebo úprava. |
| `201 Created` | Úspěšné vytvoření. Odpověď obsahuje vytvořený objekt. |
| `204 No Content` | Úspěšné smazání nebo odhlášení. Odpověď nemá tělo. |
| `401 Unauthorized` | Volající není přihlášen. |
| `403 Forbidden` | Volající je přihlášen, ale nemá oprávnění. |
| `404 Not Found` | Objekt neexistuje, **nebo** k němu volající nemá vůbec přístup. Nesmí se tím prozradit, že objekt existuje v jiné akci. |
| `409 Conflict` | Porušení obchodního pravidla (plná kapacita, duplicita, kolize…). |
| `422 Unprocessable Content` | Neplatný vstup (formát, povinné pole). |

Při náporu (souběžné přihlašování) **nesmí server vracet `5xx`** kvůli kolizím v databázi. Neúspěch kvůli kapacitě se vždy hlásí jako `409`.

---

## 2. Katalog kódů chyb

| `code` | HTTP | Význam | Příběh |
|---|---|---|---|
| `VALIDATION_ERROR` | 422 | Neplatný vstup, detail v `errors`. | F2.1, F7.1 |
| `UNAUTHENTICATED` | 401 | Chybí nebo je neplatný token. | F1.2 |
| `FORBIDDEN` | 403 | Role nemá oprávnění k operaci nebo datům. | F6.1 |
| `NOT_FOUND` | 404 | Objekt neexistuje nebo není dostupný. | – |
| `REGISTRATION_CLOSED` | 409 | Mimo registrační okno akce. | F2.3, F2.4 |
| `ALREADY_REGISTERED` | 409 | Uživatel už na akci má registraci. | F2.2 |
| `EVENT_FULL` | 409 | Kapacita akce je naplněna. | F2.5 |
| `ROLE_NOT_OPEN` | 409 | Pro zvolenou roli není registrace otevřená. | F2.1 |
| `LEADER_MUST_BE_ADULT` | 409 | Vedoucí skupiny musí být plnoletý. | F5.2 |
| `GROUP_CODE_INVALID` | 409 | Kód skupiny v této akci neexistuje. | F4.2 |
| `GROUP_FULL` | 409 | Skupina dosáhla maximálního počtu členů. | F4.2 |
| `ALREADY_IN_GROUP` | 409 | Účastník už je členem skupiny. | F4.2 |
| `ALREADY_HAS_GROUP` | 409 | Vedoucí už skupinu na této akci založil. | F4.1 |
| `LEADER_HAS_MEMBERS` | 409 | Změna by připravila skupinu s členy o plnoletého vedoucího. | F5.2, F6.2 |
| `REGISTRATION_NOT_COMPLETED` | 409 | Registrace není dokončená, např. nezletilý čeká na skupinu. | F5.1, F7.3 |
| `PROGRAM_SELECTION_CLOSED` | 409 | Mimo okno výběru programů. | F7.3 |
| `PROGRAM_FULL` | 409 | Program nemá volné místo. | F7.3, F7.4 |
| `PROGRAM_TIME_CONFLICT` | 409 | Časový překryv s jiným přihlášeným programem. | F7.3 |
| `PROGRAM_NOT_AVAILABLE_FOR_ROLE` | 409 | Program není dostupný pro roli volajícího. | F7.3 |
| `ALREADY_SIGNED_UP` | 409 | Na program už je přihlášen. | F7.3 |
| `CAPACITY_BELOW_SIGNUPS` | 409 | Kapacitu nelze snížit pod počet přihlášených. | F7.1 |
| `NO_COLUMNS_SELECTED` | 422 | Export bez vybraných sloupců. | F8.4 |

---

## 3. Datový model

### 3.1 User (uživatelský účet)

```json
{
  "id": "0b5d...",
  "skautisPersonId": "skautis-001",
  "email": "tomas.skautis@example.cz",
  "displayName": "Tomáš Dvořáček",
  "isAdmin": false
}
```

| Pole | Typ | Poznámka |
|---|---|---|
| `skautisPersonId` | string | Identifikátor osoby ve (simulovaném) skautISu. Každý účet má právě jeden, unikátní. |
| `isAdmin` | boolean | Administrátor systému (globální role). |

### 3.2 Event (akce)

```json
{
  "id": "11111111-1111-4111-8111-111111111111",
  "name": "Testovací akce 2027",
  "startDate": "2027-06-01",
  "endDate": "2027-06-05",
  "registrationOpensAt": "2026-11-01T00:00:00+01:00",
  "registrationClosesAt": "2027-05-01T23:59:59+02:00",
  "programSelectionOpensAt": "2027-01-10T18:00:00+01:00",
  "programSelectionClosesAt": "2027-05-15T23:59:59+02:00",
  "capacity": 400,
  "maxGroupSize": 12,
  "openRoles": ["participant", "group_leader", "lecturer"],
  "organizerUserIds": ["5a1e..."],
  "registeredCount": 128
}
```

| Pole | Typ | Poznámka |
|---|---|---|
| `capacity` | integer \| null | `null` = neomezeno. Počítají se všechny registrace bez ohledu na stav. |
| `maxGroupSize` | integer \| null | Maximální počet členů skupiny **včetně vedoucího**. `null` = neomezeno. |
| `openRoles` | pole rolí | Role, do kterých se lze sám registrovat (podmnožina `participant`, `group_leader`, `lecturer`). |
| `registeredCount` | integer | Počítá server. Jen pro čtení. |

### 3.3 Registration (registrace osoby na akci)

```json
{
  "id": "7c9e...",
  "eventId": "1111...",
  "userId": "0b5d...",
  "code": "K7MP3QXA",
  "roles": ["participant"],
  "status": "completed",
  "blockingReasons": [],
  "groupId": "d4f0...",
  "ageAtEventStart": 14,
  "isMinor": true,
  "visibleCategories": ["basic", "contact", "health", "diet"],
  "data": {
    "basic": {
      "firstName": "Jana",
      "lastName": "Nováková",
      "birthDate": "2012-09-14"
    },
    "contact": {
      "email": "jana.novakova@example.cz",
      "phone": "+420 777 123 456"
    },
    "health": {
      "conditions": "astma",
      "allergies": "pyl",
      "medications": "Ventolin dle potřeby"
    },
    "diet": {
      "restrictions": ["vegetarian"],
      "note": null
    }
  },
  "createdAt": "2026-11-20T10:15:00+01:00",
  "updatedAt": "2026-11-20T10:15:00+01:00"
}
```

| Pole | Typ | Poznámka |
|---|---|---|
| `code` | string | Identifikační kód osoby (F3). Formát v kap. 3.7. Nikdy se nemění. |
| `roles` | pole rolí | Právě **jedna základní role** (`participant`, `group_leader` nebo `lecturer`) + volitelně **týmové role** (`medic`, `organizer`). |
| `status` | `completed` \| `awaiting_group` | `awaiting_group` = nezletilý bez skupiny s plnoletým vedoucím (F5). |
| `blockingReasons` | pole kódů | Proč registrace není dokončená, např. `["MINOR_REQUIRES_GROUP"]`. U `completed` prázdné. |
| `groupId` | UUID \| null | Skupina, do které osoba patří. U vedoucího jeho vlastní skupina. |
| `ageAtEventStart`, `isMinor` | počítá server | Jen pro čtení. |
| `visibleCategories` | pole kategorií | Které kategorie `data` volající v této odpovědi vidí. |
| `data` | objekt | Obsahuje **jen** kategorie z `visibleCategories`. Ostatní klíče chybí. |

#### Validace `data`

| Pole | Povinné | Pravidlo |
|---|---|---|
| `basic.firstName`, `basic.lastName` | ano | 1–100 znaků, po oříznutí mezer neprázdné. |
| `basic.birthDate` | ano | Platné datum, ne v budoucnosti, ne před 1900-01-01. |
| `contact.email` | ano | Platný formát e-mailu. |
| `contact.phone` | ano | Regulární výraz `^\+?[0-9 ]{9,20}$`. |
| `health.conditions`, `health.allergies`, `health.medications` | ne | Max. 1 000 znaků. |
| `diet.restrictions` | ne | Pole z hodnot `vegetarian`, `vegan`, `gluten_free`, `lactose_free`, `other`. Výchozí `[]`. |
| `diet.note` | ne | Max. 500 znaků. |

### 3.4 Group (skupina)

```json
{
  "id": "d4f0...",
  "eventId": "1111...",
  "name": "Oddíl Lišky",
  "joinCode": "LX4K9P",
  "leaderRegistrationId": "a2b3...",
  "memberCount": 9,
  "members": [
    {
      "registrationId": "7c9e...",
      "code": "K7MP3QXA",
      "firstName": "Jana",
      "lastName": "Nováková",
      "ageAtEventStart": 14,
      "isMinor": true,
      "isLeader": false
    }
  ]
}
```

- `memberCount` **zahrnuje vedoucího**.
- `joinCode` vidí jen vedoucí skupiny, pořadatel a administrátor. Ostatním chybí.
- `members` se vrací jen v detailu skupiny, ne v seznamu.

### 3.5 Program

```json
{
  "id": "e8a1...",
  "eventId": "1111...",
  "name": "Lanové centrum",
  "description": "Výstup na lanové překážky s instruktorem.",
  "startsAt": "2027-06-02T09:00:00+02:00",
  "endsAt": "2027-06-02T11:00:00+02:00",
  "location": "Louka u jídelny",
  "capacity": 20,
  "signedUpCount": 17,
  "freeSpots": 3,
  "lecturerRegistrationId": "c3d4...",
  "lecturerName": "Petr Svoboda",
  "availableForRoles": ["participant", "group_leader"]
}
```

| Pole | Poznámka |
|---|---|
| `availableForRoles` | Prázdné pole = dostupný pro všechny základní role. |
| `signedUpCount`, `freeSpots` | Počítá server. `freeSpots = capacity − signedUpCount`, nikdy záporné. |
| `lecturerName` | Jediný osobní údaj na veřejném výpisu (jméno lektora). |

### 3.6 AuditLogEntry (záznam historie)

```json
{
  "id": "f1e2...",
  "eventId": "1111...",
  "at": "2026-11-20T10:20:31+01:00",
  "actorUserId": "0b5d...",
  "action": "registration.updated",
  "targetType": "registration",
  "targetId": "7c9e...",
  "targetRegistrationId": "7c9e...",
  "details": {
    "changedFields": ["contact.phone", "health.allergies"]
  }
}
```

Hodnoty `action` a jejich `details`:

| `action` | Kdy | `details` |
|---|---|---|
| `registration.created` | Vytvoření registrace. | `{ "roles": [...], "status": "..." }` |
| `registration.updated` | Změna údajů. | `{ "changedFields": ["kategorie.pole", ...] }` |
| `registration.roles_changed` | Změna rolí. | `{ "before": [...], "after": [...] }` |
| `group.created` | Založení skupiny. | `{ "groupId": "...", "name": "..." }` |
| `group.member_joined` | Připojení do skupiny. | `{ "groupId": "..." }` |
| `group.member_removed` | Odebrání ze skupiny. | `{ "groupId": "...", "newStatus": "..." }` |
| `program.signed_up` | Přihlášení na program. | `{ "programId": "..." }` |
| `program.signed_out` | Odhlášení z programu. | `{ "programId": "..." }` |
| `export.created` | Export dat. | `{ "columns": [...], "filters": {...}, "rowCount": 42 }` |

**Do `details` se nikdy neukládají hodnoty polí**, jen jejich názvy. U zdravotních údajů je to povinné, u ostatních pro jednotnost také.

### 3.7 Formát kódů

| Kód | Formát | Unikátní v rámci |
|---|---|---|
| `registration.code` | 8 znaků z abecedy `ABCDEFGHJKMNPQRSTUVWXYZ23456789`, regex `^[A-HJKMNP-Z2-9]{8}$` | celého systému |
| `group.joinCode` | 6 znaků ze stejné abecedy, regex `^[A-HJKMNP-Z2-9]{6}$` | akce |

- Kódy se generují **kryptograficky bezpečným náhodným generátorem**, ne z ID ani z pořadí.
- Při kolizi se generuje znovu.
- Vstup kódu od uživatele se porovnává **bez ohledu na velikost písmen** a s oříznutím mezer.

---

## 4. Oprávnění

### 4.1 Kategorie údajů podle role

| Role volajícího | Koho vidí | `basic` | `contact` | `health` | `diet` |
|---|---|:-:|:-:|:-:|:-:|
| `participant` | jen sebe | ✔ | ✔ | ✔ | ✔ |
| `group_leader` | sebe + členy své skupiny | ✔ | ✔ | ✔ | ✔ |
| `lecturer` | sebe + účastníky svého programu | ✔ (jen jméno, příjmení, kód) | ✘ | ✘ | ✘ |
| `medic` | všechny registrované na akci | ✔ | ✔ | ✔ | ✘ |
| `organizer` | všechny registrované na své akci | ✔ | ✔ | ✔ | ✔ |
| admin (`isAdmin`) | všechny ve všech akcích | ✔ | ✔ | ✔ | ✔ |

Pravidla:
1. Má-li osoba více rolí, platí **sjednocení** jejich oprávnění.
2. Kategorie, ke které volající nemá přístup, **v odpovědi chybí** (klíč není přítomen) a není uvedena ve `visibleCategories`.
3. **Explicitní žádost o nepovolenou kategorii** (`?categories=health` u role bez přístupu) → `403 FORBIDDEN`. Díky tomu lze oprávnění testovat jednoznačně (M3).
4. Registrace, kterou volající vůbec nesmí vidět (např. účastník cizí registraci) → `404 NOT_FOUND`.
5. Oprávnění se kontrolují **na serveru u každého požadavku**.

### 4.2 Kdo smí volat jaký endpoint

Legenda: **V** = veřejné bez přihlášení, **P** = přihlášený uživatel, **Ú** = registrovaný na akci (jakákoli role), **VS** = vedoucí dané skupiny, **L** = lektor daného programu, **Z** = zdravotník akce, **O** = pořadatel akce, **A** = administrátor.

| Endpoint | Smí |
|---|---|
| `GET /auth/skautis-mock/persons`, `POST /auth/skautis-mock/login` | V |
| `POST /auth/logout`, `GET /auth/me` | P |
| `GET /events`, `GET /events/{eventId}` | V |
| `POST /events` | A |
| `PATCH /events/{eventId}` | O, A (měnit `organizerUserIds` smí jen A) |
| `POST /events/{eventId}/registrations` | P |
| `GET`/`PATCH /events/{eventId}/registrations/me` | Ú |
| `GET /events/{eventId}/registrations` | Z, O, A |
| `GET /events/{eventId}/registrations/{registrationId}` | dotyčný sám, VS (člen jeho skupiny), L (účastník jeho programu), Z, O, A |
| `PUT /events/{eventId}/registrations/{registrationId}/roles` | O, A |
| `POST /events/{eventId}/groups` | Ú s rolí `group_leader` |
| `GET /events/{eventId}/groups` | Ú (vidí jen svou skupinu), O, A (vidí všechny) |
| `GET /events/{eventId}/groups/{groupId}` | VS, O, A |
| `POST /events/{eventId}/groups/join` | Ú |
| `DELETE /events/{eventId}/groups/{groupId}/members/{registrationId}` | VS, O, A |
| `GET /events/{eventId}/programs`, `GET .../programs/{programId}` | V |
| `POST`/`PATCH`/`DELETE .../programs[/{programId}]` | O, A |
| `POST .../programs/{programId}/signups`, `DELETE .../programs/{programId}/signups/me` | Ú |
| `GET .../programs/{programId}/signups` | L, O, A |
| `GET /events/{eventId}/registrations/me/schedule` | Ú |
| `GET /events/{eventId}/exports/columns`, `POST /events/{eventId}/exports` | Z, O, A |
| `GET /events/{eventId}/audit-log` | O, A |

---

## 5. Endpointy

U každého endpointu je uveden request, úspěšná odpověď a nejdůležitější chyby. Obecné chyby `401`, `403` a `404` se u jednotlivých endpointů neopakují.

### 5.1 Autentizace (F1)

Přihlášení je možné **pouze přes skautIS** (v MVP simulace). Endpointy pro registraci a přihlášení e-mailem a heslem **neexistují**.

#### `POST /api/v1/auth/logout` – odhlášení · US-F1.2

Odpověď `204`. Token je od té chvíle neplatný a další požadavky s ním vrací `401`.

#### `GET /api/v1/auth/me` – aktuální uživatel

Odpověď `200`:
```json
{
  "user": { "id": "0b5d...", "skautisPersonId": "skautis-001", "email": "...", "displayName": "...", "isAdmin": false },
  "registrations": [
    { "eventId": "1111...", "eventName": "Testovací akce 2027", "registrationId": "7c9e...", "roles": ["participant"], "status": "completed" }
  ]
}
```

#### `GET /api/v1/auth/skautis-mock/persons` – osoby simulace skautISu · US-F1.1

Odpověď `200`:
```json
{
  "items": [
    { "personId": "skautis-001", "firstName": "Tomáš", "lastName": "Dvořáček", "birthDate": "1998-03-12", "email": "tomas.skautis@example.cz", "unit": "Středisko Testov" },
    { "personId": "skautis-002", "firstName": "Eliška", "lastName": "Malá", "birthDate": "2013-07-01", "email": "eliska.skautis@example.cz", "unit": "Středisko Testov" },
    { "personId": "skautis-003", "firstName": "Marek", "lastName": "Veselý", "birthDate": "1990-11-30", "email": "marek.skautis@example.cz", "unit": "Středisko Testov" }
  ]
}
```

Seznam obsahuje tyto tři osoby (se stejným `personId` a údaji) a **všechny osoby ze standardních testovacích dat** (kap. 6.2). Musí být stejný ve všech variantách. Řadí se podle příjmení.

#### `POST /api/v1/auth/skautis-mock/login` – přihlášení simulací · US-F1.1

Request:
```json
{ "personId": "skautis-002" }
```

Odpověď `200`:
```json
{
  "token": "eyJhbGciOi...",
  "user": { "id": "9a8b...", "skautisPersonId": "skautis-002", "email": "eliska.skautis@example.cz", "displayName": "Eliška Malá", "isAdmin": false },
  "prefill": {
    "basic": { "firstName": "Eliška", "lastName": "Malá", "birthDate": "2013-07-01" },
    "contact": { "email": "eliska.skautis@example.cz", "phone": null }
  }
}
```

Pravidla:
- První přihlášení účet založí, další přihlášení stejnou osobou použije stejný účet.
- Neznámé `personId` → `404 NOT_FOUND`.
- Simulace **nevolá žádnou externí službu**.

---

### 5.2 Akce (F8.1, F2.3, F2.5, F4.4)

#### `GET /api/v1/events` – seznam akcí

Odpověď `200`: stránkovaný seznam objektů `Event`. Veřejné, bez `organizerUserIds`.

#### `GET /api/v1/events/{eventId}` – detail akce

Odpověď `200`: objekt `Event`. `organizerUserIds` vidí jen O a A.

#### `POST /api/v1/events` – založení akce · US-F8.1

Request:
```json
{
  "name": "Testovací akce 2027",
  "startDate": "2027-06-01",
  "endDate": "2027-06-05",
  "registrationOpensAt": "2026-11-01T00:00:00+01:00",
  "registrationClosesAt": "2027-05-01T23:59:59+02:00",
  "programSelectionOpensAt": "2027-01-10T18:00:00+01:00",
  "programSelectionClosesAt": "2027-05-15T23:59:59+02:00",
  "capacity": 400,
  "maxGroupSize": 12,
  "openRoles": ["participant", "group_leader", "lecturer"],
  "organizerUserIds": ["5a1e..."]
}
```

Odpověď `201`: vytvořený `Event`.

Chyby: `422 VALIDATION_ERROR`, pokud:
- `endDate` je před `startDate`,
- konec okna je před jeho začátkem,
- `capacity` nebo `maxGroupSize` je menší než 1,
- `organizerUserIds` je prázdné nebo neexistuje.

#### `PATCH /api/v1/events/{eventId}` – úprava akce · US-F2.3, F2.5, F4.4

Request: libovolná podmnožina polí z `POST /events`. Například:
```json
{ "registrationClosesAt": "2026-11-19T23:59:59+01:00", "capacity": 150 }
```

Odpověď `200`: upravený `Event`.

Chyby:
- `422 VALIDATION_ERROR`,
- `403 FORBIDDEN`, pokud pořadatel mění `organizerUserIds`.

Snížení `capacity` pod `registeredCount` je povoleno, jen se tím zastaví další registrace.

---

### 5.3 Registrace (F2, F3, F5)

#### `POST /api/v1/events/{eventId}/registrations` – registrace na akci · US-F2.1, F2.2, F3.1, F5.1, F5.2

Request:
```json
{
  "role": "participant",
  "groupCode": "LX4K9P",
  "data": {
    "basic": { "firstName": "Jana", "lastName": "Nováková", "birthDate": "2012-09-14" },
    "contact": { "email": "jana.novakova@example.cz", "phone": "+420 777 123 456" },
    "health": { "conditions": "astma", "allergies": "pyl", "medications": null },
    "diet": { "restrictions": ["vegetarian"], "note": null }
  }
}
```

- `role`: povinné, jedna z `participant`, `group_leader`, `lecturer`.
- `groupCode`: nepovinné. Pokud je vyplněné, registrace se rovnou připojí do skupiny.
- `health` a `diet`: nepovinné. Chybějící = prázdné hodnoty.

Odpověď `201`: objekt `Registration`.

Výsledek podle situace:

| Situace | `status` | `blockingReasons` |
|---|---|---|
| Plnoletý, bez skupiny | `completed` | `[]` |
| Plnoletý nebo nezletilý s platným `groupCode`, vedoucí plnoletý | `completed` | `[]` |
| Nezletilý bez `groupCode` | `awaiting_group` | `["MINOR_REQUIRES_GROUP"]` |

Chyby (při chybě **se registrace nevytvoří**):

| Kód | Kdy |
|---|---|
| `422 VALIDATION_ERROR` | Viz validace v kap. 3.3. |
| `409 REGISTRATION_CLOSED` | Aktuální čas je mimo `registrationOpensAt` až `registrationClosesAt`. |
| `409 ROLE_NOT_OPEN` | `role` není v `openRoles`. |
| `409 ALREADY_REGISTERED` | Uživatel už na akci registraci má. Tělo chyby obsahuje `"existingRegistrationId"`. |
| `409 EVENT_FULL` | `registeredCount >= capacity`. |
| `409 LEADER_MUST_BE_ADULT` | `role = group_leader` a věk < 18. |
| `409 GROUP_CODE_INVALID` | `groupCode` v akci neexistuje. |
| `409 GROUP_FULL` | Skupina dosáhla `maxGroupSize`. |

Pravidla pro souběh:
- Unikátnost dvojice (uživatel, akce) a kapacitu akce musí hlídat **databáze nebo transakce**, ne kontrola před zápisem v aplikaci.
- Ani při souběžném odeslání nesmí vzniknout duplicita ani překročení kapacity.

Pořadí kontrol (důležité pro testy, když platí víc chyb najednou):
1. `VALIDATION_ERROR`
2. `REGISTRATION_CLOSED`
3. `ROLE_NOT_OPEN`
4. `ALREADY_REGISTERED`
5. `LEADER_MUST_BE_ADULT`
6. `GROUP_CODE_INVALID`
7. `GROUP_FULL`
8. `EVENT_FULL`

#### `GET /api/v1/events/{eventId}/registrations/me` – vlastní registrace · US-F3.2

Odpověď `200`: vlastní `Registration` se všemi kategoriemi.

Chyby: `404 NOT_FOUND`, pokud uživatel na akci registrován není.

#### `PATCH /api/v1/events/{eventId}/registrations/me` – úprava vlastních údajů · US-F2.4

Request: částečný objekt `data`. Posílají se jen měněná pole.
```json
{ "data": { "contact": { "phone": "+420 602 000 111" }, "health": { "allergies": "pyl, ořechy" } } }
```

Odpověď `200`: upravená `Registration`.

Chyby:
- `422 VALIDATION_ERROR`,
- `409 REGISTRATION_CLOSED` po konci registračního okna,
- `409 LEADER_MUST_BE_ADULT`, pokud by změna `birthDate` udělala z osoby s rolí `group_leader` nezletilého. Změna se odmítne celá.

Pravidla:
- Pokud změna `birthDate` udělá ze člena bez skupiny nezletilého, `status` se změní na `awaiting_group`. A naopak.
- Každá úprava vytvoří záznam `registration.updated` se seznamem změněných polí.

#### `GET /api/v1/events/{eventId}/registrations` – přehled registrací · US-F8.2

Query parametry:

| Parametr | Příklad | Význam |
|---|---|---|
| `role` | `participant` | Filtr podle role (opakovatelný: `?role=participant&role=lecturer`). |
| `groupId` | UUID nebo `none` | Filtr podle skupiny. `none` = bez skupiny. |
| `status` | `awaiting_group` | Filtr podle stavu. |
| `minorWithoutGroup` | `true` | Jen nezletilí bez skupiny. |
| `q` | `nováková` / `K7MP3QXA` | Fulltext v jméně, příjmení, e-mailu a kódu. Bez ohledu na velikost písmen a diakritiku. |
| `sort` | `lastName` / `-createdAt` | Řazení, `-` = sestupně. Výchozí `lastName`. |
| `page`, `pageSize` | `1`, `50` | Stránkování. |

Odpověď `200`:
```json
{
  "items": [
    {
      "id": "7c9e...",
      "code": "K7MP3QXA",
      "roles": ["participant"],
      "status": "completed",
      "groupId": "d4f0...",
      "groupName": "Oddíl Lišky",
      "ageAtEventStart": 14,
      "isMinor": true,
      "visibleCategories": ["basic", "contact", "health"],
      "data": {
        "basic": { "firstName": "Jana", "lastName": "Nováková", "birthDate": "2012-09-14" },
        "contact": { "email": "jana.novakova@example.cz", "phone": "+420 777 123 456" },
        "health": { "conditions": "astma", "allergies": "pyl", "medications": null }
      }
    }
  ],
  "page": 1, "pageSize": 50, "total": 1
}
```
(Příklad odpovědi pro zdravotníka: chybí kategorie `diet`.)

Výkon: p95 < 1 s při 2 000 registracích na akci (NFR-1).

#### `GET /api/v1/events/{eventId}/registrations/{registrationId}` – detail registrace · US-F8.3, F6.1

Query parametr `categories` (nepovinný, opakovatelný): `?categories=basic&categories=health`.

Odpověď `200`: `Registration` doplněná o pole `programs` (seznam `{ "programId", "name", "startsAt", "endsAt" }`).

Chování:
- Bez `categories` se vrátí všechny kategorie, ke kterým má volající přístup.
- S `categories` se vrátí jen požadované. Pokud je mezi nimi nepovolená → `403 FORBIDDEN`.

#### `PUT /api/v1/events/{eventId}/registrations/{registrationId}/roles` – změna rolí · US-F6.2

Request (kompletní nový seznam rolí):
```json
{ "roles": ["participant", "medic"] }
```

Odpověď `200`: upravená `Registration`.

Chyby:

| Kód | Kdy |
|---|---|
| `422 VALIDATION_ERROR` | Seznam neobsahuje právě jednu základní roli nebo obsahuje neznámou roli. |
| `409 LEADER_MUST_BE_ADULT` | Přidání `group_leader` nezletilému. |
| `409 LEADER_HAS_MEMBERS` | Odebrání `group_leader` vedoucímu, jehož skupina má členy. |

Každá změna vytvoří záznam `registration.roles_changed`.

---

### 5.4 Skupiny (F4, F5)

#### `POST /api/v1/events/{eventId}/groups` – založení skupiny · US-F4.1

Request:
```json
{ "name": "Oddíl Lišky" }
```

Odpověď `201`: `Group` s vygenerovaným `joinCode` a vedoucím jako jediným členem (`memberCount: 1`). Registrace vedoucího dostane `groupId` této skupiny.

Chyby:
- `422 VALIDATION_ERROR` (název 1–100 znaků),
- `403 FORBIDDEN`, pokud volající nemá roli `group_leader`,
- `409 ALREADY_HAS_GROUP`,
- `409 ALREADY_IN_GROUP`, pokud je vedoucí členem cizí skupiny.

#### `GET /api/v1/events/{eventId}/groups` – seznam skupin · US-F8.2

Odpověď `200`: stránkovaný seznam `Group` bez `members`. Doplněno o `leaderName`. Pořadatel vidí všechny skupiny, ostatní jen svou.

#### `GET /api/v1/events/{eventId}/groups/{groupId}` – detail skupiny · US-F4.3

Odpověď `200`: `Group` včetně `members`.
- Vedoucí a pořadatel dostanou u každého člena i objekt `data` se všemi kategoriemi (viz kap. 4.1).
- Člen skupiny detail ostatních členů nevidí (`403 FORBIDDEN`). O své skupině ví z `groupId` ve vlastní registraci a ze seznamu skupin (název a jméno vedoucího).

#### `POST /api/v1/events/{eventId}/groups/join` – připojení do skupiny kódem · US-F4.2, F5.1

Request:
```json
{ "code": "lx4k9p" }
```

Odpověď `200`: upravená vlastní `Registration`. U nezletilého se `status` změní z `awaiting_group` na `completed`.

Chyby:
- `404 NOT_FOUND`, pokud volající není na akci registrován,
- `409 GROUP_CODE_INVALID`,
- `409 GROUP_FULL`,
- `409 ALREADY_IN_GROUP`.

Kapacitu skupiny je nutné hlídat i při souběžném připojování.

#### `DELETE /api/v1/events/{eventId}/groups/{groupId}/members/{registrationId}` – odebrání člena · US-F4.3, F5.1

Odpověď `204`.

Důsledky:
- `groupId` člena se nastaví na `null`.
- Nezletilý člen přejde do stavu `awaiting_group` s `blockingReasons: ["MINOR_REQUIRES_GROUP"]`.
- Přihlášky na programy mu zůstávají, ale dokud není znovu ve skupině, nesmí se přihlašovat na další programy.
- Vytvoří se záznam `group.member_removed`.

Chyby:
- `409 LEADER_HAS_MEMBERS`, pokud jde o odebrání vedoucího vlastní skupiny,
- `404 NOT_FOUND`, pokud registrace není členem skupiny.

---

### 5.5 Programy (F7)

#### `GET /api/v1/events/{eventId}/programs` – seznam programů · US-F7.2

Veřejné. Query parametry: `from`, `to` (filtr podle času začátku).

Odpověď `200`:
```json
{ "items": [ { "id": "e8a1...", "name": "Lanové centrum", "...": "objekt Program" } ] }
```

Seznam se nestránkuje. Je řazený podle `startsAt` a **neobsahuje žádné osobní údaje přihlášených**.

#### `GET /api/v1/events/{eventId}/programs/{programId}` – detail programu

Odpověď `200`: objekt `Program`. Pokud je volající přihlášený, odpověď navíc obsahuje `"isSignedUp": true|false`.

#### `POST /api/v1/events/{eventId}/programs` – vytvoření programu · US-F7.1

Request:
```json
{
  "name": "Lanové centrum",
  "description": "Výstup na lanové překážky s instruktorem.",
  "startsAt": "2027-06-02T09:00:00+02:00",
  "endsAt": "2027-06-02T11:00:00+02:00",
  "location": "Louka u jídelny",
  "capacity": 20,
  "lecturerRegistrationId": "c3d4...",
  "availableForRoles": []
}
```

Odpověď `201`: objekt `Program`.

Chyby: `422 VALIDATION_ERROR`, pokud:
- chybí povinné pole (`name`, `startsAt`, `endsAt`, `location`, `capacity`),
- `endsAt <= startsAt`,
- `capacity < 1`,
- `lecturerRegistrationId` není registrace s rolí `lecturer` na této akci.

#### `PATCH /api/v1/events/{eventId}/programs/{programId}` – úprava programu · US-F7.1

Request: podmnožina polí z vytvoření.

Odpověď `200`.

Chyby:
- `422 VALIDATION_ERROR`,
- `409 CAPACITY_BELOW_SIGNUPS`, pokud by nová `capacity` byla menší než `signedUpCount`.

#### `DELETE /api/v1/events/{eventId}/programs/{programId}` – smazání programu

Odpověď `204`. Přihlášky se smažou a u každé se zaznamená `program.signed_out`.

#### `POST /api/v1/events/{eventId}/programs/{programId}/signups` – přihlášení na program · US-F7.3, F7.4

Request: bez těla. Volající se přihlašuje sám za sebe.

Odpověď `201`:
```json
{ "programId": "e8a1...", "registrationId": "7c9e...", "createdAt": "2027-01-10T18:00:01+01:00", "freeSpots": 2 }
```

Chyby (pořadí kontrol):
1. `404 NOT_FOUND`: volající nemá na akci registraci.
2. `409 REGISTRATION_NOT_COMPLETED`: `status = awaiting_group`.
3. `409 PROGRAM_SELECTION_CLOSED`: mimo `programSelectionOpensAt` až `programSelectionClosesAt`.
4. `409 PROGRAM_NOT_AVAILABLE_FOR_ROLE`.
5. `409 ALREADY_SIGNED_UP`.
6. `409 PROGRAM_TIME_CONFLICT`: tělo chyby obsahuje `"conflictingProgramId"`.
7. `409 PROGRAM_FULL`.

**Kritický požadavek (M11, M12):**
- Kapacita a unikátnost přihlášky (registrace, program) se musí hlídat atomicky na úrovni databáze, např. podmíněným `UPDATE ... WHERE signed_up_count < capacity`, zámkem řádku nebo unikátním indexem.
- Při 300 souběžných požadavcích na program s kapacitou 20 musí odpovědět přesně 20× `201` a 280× `409 PROGRAM_FULL`, nikdy `5xx`.

Časový překryv: programy A a B se překrývají, pokud `A.startsAt < B.endsAt && B.startsAt < A.endsAt`. Programy, které na sebe jen navazují (konec = začátek), se nepřekrývají.

#### `DELETE /api/v1/events/{eventId}/programs/{programId}/signups/me` – odhlášení z programu · US-F7.3

Odpověď `204`. Místo se uvolní.

Chyby:
- `409 PROGRAM_SELECTION_CLOSED`,
- `404 NOT_FOUND`, pokud volající na programu není.

#### `GET /api/v1/events/{eventId}/programs/{programId}/signups` – přihlášení na programu · US-F6.3

Odpověď `200`:
```json
{
  "items": [
    { "registrationId": "7c9e...", "code": "K7MP3QXA", "firstName": "Jana", "lastName": "Nováková", "signedUpAt": "2027-01-10T18:00:01+01:00" }
  ],
  "total": 1
}
```

Lektor dostane **jen tato pole**, a jen pro programy, kde je uveden jako lektor. U cizího programu → `403 FORBIDDEN`.

#### `GET /api/v1/events/{eventId}/registrations/me/schedule` – můj harmonogram · US-F7.5

Odpověď `200`:
```json
{
  "items": [
    { "programId": "e8a1...", "name": "Lanové centrum", "startsAt": "2027-06-02T09:00:00+02:00", "endsAt": "2027-06-02T11:00:00+02:00", "location": "Louka u jídelny" }
  ]
}
```

Seznam je řazený podle `startsAt` vzestupně.

---

### 5.6 Export (F8.4)

#### `GET /api/v1/events/{eventId}/exports/columns` – sloupce povolené pro export

Odpověď `200`: jen sloupce z kategorií, ke kterým má volající přístup.
```json
{
  "items": [
    { "key": "code", "category": "basic", "label": "Identifikační kód" },
    { "key": "firstName", "category": "basic", "label": "Jméno" },
    { "key": "allergies", "category": "health", "label": "Alergie" }
  ]
}
```

Úplný katalog sloupců:

| `key` | Kategorie |
|---|---|
| `code`, `firstName`, `lastName`, `birthDate`, `ageAtEventStart`, `roles`, `status`, `groupName` | `basic` |
| `email`, `phone` | `contact` |
| `healthConditions`, `allergies`, `medications` | `health` |
| `dietRestrictions`, `dietNote` | `diet` |

#### `POST /api/v1/events/{eventId}/exports` – export do CSV · US-F8.4

Request:
```json
{
  "columns": ["code", "firstName", "lastName", "allergies"],
  "filters": { "role": ["participant"], "groupId": null, "status": null, "minorWithoutGroup": false, "q": null }
}
```

`filters` mají stejný význam jako query parametry `GET /registrations`.

Odpověď `200`:
- Hlavičky:
  - `Content-Type: text/csv; charset=utf-8`
  - `Content-Disposition: attachment; filename="export-<eventId>-<YYYYMMDD-HHmmss>.csv"`
- Tělo:
  - UTF-8 **s BOM** (kvůli správnému zobrazení diakritiky v Excelu),
  - oddělovač `,`, uvozovky a escapování podle RFC 4180,
  - první řádek jsou hlavičky = `key` sloupců ve zvoleném pořadí,
  - pole `roles` a `dietRestrictions` jsou spojená znakem `|`.

```
code,firstName,lastName,allergies
K7MP3QXA,Jana,Nováková,pyl
```

Chyby:
- `422 NO_COLUMNS_SELECTED` (prázdné `columns`),
- `422 VALIDATION_ERROR` (neznámý sloupec),
- `403 FORBIDDEN` (sloupec z nepovolené kategorie; v tom případě se nic neexportuje).

Každý úspěšný export vytvoří záznam `export.created` se seznamem sloupců, filtry a počtem řádků.

---

### 5.7 Historie operací (F9)

#### `GET /api/v1/events/{eventId}/audit-log` – historie · US-F9.1, F9.2

Query parametry: `action` (opakovatelný), `actorUserId`, `targetRegistrationId`, `from`, `to`, `page`, `pageSize`.

Odpověď `200`: stránkovaný seznam `AuditLogEntry`, řazený od nejnovějšího.

Pravidla:
- Žádný endpoint pro úpravu ani smazání záznamů neexistuje.
- `PUT`, `PATCH` a `DELETE` na `/audit-log` vrací `405 Method Not Allowed`.
- Záznam se zapisuje **ve stejné transakci** jako samotná operace. Neúspěšná operace tedy nezanechá záznam.

---

## 6. Podpora testování

Tyto endpointy a pravidla existují **jen kvůli měřitelnosti**. Musí je mít všechny varianty.

### 6.1 Testovací endpointy

Testovací endpointy jsou dostupné **jen když běží aplikace s proměnnou prostředí `APP_ENV=test`**. Jinak vrací `404`.

| Endpoint | Účel |
|---|---|
| `GET /api/v1/health` | Vždy dostupný. Vrací `200 {"status": "ok"}`, jakmile je aplikace připravena (čeká na něj CI). |
| `POST /api/v1/test/reset` | Smaže všechna data a nahraje **standardní testovací data** (kap. 6.2). Vrací `200` s ID vytvořených objektů. |
| `POST /api/v1/test/login-as` | Request `{ "email": "..." }`. Vrátí token pro testový účet bez procházení simulace (zrychlení testů a zátěžového testu). |
| `POST /api/v1/test/bulk-users` | Request `{ "count": 300, "eventId": "...", "registered": true }`. Vytvoří N plnoletých testových účtů, volitelně rovnou registrovaných, a vrátí jejich tokeny. Slouží zátěžovému testu. |

Odpověď `POST /test/reset`:
```json
{
  "eventId": "11111111-1111-4111-8111-111111111111",
  "groupIds": { "lisky": "..." },
  "programIds": { "lanove": "...", "lukostrelba": "...", "navazujici": "...", "zatez": "...", "jenLektori": "..." },
  "userIds": { "admin": "...", "organizer": "...", "...": "..." }
}
```

### 6.2 Standardní testovací data (seed)

Data musí být po `POST /test/reset` **ve všech variantách stejná**. Seed se vytváří také skriptem pro lokální spuštění (NFR-8). Všechny osoby jsou smyšlené.

**Akce:**

| Pole | Hodnota |
|---|---|
| `id` | `11111111-1111-4111-8111-111111111111` |
| `name` | `Testovací akce` |
| `startDate`, `endDate` | dnešní datum + 60 dní, + 64 dní |
| Registrační okno | od (teď − 1 den) do (teď + 30 dní) |
| Okno výběru programů | od (teď − 1 den) do (teď + 30 dní) |
| `capacity` | `null` |
| `maxGroupSize` | `5` |
| `openRoles` | `participant`, `group_leader`, `lecturer` |

**Účty.** Každý účet odpovídá osobě simulace skautISu s `personId` = `seed-` + část e-mailu před `@` (např. `seed-poradatel`). Přihlašuje se výběrem osoby v simulaci nebo v testech přes `POST /test/login-as`. „Věk“ je věk k `startDate` akce: seed počítá `birthDate` tak, aby věk vyšel přesně, např. pro 14 let `birthDate = startDate − 14 let − 10 dní`.

| E-mail | Admin | Registrace na akci | Věk | Skupina |
|---|:-:|---|:-:|---|
| `admin@test.local` | ano | – | – | – |
| `poradatel@test.local` | – | `participant` + `organizer` | 30 | – |
| `zdravotnik@test.local` | – | `participant` + `medic` | 28 | – |
| `lektor@test.local` | – | `lecturer` | 35 | – |
| `vedouci@test.local` | – | `group_leader` | 25 | „Lišky“ (vedoucí) |
| `dite1@test.local` | – | `participant` | 14 | „Lišky“ |
| `dite2@test.local` | – | `participant` | 12 | „Lišky“ |
| `dospely@test.local` | – | `participant` | 22 | – |
| `nezletily-bez-skupiny@test.local` | – | `participant`, stav `awaiting_group` | 15 | – |
| `neregistrovany-dospely@test.local` | – | – | 20 (pro registraci) | – |
| `neregistrovany-nezletily@test.local` | – | – | 16 (pro registraci) | – |
| `vedouci2@test.local` | – | `group_leader`, bez skupiny | 40 | – |

- Skupina „Lišky“ má pevný `joinCode` `LSK234`. Pevný kód je přípustný **jen v seedu**.
- U registrovaných osob mají všechny kategorie vyplněné ukázkové hodnoty. Například `dite1` má `health.allergies = "pyl"` a `diet.restrictions = ["vegetarian"]`.

**Programy** (časy relativně k `startDate` akce, den 2 = `startDate` + 1 den):

| Klíč v seedu | Název | Čas | Kapacita | Dostupný pro | Lektor |
|---|---|---|:-:|---|---|
| `lanove` | Lanové centrum | den 2, 09:00–11:00 | 2 | všechny | `lektor@test.local` |
| `lukostrelba` | Lukostřelba | den 2, 10:00–12:00 (překryv s `lanove`) | 10 | všechny | – |
| `navazujici` | Orientační běh | den 2, 11:00–12:30 (navazuje na `lanove`) | 10 | všechny | – |
| `zatez` | Zátěžový program | den 3, 09:00–10:00 | 20 | všechny | – |
| `jenLektori` | Setkání lektorů | den 3, 14:00–15:00 | 10 | `lecturer` | – |

Na programu `lanove` je po resetu přihlášen `dite1@test.local`, takže zbývá 1 volné místo.

### 6.3 Ostatní pravidla pro testovatelnost

1. **Konfigurace přes proměnné prostředí:** `DATABASE_URL`, `APP_ENV`, `PORT` (výchozí `8080`).
2. **Spuštění jedním příkazem:** `docker compose up` spustí aplikaci včetně databáze na `http://localhost:8080`. Frontend je dostupný na `/`, API na `/api/v1`.
3. **Žádné omezování počtu požadavků (rate limiting) v režimu `APP_ENV=test`**, jinak by zkreslilo zátěžový test.
4. **E-maily** (volitelné US-X.2) jdou jen na testovací SMTP server (např. Mailpit), nikdy na reálné adresy.

### 6.4 Identifikátory pro E2E testy (UI)

Skryté E2E testy (Playwright) hledají prvky podle atributu `data-testid`. Klíčové obrazovky musí tyto atributy obsahovat. Zbytek UI je na variantě.

| `data-testid` | Prvek |
|---|---|
| `skautis-mock-login`, `skautis-person-<personId>` | Přihlášení: simulace skautISu a výběr osoby |
| `logout` | Odhlášení |
| `reg-role`, `reg-first-name`, `reg-last-name`, `reg-birth-date`, `reg-email`, `reg-phone`, `reg-allergies`, `reg-diet-<hodnota>`, `reg-group-code`, `reg-submit` | Registrační formulář |
| `reg-status`, `reg-code` | Stav registrace a identifikační kód v profilu |
| `field-error-<název pole>` | Chybová hláška u pole (např. `field-error-reg-email`) |
| `group-create-name`, `group-create-submit`, `group-join-code`, `group-join-submit`, `group-member-<code>`, `group-remove-<code>` | Skupiny |
| `program-<programId>`, `program-signup-<programId>`, `program-signout-<programId>`, `program-free-spots-<programId>` | Programy |
| `schedule-item-<programId>` | Můj harmonogram |
| `admin-table`, `admin-row-<code>`, `admin-filter-role`, `admin-filter-minor-without-group`, `admin-search` | Přehled registrací |
| `export-column-<key>`, `export-submit` | Export |
| `error-message` | Obecná chybová hláška z API (zobrazuje `code` nebo text) |

---

## 7. Mapování na user stories a metriky

| User story | Endpointy | Metrika |
|---|---|---|
| F1.1–F1.2 | `/auth/*` | M1 |
| F2.1–F2.5 | `POST/GET/PATCH /registrations[/me]`, `PATCH /events` | M1, M12 |
| F3.1–F3.2 | `Registration.code`, `GET /registrations?q=` | M1 |
| F4.1–F4.4 | `/groups/*`, `PATCH /events` (`maxGroupSize`) | M1 |
| F5.1–F5.2 | `POST /registrations`, `/groups/join`, `DELETE /groups/.../members`, `PUT /roles` | M1, M3b |
| F6.1–F6.3 | všechny endpointy s daty osob, `?categories=` | M1, M3 |
| F7.1–F7.5 | `/programs/*`, `/signups`, `/me/schedule` | M1, M11, M13, M14 |
| F8.1–F8.4 | `POST /events`, `GET /registrations`, `/exports` | M1, M13 |
| F9.1–F9.2 | `/audit-log` | M1 |

---

## 8. Otevřené otázky pro tým

1. **Zdravotní údaje pro vedoucího skupiny** jsou zatím povolené (předpoklad z user stories). Pokud to organizace nepotvrdí, změní se jen řádek `group_leader` v kap. 4.1.
2. **Zátěžový test:** zda testovat i nápor registrací (`POST /registrations`), nebo jen výběr programů. Kontrakt podporuje obojí přes `/test/bulk-users`.
3. **Verze kontraktu:** po zahájení běhů se kontrakt nesmí měnit. Pokud změna bude nutná, musí jít do všech tří variant současně a zapsat se do deníku jako odchylka (proposal kap. 6.1).
