# Hikaru Asano - Personal Academic Website

A personal academic website built with Jekyll and GitHub Pages, using the [Minimal Light](https://github.com/yaoyao-liu/minimal-light) theme.

## Project Structure

```
.
├── _config.yml                  # Site settings (name, affiliation, social links, etc.)
├── index.md                     # Main page content (About Me, News, Education, etc.)
├── _data/
│   ├── publications.yml         # Publication data (edit here to add papers)
│   └── awards.yml               # Awards data (edit here to add awards)
├── _includes/
│   ├── publications.html        # Publication template (usually no need to edit)
│   └── awards.html              # Awards template (usually no need to edit)
├── _layouts/
│   └── homepage.html            # HTML layout template
├── _sass/
│   └── minimal-light.scss       # Stylesheet (SCSS)
├── assets/
│   ├── css/
│   │   ├── style.scss           # CSS entry point
│   │   └── publications.css     # Publication list styles
│   ├── img/                     # Image files
│   ├── files/                   # PDFs and other files
│   └── js/                      # JavaScript
├── Gemfile                      # Ruby dependencies
└── CNAME                        # Custom domain configuration
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
    note: "oral"
    arxiv: "https://arxiv.org/abs/xxxx.xxxxx"
    github: "https://github.com/..."
    project: "https://project-page.example.com"
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

Edit `index.md` directly.

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
# Remove lock file and reinstall
rm Gemfile.lock
bundle install
```

## License

[Creative Commons Zero v1.0 Universal](LICENSE)

Based on [Minimal Light](https://github.com/yaoyao-liu/minimal-light) theme.
