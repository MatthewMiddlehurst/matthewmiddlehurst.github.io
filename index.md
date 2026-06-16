---
layout: default
title: Home
---

<section class="hero">
  <div>
    <p class="eyebrow">{{ site.profile.role }} · {{ site.profile.affiliation }}</p>
    <h1>{{ site.profile.name }}</h1>
    <p class="lead">{{ site.profile.short_bio }}</p>
    <div class="hero-meta">
      <span class="pill">Time series machine learning</span>
      <span class="pill">Classification and benchmarking</span>
      <span class="pill">Open-source research software</span>
    </div>
    <p style="margin-top: 1.5rem;">
      <a class="button primary" href="{{ '/research/' | relative_url }}">Research overview</a>
      <a class="button" href="{{ '/publications/' | relative_url }}">Publications</a>
      <a class="button" href="{{ site.links.orcid }}">ORCID</a>
    </p>
  </div>
  <img class="profile-photo" src="{{ site.profile.photo | relative_url }}" alt="Profile photograph placeholder">
</section>

<section class="section">
  <div class="section-header">
    <h2>Research focus</h2>
    <p>My work develops, evaluates, and maintains practical machine learning methods for temporal data.</p>
  </div>
  <div class="grid">
    <article class="card">
      <h3>Time series classification</h3>
      <p>Methods for classifying ordered observations, including ensembles, dictionary methods, interval methods, and deep learning baselines.</p>
    </article>
    <article class="card">
      <h3>Benchmarking and reproducibility</h3>
      <p>Large-scale experimental evaluation, archive curation, and software infrastructure for reliable comparison of TSML algorithms.</p>
    </article>
    <article class="card">
      <h3>Multivariate and unequal-length data</h3>
      <p>Learning from sensor streams where channels, timing, alignment, and sequence length matter.</p>
    </article>
  </div>
</section>

<section class="section">
  <div class="section-header">
    <h2>Featured software</h2>
    <p>Research software is a central output of my work, not just an implementation detail.</p>
  </div>
  <div class="grid">
    <article class="card">
      <h3>aeon</h3>
      <p>A Python toolkit for learning from time series, including classification, regression, clustering, forecasting, and transformations.</p>
      <div class="links"><a href="https://github.com/aeon-toolkit/aeon">GitHub</a><a href="https://www.aeon-toolkit.org/">Docs</a></div>
    </article>
    <article class="card">
      <h3>tsml-eval</h3>
      <p>Experiment-running and evaluation utilities for time series machine learning benchmarking.</p>
      <div class="links"><a href="https://github.com/time-series-machine-learning/tsml-eval">GitHub</a></div>
    </article>
    <article class="card">
      <h3>TSML resources</h3>
      <p>Datasets, archives, and reproducible evaluation resources for time series machine learning research.</p>
      <div class="links"><a href="{{ site.links.github }}">GitHub profile</a></div>
    </article>
  </div>
</section>

<section class="section">
  <div class="section-header">
    <h2>Selected publications</h2>
    <p>For a full automatically generated list, see the publications page.</p>
  </div>
  <ol class="publications">
    {% assign selected = site.data.publications | where: "selected", true | slice: 0, 4 %}
    {% for pub in selected %}
      {% include publication.html pub=pub %}
    {% endfor %}
  </ol>
</section>

<section class="section">
  <div class="section-header">
    <h2>Contact and profiles</h2>
  </div>
  <div class="grid two">
    <article class="card">
      <h3>Academic profile</h3>
      <p>{{ site.profile.role }}, {{ site.profile.affiliation }}. Replace the placeholder email and university link in <code>_config.yml</code>.</p>
    </article>
    <article class="card">
      <h3>External links</h3>
      <p>
        <a href="{{ site.links.github }}">GitHub</a> ·
        <a href="{{ site.links.orcid }}">ORCID</a> ·
        <a href="{{ site.links.dblp }}">DBLP</a> ·
        <a href="{{ site.links.google_scholar }}">Google Scholar</a> ·
        <a href="{{ site.links.linkedin }}">LinkedIn</a>
      </p>
    </article>
  </div>
</section>
