#!/usr/bin/env python3
"""Fetch publications from DBLP and write Jekyll data JSON.

Default author: Matthew Middlehurst, DBLP PID 245/9003.

The script intentionally writes static data for Jekyll rather than making the
website call DBLP at page-load time. This keeps the public site fast and robust.
"""

from __future__ import annotations

import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "_data"
OUTPUT_PATH = DATA_DIR / "publications.json"
OVERRIDES_PATH = DATA_DIR / "publication_overrides.json"

DBLP_PID = os.environ.get("DBLP_PID", "245/9003")
DBLP_XML_URL = os.environ.get("DBLP_XML_URL", f"https://dblp.org/pid/{DBLP_PID}.xml")

RECORD_TAGS = {
    "article",
    "inproceedings",
    "proceedings",
    "book",
    "incollection",
    "phdthesis",
    "mastersthesis",
    "www",
}

TYPE_PRIORITY = {
    "journal": 0,
    "conference": 1,
    "book": 2,
    "chapter": 3,
    "thesis": 4,
    "preprint": 5,
    "web": 6,
    "other": 7,
}


def text_of(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return html.unescape("".join(element.itertext())).strip().rstrip(".")


def child_text(record: ET.Element, tag: str) -> str:
    return text_of(record.find(tag))


def all_child_text(record: ET.Element, tag: str) -> list[str]:
    return [text_of(child) for child in record.findall(tag) if text_of(child)]


def normalise_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title.casefold())
    title = re.sub(r"[^a-z0-9 ]", "", title)
    return title.strip()


def venue_and_type(record: ET.Element) -> tuple[str, str]:
    tag = record.tag
    journal = child_text(record, "journal")
    booktitle = child_text(record, "booktitle")
    school = child_text(record, "school")
    publisher = child_text(record, "publisher")

    if tag == "article":
        if journal.casefold() in {"corr", "arxiv"} or "CoRR" in journal:
            return journal or "arXiv", "preprint"
        return journal, "journal"
    if tag == "inproceedings":
        return booktitle, "conference"
    if tag == "incollection":
        return booktitle or publisher, "chapter"
    if tag == "book":
        return publisher, "book"
    if tag in {"phdthesis", "mastersthesis"}:
        return school, "thesis"
    if tag == "www":
        return "Web profile", "web"
    return booktitle or journal or publisher, "other"


def extract_doi(urls: list[str]) -> str:
    for url in urls:
        match = re.search(r"(?:doi\.org/|doi=)(10\.\d{4,9}/[^\s?#]+)", url, flags=re.I)
        if match:
            return match.group(1).rstrip(".")
    return ""


def parse_year(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def load_overrides() -> dict[str, Any]:
    if not OVERRIDES_PATH.exists():
        return {"selected_keys": [], "exclude_keys": [], "notes": {}}
    with OVERRIDES_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("selected_keys", [])
    data.setdefault("exclude_keys", [])
    data.setdefault("notes", {})
    return data


def fetch_xml() -> bytes:
    request = urllib.request.Request(
        DBLP_XML_URL,
        headers={"User-Agent": "academic-homepage-publication-updater/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def parse_publications(xml_bytes: bytes, overrides: dict[str, Any]) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_bytes)
    excluded = set(overrides.get("exclude_keys", []))
    selected = set(overrides.get("selected_keys", []))
    notes = dict(overrides.get("notes", {}))

    publications: list[dict[str, Any]] = []

    # DBLP person XML stores bibliographic records inside <r> wrappers.
    for wrapper in root.findall("r"):
        record = next((child for child in list(wrapper) if child.tag in RECORD_TAGS), None)
        if record is None:
            continue

        key = record.attrib.get("key", "")
        if key in excluded:
            continue

        title = child_text(record, "title")
        if not title:
            continue

        authors = all_child_text(record, "author") or all_child_text(record, "editor")
        venue, pub_type = venue_and_type(record)
        year = parse_year(child_text(record, "year"))
        urls = all_child_text(record, "ee")
        url = urls[0] if urls else (f"https://dblp.org/rec/{key}" if key else "")
        doi = extract_doi(urls)

        publications.append(
            {
                "title": title,
                "authors": authors,
                "venue": venue,
                "year": year,
                "type": pub_type,
                "url": url,
                "doi": doi,
                "dblp_key": key,
                "selected": key in selected,
                "note": notes.get(key, ""),
            }
        )

    # Prefer published records over duplicate arXiv/CoRR records with the same title.
    deduped: dict[str, dict[str, Any]] = {}
    for pub in publications:
        norm_title = normalise_title(pub["title"])
        existing = deduped.get(norm_title)
        if existing is None:
            deduped[norm_title] = pub
            continue

        current_rank = (TYPE_PRIORITY.get(pub["type"], 99), -int(pub["year"] or 0))
        existing_rank = (TYPE_PRIORITY.get(existing["type"], 99), -int(existing["year"] or 0))
        if current_rank < existing_rank:
            # Preserve selected/note if either duplicate was manually curated.
            pub["selected"] = bool(pub.get("selected") or existing.get("selected"))
            pub["note"] = pub.get("note") or existing.get("note", "")
            deduped[norm_title] = pub

    return sorted(
        deduped.values(),
        key=lambda p: (int(p.get("year") or 0), TYPE_PRIORITY.get(p.get("type", "other"), 99), p.get("title", "")),
        reverse=True,
    )


def write_json(publications: list[dict[str, Any]]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    payload = json.dumps(publications, indent=2, ensure_ascii=False) + "\n"
    OUTPUT_PATH.write_text(payload, encoding="utf-8")

    stamp = ROOT / "_data" / "publications_generated_at.txt"
    stamp.write_text(datetime.now(timezone.utc).isoformat(timespec="seconds") + "\n", encoding="utf-8")


def main() -> int:
    try:
        overrides = load_overrides()
        xml_bytes = fetch_xml()
        publications = parse_publications(xml_bytes, overrides)
        if not publications:
            raise RuntimeError("No publications parsed from DBLP response")
        write_json(publications)
    except (urllib.error.URLError, ET.ParseError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"Publication update failed: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {len(publications)} publications to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
