import json
import os
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, urlencode, urlparse
from urllib.request import Request, urlopen


CROSSREF_API_BASE = "https://api.crossref.org/works"
CROSSREF_MAILTO = "m.b.middlehurst@bradford.ac.uk"
ORCID_API_BASE = "https://pub.orcid.org/v3.0"
ORCID_RECORD_BASE = "https://orcid.org"
ORCID_TOKEN_URL = "https://orcid.org/oauth/token"
OUTPUT_PATH = Path("_data/publications.json")
OVERRIDES_PATH = Path("_data/publication_overrides.json")
ADDITIONS_PATH = Path("_data/publication_additions.json")
REPORT_PATH_ENV = "PUBLICATION_UPDATE_REPORT"

FEATURED_WORK_SELECTOR = (
    '[id^="cy-panel-component-work-stack-featured-works-"]'
)
REGULAR_WORK_SELECTOR = '[id^="cy-panel-component-work-stack-works-"]'
FEATURED_WORK_ID_PATTERN = re.compile(r"featured-works-(\d+)$")
PREPRINT_HOSTS = {
    "arxiv.org",
    "biorxiv.org",
    "medrxiv.org",
    "ssrn.com",
    "www.ssrn.com",
}
PUBLICATION_TYPE_LABELS = {
    "book-chapter": "Conference paper",
    "conference-paper": "Conference paper",
    "conference-proceedings": "Conference paper",
    "journal-article": "Journal article",
    "preprint": "Preprint",
    "proceedings-article": "Conference paper",
    "report": "Report",
    "working-paper": "Working paper",
}


@dataclass
class FeaturedWorksStatus:
    succeeded: bool
    put_codes: set[int]
    detail: str


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


def clean_text(value):
    """Normalise Unicode spacing and remove source-specific text artefacts."""
    value = unicodedata.normalize("NFKC", str(value or ""))
    value = value.replace("\u00ad", "")
    return " ".join(value.split())


def normalise_publication_type(work_type):
    value = clean_text(work_type).casefold()
    if not value:
        return ""
    return PUBLICATION_TYPE_LABELS.get(
        value,
        value.replace("-", " ").capitalize(),
    )


def normalise_doi(doi):
    """Return a bare, lower-case DOI regardless of its input URL form."""
    value = str(doi or "").strip()
    value = re.sub(r"^doi:\s*", "", value, flags=re.IGNORECASE)
    value = re.sub(
        r"^(?:https?://)?(?:dx\.)?doi\.org/",
        "",
        value,
        flags=re.IGNORECASE,
    )
    return value.strip().casefold()


def doi_url(doi):
    value = normalise_doi(doi)
    return f"https://doi.org/{value}" if value else ""


def is_preprint_doi(doi):
    """Recognise arXiv's DataCite DOIs, which are not Crossref publications."""
    return normalise_doi(doi).startswith("10.48550/arxiv.")


def normalise_url(url):
    """Normalise DOI and common preprint URLs without rewriting other hosts."""
    value = str(url or "").strip()
    if not value:
        return ""

    if re.match(r"^(?:dx\.)?doi\.org/", value, flags=re.IGNORECASE):
        value = f"https://{value}"

    parsed = urlparse(value)
    hostname = (parsed.hostname or "").casefold()

    if hostname in {"doi.org", "dx.doi.org"}:
        return doi_url(parsed.path.lstrip("/"))

    if hostname in PREPRINT_HOSTS and parsed.scheme == "http":
        return parsed._replace(scheme="https").geturl()

    return value


def is_preprint_url(url):
    parsed = urlparse(normalise_url(url))
    hostname = (parsed.hostname or "").casefold()
    return hostname in PREPRINT_HOSTS or (
        hostname == "doi.org" and is_preprint_doi(parsed.path.lstrip("/"))
    )


def arxiv_url(identifier):
    value = str(identifier or "").strip()
    if not value:
        return ""

    if is_preprint_doi(value):
        return f"https://arxiv.org/abs/{normalise_doi(value).split('arxiv.', 1)[1]}"

    if value.startswith(("http://", "https://")):
        return normalise_url(value)

    value = re.sub(r"^arxiv:\s*", "", value, flags=re.IGNORECASE)
    return f"https://arxiv.org/abs/{value}"


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
        value = normalise_doi(value)
    elif prefix == "orcid":
        value = str(value)
    else:
        raise ValueError(f"Unsupported publication override key prefix: {prefix!r}")

    if not value:
        raise ValueError(f"Publication override key has no value: {key!r}")

    return f"{prefix}:{value}"


