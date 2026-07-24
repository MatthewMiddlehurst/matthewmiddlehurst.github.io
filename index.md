---
layout: default
title: Home
---

<section class="hero" id="home" aria-labelledby="home-title">
  <div class="hero-copy">
    <h1 class="hero-name" id="home-title">{{ site.profile.name }}</h1>
    <p class="hero-affiliation">{{ site.profile.affiliation }}</p>
    <p class="hero-role">{{ site.profile.role }}</p>
    <p class="hero-email"><a href="mailto:{{ site.profile.email }}">{{ site.profile.email }}</a></p>
    <div class="hero-about" aria-labelledby="about-title">
      <h2 id="about-title">About me</h2>
      <p>{{ site.profile.short_bio }}</p>
    </div>
    <div class="hero-actions" aria-label="Contact and academic profiles">
      <a class="button primary" href="mailto:{{ site.profile.email }}">Email me</a>
      <a href="{{ site.links.github }}">GitHub</a>
      <a href="{{ site.links.orcid }}">ORCID</a>
      <a href="{{ site.links.google_scholar }}">Google Scholar</a>
      <a href="{{ site.links.linkedin }}">LinkedIn</a>
    </div>
  </div>
  <img class="profile-photo" src="{{ site.profile.photo | relative_url }}" alt="Portrait of Matthew Middlehurst">
</section>

{% include header.html %}

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
      <ol class="publications">
        {% for pub in site.data.publications %}
          {% include publication.html pub=pub %}
        {% endfor %}
      </ol>
    </div>
  </div>
</section>

<section class="section" id="software" aria-labelledby="software-title">
  <div class="section-header">
    <h2 id="software-title">Software and data archives</h2>
    <p>Open-source software and curated benchmark archives are central outputs of my work in reproducible time series machine learning.</p>
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
        <h3>Time Series Classification Archive</h3>
        <p class="project-type">Data archive</p>
      </div>
      <div>
        <p>A collection of univariate and multivariate time series classification datasets, published results, and benchmark resources.</p>
        <div class="project-links">
          <a href="https://www.timeseriesclassification.com/dataset.php">Datasets</a>
          <a href="https://www.timeseriesclassification.com/results.php">Results</a>
        </div>
      </div>
    </article>
    <article class="project">
      <div>
        <h3>Multiverse Archive</h3>
        <p class="project-type">Data archive and benchmarks</p>
      </div>
      <div>
        <p>A multivariate time series classification archive with reproducible experiments, published results, and leaderboard infrastructure.</p>
        <div class="project-links">
          <a href="https://github.com/aeon-toolkit/multiverse">GitHub</a>
          <a href="https://arxiv.org/abs/2603.20352">Paper</a>
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
