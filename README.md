# Hikaru Asano - Personal Academic Website

A personal academic website built with Jekyll and GitHub Pages, using the [Minimal Light](https://github.com/yaoyao-liu/minimal-light) theme.

## Project Structure

```
.
├── _config.yml                       # Site settings (name, affiliation, social links, etc.)
├── index.md                          # Main page content (About Me, News, Education, etc.)
├── _data/
│   ├── cv_info.yml                   # Personal info for CV (name, email, website)
│   ├── education.yml                 # Education entries with supervisors
│   ├── research_experience.yml       # Research experience with mentors and topics
│   ├── publications.yml              # Publications (peer-reviewed, preprints, patents)
│   ├── awards.yml                    # Awards and scholarships
│   ├── languages.yml                 # Language proficiencies
│   ├── skills.yml                    # Programming skills
│   ├── news.yml                      # News items
│   └── services.yml                  # Academic services (reviewing, etc.)
├── _includes/
│   ├── publications.html             # Publication template
│   ├── awards.html                   # Awards template
│   ├── news.html                     # News template
│   └── services.html                 # Services template
├── _layouts/
│   └── homepage.html                 # HTML layout template
├── _sass/
│   └── minimal-light.scss            # Stylesheet (SCSS)
├── assets/
│   ├── css/
│   ├── img/
│   ├── files/
│   │   └── CV.pdf                    # Auto-generated CV (do not edit manually)
│   └── js/
├── scripts/
│   └── generate_cv.py                # Generates cv/hikaru_asano_cv.tex from _data/
├── cv/
│   └── hikaru_asano_cv.tex           # Generated LaTeX source (do not edit manually)
├── Gemfile                           # Ruby dependencies
└── CNAME                             # Custom domain configuration
```

## CV Generation

The CV is generated locally from the `_data/` YAML files. Requires [PyYAML](https://pypi.org/project/PyYAML/) and a LaTeX distribution.

```bash
# First time only
pip install pyyaml

# Generate LaTeX, compile PDF, and place it in assets/files/CV.pdf
python scripts/generate_cv.py
```

## How to Edit

### Adding a publication

Add an entry to `_data/publications.yml`:

```yaml
peer_reviewed:
  - authors: "<strong>Hikaru Asano</strong>, Co-Author Name"
    title: "Paper Title"
    venue: "ICML"
    venue_full: "International Conference on Machine Learning"
    year: 2026
    note: "oral, acceptance rate 26%"   # or "poster", "long paper"
    arxiv: "https://arxiv.org/abs/xxxx.xxxxx"
    github: "https://github.com/..."
    project: "https://project-page.example.com"
```

### Adding a research experience

Add an entry to `_data/research_experience.yml`:

```yaml
- organization: "Organization Name"
  location: "City, Country"
  role: "Research Intern"
  start: "Apr 2026"
  end: "Present"
  mentors:
    - "Mentor Name"
  topic: "Research topic description"
```

### Adding an education entry

Add an entry to `_data/education.yml`:

```yaml
- institution: "University Name"
  degree: "Degree Title"
  department: "Department Name"
  start: "Apr 2019"
  end: "Mar 2022"
  supervisor: "Supervisor Name"
```

### Adding an award

Add an entry to `_data/awards.yml`:

```yaml
scholarships:
  - title: "Scholarship Name"
    description: "Details, amount, year."

academic_awards:
  - title: "Award Name"
    description: "Organization, year."
```

### Editing profile and news

Edit `index.md` or `_data/news.yml` directly.

### Changing site settings

Edit `_config.yml` (name, affiliation, social links, avatar path, etc.).

## Local Development

### Prerequisites

- [Ruby](https://www.ruby-lang.org/en/) (2.7+)
- [Bundler](https://bundler.io/)

On macOS:

```bash
brew install ruby
gem install bundler
```

### Setup & Run

```bash
# Install dependencies
bundle install

# Start local server
bundle exec jekyll serve
```

Open http://localhost:4000 in your browser to preview.
Files are automatically rebuilt on save.

### Troubleshooting

If `bundle install` fails:

```bash
rm Gemfile.lock
bundle install
```

## License

[Creative Commons Zero v1.0 Universal](LICENSE)

Based on [Minimal Light](https://github.com/yaoyao-liu/minimal-light) theme.
