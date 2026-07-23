## Publications

The monthly `update-publications.yml` workflow imports the public works from ORCID. It uses the `ORCID_CLIENT_ID` and `ORCID_CLIENT_SECRET` repository secrets and writes the generated list to `_data/publications.json`.

Curated selections, exclusions, and notes live in `_data/publication_overrides.json`. Override keys use a stable prefix:

- `doi:` followed by a lowercase DOI;
- `orcid:` followed by an ORCID work put-code; or
- `title:` followed by a lowercase title with punctuation removed.