def load_overrides():
    if not OVERRIDES_PATH.exists():
        return {
            "exclude_keys": set(),
            "url_overrides": {},
            "preprint_overrides": {},
            "author_overrides": {},
        }

    with OVERRIDES_PATH.open(encoding="utf-8") as file:
        data = json.load(file)

    exclude_keys = {
        normalise_override_key(key) for key in data.get("exclude_keys", [])
    }
    url_overrides = {
        normalise_override_key(key): normalise_url(url)
        for key, url in data.get("url_overrides", {}).items()
    }
    preprint_overrides = {
        normalise_override_key(key): normalise_url(url)
        for key, url in data.get("preprint_overrides", {}).items()
    }
    author_overrides = {
        normalise_override_key(key): [clean_text(author) for author in authors]
        for key, authors in data.get("author_overrides", {}).items()
    }

    return {
        "exclude_keys": exclude_keys,
        "url_overrides": url_overrides,
        "preprint_overrides": preprint_overrides,
        "author_overrides": author_overrides,
    }


def publication_override_keys(publication):
    """Build keys from strongest to weakest for matching local overrides."""
    keys = []
    doi = normalise_doi(publication.get("doi"))
    put_code = publication.get("orcid_put_code")
    title = normalise_title(publication.get("title") or "")

    if doi:
        keys.append(f"doi:{doi}")
    if put_code is not None and str(put_code).strip():
        keys.append(f"orcid:{put_code}")
    if title:
        keys.append(f"title:{title}")

    return keys


def load_previous_selected_keys():
    """Preserve the existing selection if Featured Works cannot be read."""
    if not OUTPUT_PATH.exists():
        return set()

    with OUTPUT_PATH.open(encoding="utf-8") as file:
        publications = json.load(file)

    keys = set()
    for publication in publications:
        if publication.get("selected"):
            keys.update(publication_override_keys(publication))

    return keys


def apply_overrides(publication, overrides, selected):
    keys = publication_override_keys(publication)

    if any(key in overrides["exclude_keys"] for key in keys):
        return None

    publication["selected"] = bool(selected)

    url_override = next(
        (
            overrides["url_overrides"][key]
            for key in keys
            if key in overrides["url_overrides"]
        ),
        "",
    )
    if url_override:
        if is_preprint_url(url_override):
            publication["preprint_url"] = url_override
        else:
            publication["url"] = url_override

    preprint_override = next(
        (
            overrides["preprint_overrides"][key]
            for key in keys
            if key in overrides["preprint_overrides"]
        ),
        "",
    )
    if preprint_override and not publication.get("preprint_url"):
        publication["preprint_url"] = preprint_override

    author_override = next(
        (
            overrides["author_overrides"][key]
            for key in keys
            if key in overrides["author_overrides"]
        ),
        [],
    )
    if author_override:
        publication["authors"] = author_override

    return publication


def get_external_ids(work):
    external_ids = get_nested_value(work, ["external-ids", "external-id"], [])
    ids = {"doi": "", "isbn": "", "pmid": "", "arxiv": ""}

    for item in external_ids:
        id_type = str(item.get("external-id-type", "")).casefold()
        id_value = item.get("external-id-value", "")
        relationship = str(item.get("external-id-relationship") or "self").casefold()

        if id_type not in ids or not id_value:
            continue

        # A proceedings/book DOI or another version's DOI does not identify
        # this work. ISBNs may legitimately identify the containing proceedings.
        if id_type in {"doi", "pmid"} and relationship != "self":
            continue
        if id_type == "arxiv" and relationship not in {"self", "version-of"}:
            continue

        if not ids[id_type] or (
            id_type == "doi"
            and is_preprint_doi(ids[id_type])
            and not is_preprint_doi(id_value)
        ):
            ids[id_type] = id_value

    return ids


def get_work_preprint_url(work):
    """Keep the preprint link even when its DOI is not the work's own DOI."""
    external_ids = get_nested_value(work, ["external-ids", "external-id"], [])
    for id_type in ("arxiv", "doi"):
        for item in external_ids:
            relationship = str(
                item.get("external-id-relationship") or "self"
            ).casefold()
            value = item.get("external-id-value", "")
            if relationship not in {"self", "version-of"} or not value:
                continue
            if str(item.get("external-id-type", "")).casefold() != id_type:
                continue
            if id_type == "arxiv" or is_preprint_doi(value):
                return arxiv_url(value)

    work_url = normalise_url(get_nested_value(work, ["url", "value"], ""))
    if is_preprint_url(work_url):
        return arxiv_url(work_url) if is_preprint_doi(work_url) else work_url
    return ""


