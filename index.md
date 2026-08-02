---
layout: default
title: Home
---

<section class="hero" id="home" aria-labelledby="home-title">
  <div class="hero-copy">
    <h1 class="hero-name" id="home-title">{{ site.profile.name }}</h1>
    <p class="hero-role">{{ site.profile.role }}</p>
    <p class="hero-affiliation">{{ site.profile.affiliation }}</p>
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
    <p>My research develops methods and open-source infrastructure for learning from time series. I work across classification, regression, and clustering, with a particular focus on reliable evaluation and on data that depart from the clean, equal-length assumptions used by many algorithms.</p>
  </div>

  <div class="topic-grid">
    <article class="topic">
      <h3>Time series learning algorithms</h3>
      <p>Developing ensemble, dictionary, interval, feature-based, and hybrid methods for classification, while extending these ideas to extrinsic regression and clustering.</p>
    </article>
    <article class="topic">
      <h3>Benchmarking and open research</h3>
      <p>Designing large-scale comparative studies, curated dataset archives, and reproducible software through aeon and tsml-eval so results can be tested, reused, and extended.</p>
    </article>
    <article class="topic">
      <h3>Complex and streaming data</h3>
      <p>Learning from multivariate, unequal-length, and continuously arriving series, including segmentation, missing or unexpected data, and methods suitable for real-time decisions.</p>
    </article>
    <article class="topic">
      <h3>Health and human movement</h3>
      <p>Applying time series methods to EEG, human activity recognition, and rehabilitation, including movement-quality assessment from skeletal motion and wearable inertial sensors.</p>
    </article>
  </div>

  <p class="section-note">Current directions include robust unequal-length classification, multivariate benchmark archives, real-time sensor-stream analysis, and rehabilitation applications. I welcome collaboration on methodological, applied, and open-source projects.</p>
</section>

<section class="section" id="publications" aria-labelledby="publications-title">
  <div class="section-header with-links">
    <div>
      <h2 id="publications-title">Publications</h2>
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

  <div class="project-group" aria-labelledby="software-projects-title">
    <h3 class="subsection-title" id="software-projects-title">Software</h3>
    <div class="project-list">
      <article class="project">
      <div>
        <h4>aeon</h4>
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
        <h4>tsml-eval</h4>
        <p class="project-type">Evaluation infrastructure</p>
      </div>
      <div>
        <p>Experiment-running and evaluation tools designed to support reproducible benchmark studies in time series machine learning.</p>
        <div class="project-links">
          <a href="https://github.com/time-series-machine-learning/tsml-eval">GitHub</a>
        </div>
      </div>
      </article>
    </div>
  </div>

  <div class="project-group" aria-labelledby="data-archives-title">
    <h3 class="subsection-title" id="data-archives-title">Data archives</h3>
    <div class="project-list">
      <article class="project">
      <div>
        <h4>Time Series Classification Archive</h4>
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
        <h4>Multiverse Archive</h4>
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
  </div>

  <p class="section-note">When using these resources in academic work, please cite the relevant papers, datasets, and versioned releases where possible.</p>
</section>

<section class="section" id="teaching" aria-labelledby="teaching-title">
  <div class="section-header">
    <h2 id="teaching-title">Teaching</h2>
    <p>My teaching and project supervision connect core computer science with practical, reproducible machine learning.</p>
  </div>

  <div class="teaching-grid">
    <div>
      <h3>Teaching experience</h3>
      <p>I am module leader for <em>Fundamentals of Programming</em> and <em>Technical and Professional Skills</em>, delivered through the Yangzhou University-University of Bradford Joint College of Advanced Manufacturing. This has included a month of in-person teaching in China.</p>
    </div>
    <div>
      <h3>Project supervision</h3>
      <p>I currently supervise one PhD student and one MSc student, and have supervised five completed undergraduate final-year projects. Potential projects can be scoped for undergraduate, master's, and PhD study in:</p>
      <ul>
        <li>Time series classification, regression, clustering, and anomaly detection</li>
        <li>Machine learning benchmarking and reproducibility</li>
        <li>Sensor, activity-recognition, health, rehabilitation, and industrial monitoring data</li>
        <li>Python research software and open-source machine learning infrastructure</li>
      </ul>
    </div>
  </div>
</section>
