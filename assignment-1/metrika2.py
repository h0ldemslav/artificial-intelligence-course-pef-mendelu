#!/usr/bin/env python3
"""Offline vyhodnocení formální přesnosti DOI/ISBN. Python 3.10+, bez závislostí."""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

DOI_FORMAT = re.compile(r"10\.[0-9]{4,9}/[-._;()/:A-Z0-9]+", re.I)
DOI_LABEL = re.compile(r"\bdoi\s*:\s*|https?://(?:dx\.)?doi\.org/", re.I)
ISBN_LABEL = re.compile(r"\bISBN(?:[- ]?(?:10|13))?\s*:?\s*", re.I)
TOKEN = re.compile(r"[^\s<>\[\]{}\"'`]+")
BARE_DOI = re.compile(r"(?<![\w/])10\.[^\s<>\[\]{}\"'`]+", re.I)
BARE_ISBN = re.compile(r"(?<![\w-])(?:97[89][0-9]{10}|[0-9]{9}[0-9Xx])(?![\w-])")
GROUPED_ISBN = re.compile(r"(?<![\w-])(?:[0-9]+-){2,}[0-9Xx]+(?![\w-])")
HEAD = re.compile(r"^\s*(?:#{1,6}\s*)?(?:\d+[.)]\s*)?(?:\*\*)?(Seznam literatury|Literatura|References|Bibliography|Nepoužité zdroje|Nejistoty)(?:\*\*)?\s*[:–-]?\s*$", re.I | re.M)


def clean_doi(value):
    value = DOI_LABEL.sub('', value.strip(), count=1).rstrip('*').rstrip('.,;:!?')
    while value.endswith(')') and value.count(')') > value.count('('):
        value = value[:-1]
    return value.lower()


def clean_isbn(value):
    return re.sub(r'[\s-]', '', value).upper()


def valid_isbn(value):
    if re.fullmatch(r'[0-9]{9}[0-9X]', value):
        return sum((10-i)*(10 if c == 'X' else int(c)) for i, c in enumerate(value)) % 11 == 0
    if re.fullmatch(r'97[89][0-9]{10}', value):
        return sum(int(c)*(1 if i % 2 == 0 else 3) for i, c in enumerate(value)) % 10 == 0
    return False


def select_text(text, scope):
    text = text.replace('\r\r\n', '\n').replace('\r\n', '\n').replace('\r', '\n')
    if scope == 'all':
        return text, 'cely_text'
    # Odstranění značek tučného písma pouze pro rozpoznání nadpisů;
    # délka i pozice původního textu zůstává zachována.
    heading_text = text.replace('**', '  ')
    heads = list(HEAD.finditer(heading_text))
    for i, h in enumerate(heads):
        if h.group(1).lower() in ('seznam literatury', 'literatura', 'references', 'bibliography'):
            end = heads[i+1].start() if i+1 < len(heads) else len(text)
            return text[h.end():end], 'seznam_literatury'
    if scope == 'bibliography':
        raise ValueError('Nenalezen samostatný nadpis seznamu literatury.')
    return text, 'cely_text_nadpis_nenalezen'


def extract(text):
    """Vrací i chybné označené kandidáty; neopravuje chybné číslice."""
    found = []
    occupied = []

    def add(kind, raw, start, end):
        norm = clean_doi(raw) if kind == 'DOI' else clean_isbn(raw)
        ok = bool(DOI_FORMAT.fullmatch(norm)) if kind == 'DOI' else valid_isbn(norm)
        found.append(dict(typ=kind, puvodni=raw, normalizovany=norm, platny=int(ok),
                          radek=text.count('\n', 0, start)+1))
        occupied.append((start, end))

    for m in DOI_LABEL.finditer(text):
        start = m.end()
        while start < len(text) and text[start] in '[`*':
            start += 1
        token = TOKEN.match(text, start)
        add('DOI', token.group() if token else '', m.start(), token.end() if token else m.end())
    for m in ISBN_LABEL.finditer(text):
        # Jen číslice, X a oddělovače; délku posuzuje validátor, nikoli extraktor.
        number = re.match(r'[0-9Xx]+(?:[ \t-]+[0-9Xx]+)*', text[m.end():])
        raw = number.group() if number else ''
        end = m.end()+len(raw)
        # Alfanumerický překlep nesmí být přijat jako platný číselný prefix.
        if end < len(text) and text[end].isalnum():
            token = TOKEN.match(text, m.end())
            raw = token.group() if token else raw
            end = token.end() if token else end
        if not raw:
            token = TOKEN.match(text, m.end())
            raw = token.group() if token else ''
            end = token.end() if token else end
        add('ISBN', raw, m.start(), end)
    for kind, pattern in [('DOI', BARE_DOI), ('ISBN', BARE_ISBN), ('ISBN', GROUPED_ISBN)]:
        for m in pattern.finditer(text):
            if any(m.start() < b and m.end() > a for a, b in occupied):
                continue
            if kind == 'ISBN' and not 9 <= len(clean_isbn(m.group())) <= 14:
                continue
            add(kind, m.group(), m.start(), m.end())
    # Každý unikátní identifikátor má stejnou váhu; opakování skóre nezvyšuje.
    unique = {}
    for item in found:
        unique.setdefault((item['typ'], item['normalizovany']), item)
    return list(unique.values())