def is_preprint_work(work):
    """Distinguish a published work with an arXiv link from a preprint copy."""
    if clean_text(work.get("type", "")).casefold() == "preprint":
        return True

    doi = get_external_ids(work)["doi"]
    if doi and not is_preprint_doi(doi):
        return False

    venue = clean_text(get_nested_value(work, ["journal-title", "value"], ""))
    if venue:
        if re.match(r"^(?:arxiv|biorxiv|medrxiv|ssrn)\b", venue.casefold()):
            return True
        if normalise_publication_type(work.get("type", "")) in {
            "Journal article", "Conference paper"
        }:
            return False

    if is_preprint_doi(doi):
        return True

    work_url = normalise_url(get_nested_value(work, ["url", "value"], ""))
    return bool(get_work_preprint_url(work)) and (
        not work_url or is_preprint_url(work_url)
    )


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
            authors.append(clean_text(name))

    return authors


def normalise_work(work):
    external_ids = get_external_ids(work)

    title = clean_text(get_nested_value(work, ["title", "title", "value"], ""))
    subtitle = clean_text(
        get_nested_value(work, ["title", "subtitle", "value"], "")
    )
    translated_title = get_nested_value(
        work,
        ["title", "translated-title", "value"],
        "",
    )

    if subtitle:
        title = f"{title}: {subtitle}"

    doi = normalise_doi(external_ids["doi"])
    work_url = normalise_url(get_nested_value(work, ["url", "value"], ""))
    preprint_url = get_work_preprint_url(work)
    preprint = is_preprint_work(work)
    if not preprint and is_preprint_doi(doi):
        # A journal record may carry only the DOI of its arXiv version.
        doi = ""

    if preprint and preprint_url:
        publication_url = preprint_url
    elif doi and not is_preprint_doi(doi):
        publication_url = doi_url(doi)
    elif work_url and not is_preprint_url(work_url):
        publication_url = work_url
    elif doi:
        publication_url = doi_url(doi)
    else:
        publication_url = preprint_url

    return {
        "title": title,
        "translated_title": clean_text(translated_title),
        "authors": get_authors(work),
        "year": get_year(work),
        "venue": clean_text(
            get_nested_value(work, ["journal-title", "value"], "")
        ),
        "type": (
            "Preprint"
            if preprint
            else normalise_publication_type(work.get("type", ""))
        ),
        "doi": doi,
        "isbn": external_ids["isbn"],
        "pmid": external_ids["pmid"],
        "arxiv": external_ids["arxiv"],
        "url": publication_url,
        "preprint_url": preprint_url,
        "orcid_put_code": work.get("put-code"),
        "source": "ORCID",
    }


def work_quality_score(work):
    """Prefer published metadata over a preprint-only copy in an ORCID group."""
    external_ids = get_external_ids(work)
    work_url = normalise_url(get_nested_value(work, ["url", "value"], ""))

    return (
        not is_preprint_work(work),
        bool(external_ids["doi"] and not is_preprint_doi(external_ids["doi"])),
        bool(get_nested_value(work, ["journal-title", "value"], "")),
        bool(work_url and not is_preprint_url(work_url)),
        len(get_authors(work)),
        bool(get_year(work)),
    )


def fetch_work_groups(orcid_id, token):
    url = f"{ORCID_API_BASE}/{orcid_id}/works"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    data = request_json(url, headers=headers)
    groups = []

    for group in data.get("group", []):
        summaries = [
            summary
            for summary in group.get("work-summary", [])
            if summary.get("put-code") is not None
        ]
        if not summaries:
            continue

        put_codes = {int(summary["put-code"]) for summary in summaries}
        groups.append({"summaries": summaries, "put_codes": put_codes})

    return groups


def fetch_work(orcid_id, put_code, token):
    url = f"{ORCID_API_BASE}/{orcid_id}/work/{put_code}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    return request_json(url, headers=headers)


def fetch_best_group_work(orcid_id, group, token):
    best_score = max(work_quality_score(summary) for summary in group["summaries"])
    # ORCID summaries omit contributors. Fetch equally ranked candidates so
    # records with complete author lists win over incomplete duplicates.
    candidates = [
        fetch_work(orcid_id, summary["put-code"], token)
        for summary in group["summaries"]
        if work_quality_score(summary) == best_score
    ]
    return max(candidates, key=work_quality_score)


