# matthewmiddlehurst.github.io

This repository contains the source for my academic website at [matthewmiddlehurst.github.io](https://matthewmiddlehurst.github.io/).

The site is built with Jekyll and hosted using GitHub Pages.

## Publications

The monthly **Update publications from ORCID** workflow imports public ORCID
works, enriches publisher DOIs with Crossref metadata, and opens a reviewable PR.
It prefers published records over preprints and preserves the previous selected
papers if ORCID Featured Works cannot be read. Preprints are displayed separately
from published papers.

- `_data/publication_overrides.json` holds canonical links and author corrections.
- `_data/publication_additions.json` holds verified works not yet in ORCID. These
  are merged by DOI or normalised title, so later ORCID imports do not duplicate
  them. Remove a curated preprint once a differently titled published version is
  imported.
- `_data/publications.json` is the generated site data; do not edit it to make
  permanent corrections.
- `_data/tutorials.json` and `_data/demos.json` populate the separate Tutorials
  and demos section before Teaching. Entries use event years; tutorials
  distinguish presenters from contributors. Associated proceedings papers remain
  in Publications.

The updater requires the repository secrets `ORCID_CLIENT_ID` and
`ORCID_CLIENT_SECRET`. In **Settings > Actions > General > Workflow permissions**,
enable **Allow GitHub Actions to create and approve pull requests**. Default
workflow permissions can remain read-only; the updater explicitly requests the
contents and pull-request permissions it needs. Updates still require merging
the generated PR; this workflow does not approve or merge it.

## Checks

**Check links** builds the site with the GitHub Pages Jekyll builder before
checking generated HTML, including publication URLs and navigation anchors. It
runs for pull requests, pushes to `main`, monthly, and manually via Actions.
Results appear in the workflow summary.
Two profile URLs (Google Scholar and LinkedIn) block automated runners and are
excluded in `.github/lychee.toml`; check these manually when changing them. The
ACM tutorial DOI is checked against its Crossref record because ACM also blocks
the runner. Other external URLs and error status codes are checked normally.

Run importer regression tests locally with:

```sh
python -B -m unittest discover -s tests -v
```
