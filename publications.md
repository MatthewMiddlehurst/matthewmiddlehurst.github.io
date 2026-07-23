---
layout: page
title: Publications
summary: "Automatically generated from ORCID, with optional local overrides for selected papers and notes."
permalink: /publications/
---

<div class="callout">
  This page is generated from my <a href="{{ site.links.orcid }}">ORCID record</a> by a monthly GitHub Action. Curated notes and selected-paper flags are controlled in <code>_data/publication_overrides.json</code>.
</div>

<p>
  External profiles:
  <a href="{{ site.links.orcid }}">ORCID</a> ·
  <a href="{{ site.links.google_scholar }}">Google Scholar</a>
</p>

{% assign selected_publications = site.data.publications | where: "selected", true %}
{% if selected_publications.size > 0 %}
## Selected publications

<ol class="publications">
  {% for pub in selected_publications %}
    {% include publication.html pub=pub %}
  {% endfor %}
</ol>
{% endif %}

## Full list

{% assign publications_by_year = site.data.publications | group_by: "year" | sort: "name" | reverse %}
{% for year in publications_by_year %}
### {{ year.name }}

<ol class="publications">
  {% for pub in year.items %}
    {% include publication.html pub=pub %}
  {% endfor %}
</ol>
{% endfor %}
