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
      <a href="{{ '/cv.pdf' | relative_url }}">CV (2025)</a>
    </div>
  </div>
  <img class="profile-photo" src="{{ site.profile.photo | relative_url }}" alt="Portrait of Matthew Middlehurst">
</section>

{% include header.html %}

<section class="section" id="research" aria-labelledby="research-title">
  <div class="section-header">
    <h2 id="research-title">Research</h2>
  </div>

  <div class="topic-grid">
    <article class="topic">
      <h3>Time series learning algorithms</h3>
      <p>Developing accurate and efficient machine learning algorithms for time series.</p>
      <p>I am also interested in anomaly detection and forecasting.</p>
    </article>
    <article class="topic">
      <h3>Benchmarking and open research</h3>
      <p>Designing large-scale comparative studies, curated dataset archives, and reproducible software through aeon and tsml-eval so results can be tested, reused, and extended.</p>
    </article>
  </div>
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

  {% assign published_papers = site.data.publications | where_exp: "pub", "pub.type != 'Preprint'" %}
  {% assign preprints = site.data.publications | where: "type", "Preprint" %}
  {% assign selected_publications = published_papers | where: "selected", true %}
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
    <h3>Published papers</h3>
    <div class="publication-archive" role="region" aria-label="Published papers" tabindex="0">
      <ol class="publications">
        {% for pub in published_papers %}
          {% include publication.html pub=pub %}
        {% endfor %}
      </ol>
    </div>
  </div>
  {% if preprints.size > 0 %}
  <div class="publication-group" id="preprints">
    <h3>Preprints</h3>
    <ol class="publications">
      {% for pub in preprints %}
        {% include publication.html pub=pub %}
      {% endfor %}
    </ol>
  </div>
  {% endif %}
</section>

<section class="section" id="software" aria-labelledby="software-title">
  <div class="section-header">
    <h2 id="software-title">Software and data archives</h2>
    <p>When using these resources in academic work, please cite the relevant papers, datasets, and versioned releases where possible.</p>
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

</section>

<section class="section" id="tutorials-and-demos" aria-labelledby="tutorials-and-demos-title">
  <div class="section-header">
    <h2 id="tutorials-and-demos-title">Tutorials and demos</h2>
  </div>

  <div class="project-group" id="tutorials" aria-labelledby="tutorials-title">
    <h3 class="subsection-title" id="tutorials-title">Tutorials</h3>
    <div class="project-list">
      {% for tutorial in site.data.tutorials %}
      <article class="project">
        <div>
          <h4>{{ tutorial.event | escape }}</h4>
          <p class="project-type">{{ tutorial.role | escape }}</p>
        </div>
        <div>
          <h4>{{ tutorial.title | escape }}</h4>
          <p>{{ tutorial.description | escape }}</p>
          <div class="project-links">
            <a href="{{ tutorial.url | escape }}">Tutorial website</a>
            {% if tutorial.materials_url %}<a href="{{ tutorial.materials_url | escape }}">Slides and code</a>{% endif %}
          </div>
        </div>
      </article>
      {% endfor %}
    </div>
  </div>

  <div class="project-group" id="demos" aria-labelledby="demos-title">
    <h3 class="subsection-title" id="demos-title">Demos</h3>
    <div class="project-list">
      {% for demo in site.data.demos %}
      <article class="project">
        <div>
          <h4>{{ demo.event | escape }}</h4>
        </div>
        <div>
          <h4>{{ demo.title | escape }}</h4>
          <p>{{ demo.description | escape }}</p>
          <div class="project-links">
            <a href="{{ demo.url | escape }}">Demo website</a>
            {% if demo.materials_url %}<a href="{{ demo.materials_url | escape }}">Video and notebook</a>{% endif %}
          </div>
        </div>
      </article>
      {% endfor %}
    </div>
  </div>
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