def get_group_preprint_url(group):
    """Find a preprint identifier from any source in an ORCID work group."""
    for summary in group["summaries"]:
        preprint_url = get_work_preprint_url(summary)
        if preprint_url:
            return preprint_url

    return ""


def get_crossref_year(metadata):
    """Prefer the citation/issue year, then Crossref's general publication year."""
    for field in ("published-print", "published", "issued", "published-online"):
        date_parts = get_nested_value(metadata, [field, "date-parts"], [])
        if date_parts and date_parts[0] and str(date_parts[0][0]).isdigit():
            return int(date_parts[0][0])
    return None


def get_crossref_authors(metadata):
    authors = []

    for author in metadata.get("author", []):
        name = clean_text(
            " ".join(
                part
                for part in (
                    author.get("given", ""),
                    author.get("family", ""),
                    author.get("suffix", ""),
                )
                if part
            )
        )
        if not name:
            name = clean_text(author.get("name", ""))
        if name:
            authors.append(name)

    return authors


def fetch_crossref_metadata(doi):
    url = (
        f"{CROSSREF_API_BASE}/{quote(normalise_doi(doi), safe='')}"
        f"?mailto={quote(CROSSREF_MAILTO, safe='@')}"
    )
    headers = {
        "Accept": "application/json",
        "User-Agent": (
            "MatthewMiddlehurstWebsite/1.0 "
            f"(mailto:{CROSSREF_MAILTO})"
        ),
    }
    return request_json(url, headers=headers).get("message", {})


def enrich_with_crossref(publication):
    """Use DOI metadata to make titles, authors, venues and types consistent."""
    doi = publication.get("doi")
    if not doi or is_preprint_doi(doi):
        return publication

    metadata = fetch_crossref_metadata(doi)

    titles = metadata.get("title", [])
    if titles:
        publication["title"] = clean_text(titles[0])

    authors = get_crossref_authors(metadata)
    if authors:
        publication["authors"] = authors

    containers = [
        clean_text(container)
        for container in metadata.get("container-title", [])
        if clean_text(container)
    ]
    if containers:
        publication["venue"] = containers[-1]

    year = get_crossref_year(metadata)
    if year:
        publication["year"] = year

    crossref_type = metadata.get("type", "")
    if crossref_type:
        publication["type"] = normalise_publication_type(crossref_type)

    return publication


def concise_error(error):
    detail = " ".join(str(error).split()) or error.__class__.__name__
    return detail[:500]


def fetch_featured_put_codes(orcid_id):
    """Read Featured Works from the public ORCID page.

    ORCID's public API does not currently expose the Featured Works selection,
    so this deliberately isolated browser step reads the identifiers rendered
    by the public record. Any failure is reported and handled non-destructively.
    """
    try:
        from playwright.sync_api import sync_playwright
    except Exception as error:
        return FeaturedWorksStatus(
            False,
            set(),
            f"Playwright was unavailable: {concise_error(error)}",
        )

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(
                    f"{ORCID_RECORD_BASE}/{orcid_id}",
                    wait_until="domcontentloaded",
                    timeout=60_000,
                )
                page.wait_for_selector(REGULAR_WORK_SELECTOR, timeout=60_000)
                page.wait_for_timeout(2_000)

                element_ids = page.locator(FEATURED_WORK_SELECTOR).evaluate_all(
                    "(elements) => elements.map((element) => element.id)"
                )
                put_codes = {
                    int(match.group(1))
                    for element_id in element_ids
                    if (match := FEATURED_WORK_ID_PATTERN.search(element_id))
                }

                featured_heading_present = (
                    page.get_by_text("Featured works", exact=True).count() > 0
                )
                if featured_heading_present and not put_codes:
                    return FeaturedWorksStatus(
                        False,
                        set(),
                        "The Featured Works section was visible, but its work "
                        "identifiers could not be read.",
                    )

                return FeaturedWorksStatus(
                    True,
                    put_codes,
                    "Featured Works were read from the public ORCID record.",
                )
            finally:
                browser.close()
    except Exception as error:
        return FeaturedWorksStatus(
            False,
            set(),
            f"The public ORCID page could not be read: {concise_error(error)}",
        )


def validate_featured_put_codes(status, groups):
    if not status.succeeded:
        return status

    known_put_codes = set()
    for group in groups:
        known_put_codes.update(group["put_codes"])

    unmatched = status.put_codes - known_put_codes
    if unmatched:
        values = ", ".join(str(value) for value in sorted(unmatched))
        return FeaturedWorksStatus(
            False,
            set(),
            "Featured Works were found on the public page but not in the "
            f"ORCID API response (put codes: {values}).",
        )

    return status


