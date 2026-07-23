import json
import os
import re
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ORCID_API_BASE = "https://pub.orcid.org/v3.0"
ORCID_TOKEN_URL = "https://orcid.org/oauth/token"
OUTPUT_PATH = Path("_data/publications.json")
OVERRIDES_PATH = Path("_data/publication_overrides.json")


def require_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def request_json(url, headers=None, data=None):
    request = Request(url, headers=headers or {}, data=data)
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def get_access_token(client_id, client_secret):
    data = urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "scope": "/read-public",
        }
    ).encode("utf-8")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = request_json(ORCID_TOKEN_URL, headers=headers, data=data)
    token = response.get("access_token")

    if not token:
        raise RuntimeError("ORCID did not return an access token.")

    return token


def get_nested_value(data, keys, default=""):
    current = data

    for key in keys:
        if not isinstance(current, dict):
            return default

        current = current.get(key)

        if current is None:
            return default

    return current


def normalise_title(title):
    """Return a stable, punctuation-insensitive title for override matching."""
    return re.sub(r"[^a-z0-9]+", " ", str(title).casefold()).strip()


def normalise_override_key(key):
    """Normalise the prefix and value of a configured override key."""
    prefix, separator, value = str(key).partition(":")
    if not separator:
        raise ValueError(f"Invalid publication override key: {key!r}")

    prefix = prefix.strip().casefold()
    value = value.strip()

    if prefix == "title":
        value = normalise_title(value)
    elif prefix == "doi":
        value = value.casefold()
    elif prefix == "orcid":
        value = str(value)
    else:
        raise ValueError(f"Unsupported publication override key prefix: {prefix!r}")

    if not value:
        raise ValueError(f"Publication override key has no value: {key!r}")

    return f"{prefix}:{value}"


def load_overrides():
    if not OVERRIDES_PATH.exists():
        return {"selected_keys": set(), "exclude_keys": set(), "notes": {}}

    with OVERRIDES_PATH.open(encoding="utf-8") as file:
        data = json.load(file)

    selected_keys = {
        normalise_override_key(key) for key in data.get("selected_keys", [])
    }
    exclude_keys = {
        normalise_override_key(key) for key in data.get("exclude_keys", [])
    }
    notes = {
        normalise_override_key(key): note
        for key, note in data.get("notes", {}).items()
    }

    return {
        "selected_keys": selected_keys,
        "exclude_keys": exclude_keys,
        "notes": notes,
    }


def publication_override_keys(publication):
    """Build keys from strongest to weakest for matching local overrides."""
    keys = []
    doi = str(publication.get("doi") or "").strip().casefold()
    put_code = publication.get("orcid_put_code")
    title = normalise_title(publication.get("title") or "")

    if doi:
        keys.append(f"doi:{doi}")
    if put_code is not None and str(put_code).strip():
        keys.append(f"orcid:{put_code}")
    if title:
        keys.append(f"title:{title}")

    return keys


def apply_overrides(publication, overrides):
    keys = publication_override_keys(publication)

    if any(key in overrides["exclude_keys"] for key in keys):
        return None

    publication["selected"] = any(
        key in overrides["selected_keys"] for key in keys
    )
    publication["note"] = next(
        (overrides["notes"][key] for key in keys if key in overrides["notes"]),
        "",
    )
    return publication


def get_external_ids(work):
    external_ids = get_nested_value(work, ["external-ids", "external-id"], [])
    ids = {"doi": "", "isbn": "", "pmid": "", "arxiv": "", "url": ""}

    for item in external_ids:
        id_type = item.get("external-id-type", "").lower()
        id_value = item.get("external-id-value", "")
        id_url = get_nested_value(item, ["external-id-url", "value"], "")

        if id_type in ids and id_value:
            ids[id_type] = id_value

        if id_type == "doi" and id_value:
            ids["url"] = id_url or f"https://doi.org/{id_value}"

    return ids


def get_year(work):
    year = get_nested_value(work, ["publication-date", "year", "value"], "")

    if str(year).isdigit():
        return int(year)

    return None


def get_authors(work):
    contributors = get_nested_value(work, ["contributors", "contributor"], [])
    authors = []

    for contributor in contributors:
        name = get_nested_value(contributor, ["credit-name", "value"], "")
        if name:
            authors.append(name)

    return authors


def normalise_work(work):
    external_ids = get_external_ids(work)

    title = get_nested_value(work, ["title", "title", "value"], "")
    subtitle = get_nested_value(work, ["title", "subtitle", "value"], "")
    translated_title = get_nested_value(work, ["title", "translated-title", "value"], "")

    if subtitle:
        title = f"{title}: {subtitle}"

    url = get_nested_value(work, ["url", "value"], "") or external_ids["url"]

    return {
        "title": title,
        "translated_title": translated_title,
        "authors": get_authors(work),
        "year": get_year(work),
        "venue": get_nested_value(work, ["journal-title", "value"], ""),
        "type": work.get("type", ""),
        "doi": external_ids["doi"],
        "isbn": external_ids["isbn"],
        "pmid": external_ids["pmid"],
        "arxiv": external_ids["arxiv"],
        "url": url,
        "orcid_put_code": work.get("put-code"),
        "source": "ORCID",
    }


def fetch_work_summaries(orcid_id, token):
    url = f"{ORCID_API_BASE}/{orcid_id}/works"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    data = request_json(url, headers=headers)
    summaries = []

    for group in data.get("group", []):
        work_summaries = group.get("work-summary", [])
        if work_summaries:
            summaries.append(work_summaries[0])

    return summaries


def fetch_work(orcid_id, put_code, token):
    url = f"{ORCID_API_BASE}/{orcid_id}/work/{put_code}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    return request_json(url, headers=headers)


def write_publications(publications):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_PATH.write_text(
        json.dumps(publications, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

if __name__ == "__main__":
    orcid_id = require_env("ORCID_ID")
    client_id = require_env("ORCID_CLIENT_ID")
    client_secret = require_env("ORCID_CLIENT_SECRET")

    token = get_access_token(client_id, client_secret)
    overrides = load_overrides()
    summaries = fetch_work_summaries(orcid_id, token)

    publications = []

    for summary in summaries:
        put_code = summary.get("put-code")
        if not put_code:
            continue

        work = fetch_work(orcid_id, put_code, token)
        publication = normalise_work(work)
        publication = apply_overrides(publication, overrides)

        if publication and publication["title"]:
            publications.append(publication)

    if not publications:
        raise RuntimeError(
            "ORCID returned no publications; refusing to overwrite the data file."
        )

    publications.sort(
        key=lambda item: (
            item["year"] or 0,
            item["title"].lower(),
        ),
        reverse=True,
    )

    write_publications(publications)

    print(f"Wrote {len(publications)} publications to {OUTPUT_PATH}")
