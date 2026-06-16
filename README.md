# Matthew Middlehurst academic website

A lightweight Jekyll academic homepage designed for GitHub Pages.

## What this contains

- Modern custom Jekyll layout with no heavy theme dependency.
- Pages for research, publications, software, teaching, and CV.
- DBLP-driven publication updates via GitHub Actions.
- GitHub Pages deployment via GitHub Actions.
- Placeholder profile image and editable site metadata.

## Recommended repository

For the cleanest URL, create a repository named:

```text
matthewmiddlehurst.github.io
```

Then push these files to its `main` branch.

Your existing `MatthewMiddlehurst/MatthewMiddlehurst` repository can remain as your GitHub profile README and link to this site.

## First edits to make

Edit `_config.yml`:

```yaml
profile:
  email: "TODO: add academic email"
links:
  university: "TODO: add University of Bradford profile URL"
```

Replace the placeholder image:

```text
assets/images/profile-placeholder.svg
```

with a real photo, for example:

```text
assets/images/profile.jpg
```

and update `_config.yml`:

```yaml
profile:
  photo: "/assets/images/profile.jpg"
```

## Publications

The publication page is generated from:

```text
_data/publications.json
```

The GitHub Action `.github/workflows/update-publications.yml` updates that file from DBLP using:

```yaml
DBLP_PID: "245/9003"
```

Manual curation lives in:

```text
_data/publication_overrides.json
```

Use it to mark selected papers, add notes, or exclude records.

Example:

```json
{
  "selected_keys": ["journals/jmlr/MiddlehurstIGHG24"],
  "exclude_keys": ["journals/corr/abs-2304-13029"],
  "notes": {
    "journals/jmlr/MiddlehurstIGHG24": "Software paper for the aeon toolkit."
  }
}
```

Run locally:

```bash
python scripts/update_publications.py
```

## Local preview

Install Ruby and Bundler, then run:

```bash
bundle install
bundle exec jekyll serve
```

Open the local URL printed by Jekyll, usually:

```text
http://127.0.0.1:4000
```

## GitHub Pages setup

In the GitHub repository:

1. Go to **Settings → Pages**.
2. Under **Build and deployment**, choose **GitHub Actions**.
3. Push to `main`, or run **Build and deploy site** manually from the Actions tab.
4. Run **Update publications** manually once to refresh the publication list.

## Useful optional automations

- Monthly link checker for broken external URLs.
- Scheduled CV PDF rebuild if you keep a Markdown/LaTeX CV in the repo.
- GitHub repository statistics update for aeon/tsml-eval cards.
- News item generator from tagged GitHub releases or a small `_data/news.yml` file.
- Lighthouse/PageSpeed check on pull requests.
