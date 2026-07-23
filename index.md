---
layout: default
title: Home
---

<section class="hero" id="home" aria-labelledby="home-title">
  <div class="hero-copy">
    <p class="eyebrow">{{ site.profile.role }} · {{ site.profile.affiliation }}</p>
    <h1 id="home-title">{{ site.profile.name }}</h1>
    <p class="lead">{{ site.profile.short_bio }}</p>
    <p class="hero-summary">My research develops and evaluates machine learning methods for temporal data, with an emphasis on rigorous benchmarking and useful open-source software.</p>
    <div class="hero-actions" aria-label="Contact and academic profiles">
      <a class="button primary" href="mailto:{{ site.profile.email }}">Email me</a>
      <a href="{{ site.links.orcid }}">ORCID</a>
      <a href="{{ site.links.google_scholar }}">Google Scholar</a>
      <a href="{{ site.links.github }}">GitHub</a>
    </div>
  </div>
  <img class="profile-photo" src="{{ site.profile.photo | relative_url }}" alt="Portrait of Matthew Middlehurst">
</section>

<section class="section" id="research" aria-labelledby="research-title">
  <div class="section-header">
    <h2 id="research-title">Research</h2>
    <p>I work on machine learning for ordered observations, including sensor streams, human activity data, industrial measurements, biomedical signals, and other temporal data.</p>
  </div>

  <div class="topic-grid">
    <article class="topic">
      <h3>Classification algorithms</h3>
      <p>Designing and evaluating ensemble, dictionary, interval, convolutional, feature-based, and hybrid approaches to time series classification.</p>
    </article>
    <article class="topic">
      <h3>Benchmarking and reproducibility</h3>
      <p>Developing fair experimental protocols, curated archives, and infrastructure for reliable comparison of time series machine learning algorithms.</p>
    </article>
    <article class="topic">
      <h3>Complex temporal data</h3>
      <p>Learning from multivariate and unequal-length series where channels, missing values, alignment, sampling, and sequence length matter.</p>
    </article>
    <article class="topic">
      <h3>Applied machine learning</h3>
      <p>Working with human activity recognition, rehabilitation, biosignal analysis, and sensor-based monitoring problems.</p>
    </article>
  </div>

  <p class="section-note">I welcome collaborations involving temporal data, reproducible benchmarking, open-source machine learning, and applied sensor data problems.</p>
</section>

<section class="section" id="publications" aria-labelledby="publications-title">
  <div class="section-header with-links">
    <div>
      <h2 id="publications-title">Publications</h2>
      <p>Selected papers are highlighted below, followed by the complete publication list.</p>
    </div>
    <div class="profile-links" aria-label="External publication profiles">
      <a href="{{ site.links.orcid }}">ORCID</a>
      <a href="{{ site.links.google_scholar }}">Google Scholar</a>
    </div>
  </div>

  {% assign selected_publications = site.data.publications | where: "selected", true %}
  {% if selected_publications.size > 0 %}
  <div class="publication-group">
    <h3>Selected publications</h3>
    <ol class="publications">
      {% for pub in selected_publications %}
        {% include publication.html pub=pub %}
      {% endfor %}
    </ol>
  </div>
  {% endif %}

  <div class="publication-group">
    <h3>All publications</h3>
    <div class="publication-archive" role="region" aria-label="Complete publication list" tabindex="0">
      {% assign publications_by_year = site.data.publications | group_by: "year" | sort: "name" | reverse %}
      {% for year in publications_by_year %}
        <h3 class="publication-year">{{ year.name }}</h3>
        <ol class="publications">
          {% for pub in year.items %}
            {% include publication.html pub=pub %}
          {% endfor %}
        </ol>
      {% endfor %}
    </div>
  </div>
</section>

<section class="section" id="software" aria-labelledby="software-title">
  <div class="section-header">
    <h2 id="software-title">Software</h2>
    <p>Research software is a central output of my work and supports reproducible time series machine learning research.</p>
  </div>

  <div class="project-list">
    <article class="project">
      <div>
        <h3>aeon</h3>
        <p class="project-type">Python toolkit</p>
      </div>
      <div>
        <p>A toolkit for learning from time series, covering classification, regression, clustering, forecasting, transformations, distances, and benchmarking utilities.</p>
        <div class="project-links">
          <a href="https://github.com/aeon-toolkit/aeon">GitHub</a>
          <a href="https://www.aeon-toolkit.org/">Documentation</a>
        </div>
      </div>
    </article>
    <article class="project">
      <div>
        <h3>tsml-eval</h3>
        <p class="project-type">Evaluation infrastructure</p>
      </div>
      <div>
        <p>Experiment-running and evaluation tools designed to support reproducible benchmark studies in time series machine learning.</p>
        <div class="project-links">
          <a href="https://github.com/time-series-machine-learning/tsml-eval">GitHub</a>
        </div>
      </div>
    </article>
    <article class="project">
      <div>
        <h3>TSML resources</h3>
        <p class="project-type">Datasets and benchmarks</p>
      </div>
      <div>
        <p>Archives, code, configurations, and data-processing workflows for comparing algorithms across temporal learning tasks.</p>
        <div class="project-links">
          <a href="{{ site.links.github }}">Browse projects</a>
        </div>
      </div>
    </article>
  </div>

  <p class="section-note">When using this software in academic work, please cite the relevant software papers and versioned releases where possible.</p>
</section>

<section class="section" id="teaching" aria-labelledby="teaching-title">
  <div class="section-header">
    <h2 id="teaching-title">Teaching</h2>
    <p>My teaching and project supervision connect core computer science with practical, reproducible machine learning.</p>
  </div>

  <div class="teaching-grid">
    <div>
      <h3>Teaching areas</h3>
      <ul>
        <li>Programming and software development</li>
        <li>Algorithms and data structures</li>
        <li>Machine learning and data science</li>
        <li>Time series machine learning</li>
        <li>Research methods, reproducibility, and academic writing</li>
      </ul>
    </div>
    <div>
      <h3>Supervision interests</h3>
      <ul>
        <li>Time series classification, regression, clustering, and anomaly detection</li>
        <li>Machine learning benchmarking and reproducibility</li>
        <li>Sensor, activity-recognition, health, rehabilitation, and industrial monitoring data</li>
        <li>Python research software and open-source machine learning infrastructure</li>
      </ul>
    </div>
  </div>
</section>