def evaluate(text, scope='all', reference=None):
    selected, used_scope = select_text(text, scope)
    items = extract(selected)
    n, valid = len(items), sum(x['platny'] for x in items)
    result = dict(rozsah=used_scope, pocet_identifikatoru=n, pocet_platnych=valid,
                  pocet_neplatnych=n-valid, metrika2_formalni=valid/n if n else 0.0,
                  stav='OK' if n else 'BEZ_IDENTIFIKATORU',
                  metrika2_referencni='', reference_shody='', reference_chybi='', reference_navic='')
    if reference is not None:
        expected = set()
        for kind, key, normalizer in [('DOI', 'doi', clean_doi), ('ISBN', 'isbn', clean_isbn)]:
            values = reference.get(key, [])
            if not isinstance(values, list) or not all(isinstance(x, str) for x in values):
                raise ValueError(f'Reference {key} musí být seznam řetězců.')
            for raw in values:
                norm = normalizer(raw)
                if not (DOI_FORMAT.fullmatch(norm) if kind == 'DOI' else valid_isbn(norm)):
                    raise ValueError(f'Neplatná reference: {raw}')
                expected.add((kind, norm))
        actual = {(x['typ'], x['normalizovany']) for x in items}
        matched = actual & expected
        union = actual | expected
        result.update(metrika2_referencni=len(matched)/len(union) if union else '',
                      reference_shody=len(matched), reference_chybi=len(expected-actual),
                      reference_navic=len(actual-expected))
    return result, items


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        sample = f.read(4096)
        f.seek(0)
        delimiter = ';' if sample.splitlines()[0].count(';') > sample.splitlines()[0].count(',') else ','
        reader = csv.DictReader(f, delimiter=delimiter)
        return list(reader), reader.fieldnames or []


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path, required=True, help='Složka s UTF-8 soubory .txt (rekurzivně).')
    p.add_argument('--output', type=Path, default=Path('vysledky_metrika2.csv'))
    p.add_argument('--details', type=Path, default=Path('identifikatory_metrika2.csv'))
    p.add_argument('--expected-count', type=int, default=120, help='Očekávaný počet; 0 kontrolu vypne.')
    p.add_argument('--scope', choices=['all', 'auto', 'bibliography'], default='all')
    p.add_argument('--references', type=Path, help='JSON: run_id -> {doi: [...], isbn: [...]}')
    p.add_argument('--central', type=Path, help='Existující CSV s klíčem run_id; výstup bude jeho doplněná kopie.')
    args = p.parse_args()
    try:
        if not args.input.is_dir():
            raise ValueError('Vstupní složka neexistuje.')
        files = sorted(args.input.rglob('*.txt'))
        if not files or (args.expected_count and len(files) != args.expected_count):
            raise ValueError(f'Nalezeno {len(files)} výstupů, očekáváno {args.expected_count}. Pro jiný počet použijte --expected-count N.')
        paths = [args.output.resolve(), args.details.resolve()]
        inputs = {f.resolve() for f in files} | {x.resolve() for x in (args.central, args.references) if x}
        if paths[0] == paths[1] or any(x in inputs for x in paths):
            raise ValueError('Výstupy musí mít odlišné cesty a nesmějí přepsat vstupní soubory.')
        refs = json.loads(args.references.read_text(encoding='utf-8-sig')) if args.references else {}
        if not isinstance(refs, dict):
            raise ValueError('Reference JSON musí být objekt.')
        results, details = [], []
        for file in files:
            run_id = file.relative_to(args.input).with_suffix('').as_posix()
            if args.references and run_id not in refs:
                raise ValueError(f'Chybí reference pro {run_id}.')
            if args.references and not isinstance(refs[run_id], dict):
                raise ValueError(f'Reference pro {run_id} musí být objekt.')
            row, items = evaluate(file.read_text(encoding='utf-8-sig'), args.scope, refs.get(run_id))
            results.append(dict(run_id=run_id, soubor=file.relative_to(args.input).as_posix(), **row))
            details.extend(dict(run_id=run_id, **item) for item in items)
        fields = list(results[0])
        if args.central:
            central, columns = read_csv(args.central)
            ids = [r.get('run_id', '') for r in central]
            if 'run_id' not in columns or not all(ids) or len(ids) != len(set(ids)):
                raise ValueError('Centrální CSV musí mít jedinečný neprázdný klíč run_id.')
            updates = {r['run_id']: r for r in results}
            missing = set(updates)-set(ids)
            if missing:
                raise ValueError('V centrální tabulce chybí run_id: '+', '.join(sorted(missing)))
            fields = columns+[f for f in fields if f not in columns]
            results = [dict(r, **updates.get(r['run_id'], {})) for r in central]
        write_csv(args.output, results, fields)
        write_csv(args.details, details, ['run_id','typ','puvodni','normalizovany','platny','radek'])
        print(f'Vyhodnoceno {len(files)} výstupů. CSV: {args.output}. Detaily: {args.details}.')
        return 0
    except (ValueError, OSError, UnicodeError, csv.Error) as e:
        print(f'CHYBA: {e}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