def write_publications(publications):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_PATH.write_text(
        json.dumps(publications, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def merge_publication_additions(publications, overrides):
    """Include curated works missing from ORCID without duplicating later imports."""
    if not ADDITIONS_PATH.exists():
        return publications

    additions = json.loads(ADDITIONS_PATH.read_text(encoding="utf-8"))
    for addition in additions:
        addition = apply_overrides(dict(addition), overrides, addition.get("selected", False))
        if addition is None:
            continue
        keys = set(publication_override_keys(addition))
        match = next(
            (i for i, pub in enumerate(publications)
             if keys.intersection(publication_override_keys(pub))),
            None,
        )
        if match is None:
            publications.append(addition)
        elif publications[match].get("type") == "Preprint" and addition.get("type") != "Preprint":
            addition["selected"] = publications[match].get("selected", False)
            addition.setdefault("preprint_url", publications[match].get("preprint_url", ""))
            publications[match] = addition
    return publications


def write_update_report(
    publications,
    featured_status,
    crossref_enriched_count,
    crossref_failures,
):
    selected_count = sum(
        1 for publication in publications if publication.get("selected")
    )
    lines = [
        (
            f"- Publication import: **succeeded** — "
            f"{len(publications)} works written, including any curated additions."
        )
    ]

    if crossref_failures:
        failed_dois = ", ".join(crossref_failures)
        lines.extend(
            [
                "- Crossref metadata enrichment: **partially failed** — "
                f"{crossref_enriched_count} DOI records were standardised; "
                f"{len(crossref_failures)} retained their ORCID formatting.",
                f"  - Affected DOI(s): {failed_dois}",
            ]
        )
    else:
        lines.append(
            "- Crossref metadata enrichment: **succeeded** — "
            f"{crossref_enriched_count} DOI records were standardised."
        )

    if featured_status.succeeded:
        lines.append(
            f"- ORCID Featured Works sync: **succeeded** — "
            f"{len(featured_status.put_codes)} Featured Works found and "
            f"{selected_count} publications selected on the website."
        )
    else:
        lines.extend(
            [
                "- ORCID Featured Works sync: **failed** — the previous "
                "website selection was retained.",
                f"  - Reason: {featured_status.detail}",
            ]
        )

    report = "\n".join(lines) + "\n"
    report_path = os.environ.get(REPORT_PATH_ENV)
    if report_path:
        Path(report_path).write_text(report, encoding="utf-8")

    print(report, end="")


def main():
    orcid_id = require_env("ORCID_ID")
    client_id = require_env("ORCID_CLIENT_ID")
    client_secret = require_env("ORCID_CLIENT_SECRET")

    previous_selected_keys = load_previous_selected_keys()
    featured_status = fetch_featured_put_codes(orcid_id)
    token = get_access_token(client_id, client_secret)
    overrides = load_overrides()
    groups = fetch_work_groups(orcid_id, token)
    featured_status = validate_featured_put_codes(featured_status, groups)

    publications = []
    crossref_enriched_count = 0
    crossref_failures = []

    for group in groups:
        work = fetch_best_group_work(orcid_id, group, token)
        publication = normalise_work(work)
        group_preprint_url = get_group_preprint_url(group)
        if group_preprint_url:
            publication["preprint_url"] = group_preprint_url

        if publication["doi"] and not is_preprint_doi(publication["doi"]):
            try:
                publication = enrich_with_crossref(publication)
                crossref_enriched_count += 1
            except Exception:
                crossref_failures.append(publication["doi"])

        if featured_status.succeeded:
            selected = bool(group["put_codes"] & featured_status.put_codes)
        else:
            selected = any(
                key in previous_selected_keys
                for key in publication_override_keys(publication)
            )

        publication = apply_overrides(publication, overrides, selected)

        if publication and publication["title"]:
            publications.append(publication)

    if not publications:
        raise RuntimeError(
            "ORCID returned no publications; refusing to overwrite the data file."
        )

    publications = merge_publication_additions(publications, overrides)

    publications.sort(
        key=lambda item: (
            item["year"] or 0,
            item["title"].casefold(),
        ),
        reverse=True,
    )

    write_publications(publications)
    write_update_report(
        publications,
        featured_status,
        crossref_enriched_count,
        crossref_failures,
    )
    print(f"Wrote {len(publications)} publications to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
