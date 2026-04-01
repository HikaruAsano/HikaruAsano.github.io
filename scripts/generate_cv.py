#!/usr/bin/env python3
"""Generate CV LaTeX from Jekyll _data YAML files, then write to cv/hikaru_asano_cv.tex."""

import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not found. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data"
OUT = ROOT / "cv" / "hikaru_asano_cv.tex"


def load(name: str) -> dict | list:
    with open(DATA / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def html_to_tex(s: str) -> str:
    """Convert <strong> / <em> HTML tags to LaTeX equivalents."""
    if not s:
        return ""
    s = re.sub(r"<strong>(.*?)</strong>", r"\\textbf{\1}", s)
    s = re.sub(r"<b>(.*?)</b>", r"\\textbf{\1}", s)
    s = re.sub(r"<em>(.*?)</em>", r"\\textit{\1}", s)
    s = re.sub(r"<i>(.*?)</i>", r"\\textit{\1}", s)
    return s


def safe(s: str) -> str:
    """Escape bare & and % that are NOT already preceded by a backslash."""
    if not s:
        return ""
    s = s.replace("&", r"\&")
    s = re.sub(r"(?<!\\)%", r"\\%", s)
    return s


def format_note(note: str) -> str | None:
    """Turn note YAML string into a coloured LaTeX line.

    Examples:
      "poster, acceptance rate 24.5%"  ->  Poster presentation | Acceptance rate: 24.5%
      "oral, acceptance rate 23.3%"    ->  Oral presentation | Acceptance rate: 23.3%
      "long paper"                      ->  Long paper
    """
    if not note:
        return None
    parts = [p.strip() for p in note.split(",")]
    rendered = []
    for part in parts:
        low = part.lower()
        if low == "oral":
            rendered.append("Oral presentation")
        elif low == "poster":
            rendered.append("Poster presentation")
        elif low == "long paper":
            rendered.append("Long paper")
        elif "acceptance rate" in low:
            m = re.search(r"[\d.]+", part)
            if m:
                rendered.append(f"Acceptance rate: {m.group()}\\%")
        else:
            rendered.append(part.capitalize())
    if not rendered:
        return None
    inner = " $|$ ".join(rendered)
    return r"\textcolor{accentColor}{" + inner + "}"


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def build_education(data: list) -> str:
    lines = [r"\section{Education}", ""]
    for i, edu in enumerate(data):
        date_range = f"{edu['start']} -- {edu['end']}"
        lines.append(r"\begin{twocolentry}{" + date_range + "}")
        lines.append(f"    \\textbf{{{safe(edu['institution'])}}} \\newline")
        lines.append(f"    {safe(edu['degree'])} in {safe(edu['department'])}")
        lines.append(r"\end{twocolentry}")
        if edu.get("supervisor"):
            lines.append("")
            lines.append(r"\vspace{0.10 cm}")
            lines.append(r"\begin{onecolentry}")
            lines.append(r"    \begin{highlights}")
            lines.append(f"        \\item \\textit{{Supervisor:}} {safe(edu['supervisor'])}")
            lines.append(r"    \end{highlights}")
            lines.append(r"\end{onecolentry}")
        if i < len(data) - 1:
            lines.append("")
            lines.append(r"\vspace{0.3 cm}")
            lines.append("")
    return "\n".join(lines)


def build_research_experience(data: list) -> str:
    lines = [r"\section{Research Experience}", ""]
    for i, exp in enumerate(data):
        date_range = f"{exp['start']} -- {exp['end']}"
        lines.append(r"\begin{twocolentry}{" + date_range + "}")
        lines.append(f"    \\textbf{{{safe(exp['organization'])}}}, {safe(exp['location'])} \\newline")
        lines.append(f"    {safe(exp['role'])}")
        lines.append(r"\end{twocolentry}")

        bullets = []
        if exp.get("mentors"):
            mentor_str = ", ".join(safe(m) for m in exp["mentors"])
            bullets.append(f"        \\item \\textit{{Mentor:}} {mentor_str}")
        if exp.get("topic"):
            bullets.append(f"        \\item \\textit{{Research Topic:}} {safe(exp['topic'])}")

        if bullets:
            lines.append("")
            lines.append(r"\vspace{0.10 cm}")
            lines.append(r"\begin{onecolentry}")
            lines.append(r"    \begin{highlights}")
            lines.extend(bullets)
            lines.append(r"    \end{highlights}")
            lines.append(r"\end{onecolentry}")

        if i < len(data) - 1:
            lines.append("")
            lines.append(r"\vspace{0.2 cm}")
            lines.append("")
    return "\n".join(lines)


def build_publications(data: dict) -> str:
    lines = [r"\section{Publications}", ""]

    # --- Peer-reviewed ---
    lines.append(r"\subsection{International Conference (Peer-Reviewed)}")
    lines.append("")
    lines.append(r"    \begin{onecolentry}")
    lines.append(r"        \begin{highlights}")
    for pub in data.get("peer_reviewed", []):
        authors = html_to_tex(pub["authors"])
        title = safe(pub["title"])
        venue_full = safe(pub.get("venue_full", ""))
        venue = safe(pub.get("venue", ""))
        year = pub.get("year", "")
        note_tex = format_note(pub.get("note"))

        item = f"            \\item {authors} \\newline\n"
        item += f"            ``{title}'' \\newline\n"
        item += f"            \\textit{{{venue_full}}} \\textbf{{({venue})}}, {year}"
        if note_tex:
            item += f" \\newline\n            {note_tex}"
        lines.append(item)
        lines.append("")
    lines.append(r"        \end{highlights}")
    lines.append(r"    \end{onecolentry}")

    # --- Preprints ---
    lines.append("")
    lines.append(r"\subsection{Preprint}")
    lines.append("")
    lines.append(r"    \begin{onecolentry}")
    lines.append(r"        \begin{highlights}")
    for pub in data.get("preprints", []):
        authors = html_to_tex(pub["authors"])
        title = safe(pub["title"])
        year = pub.get("year", "")
        item = f"            \\item {authors} \\newline\n"
        item += f"            ``{title}'' \\newline\n"
        item += f"            \\textit{{arXiv preprint}}, {year}"
        lines.append(item)
        lines.append("")
    lines.append(r"        \end{highlights}")
    lines.append(r"    \end{onecolentry}")

    # --- Patents ---
    if data.get("patents"):
        lines.append("")
        lines.append(r"\subsection{Patent}")
        lines.append("")
        lines.append(r"    \begin{onecolentry}")
        lines.append(r"        \begin{highlights}")
        for pat in data["patents"]:
            authors = html_to_tex(pat["authors"])
            title = safe(pat["title"])
            pnum = safe(pat.get("patent_number", ""))
            item = f"            \\item {authors} \\newline\n"
            item += f"            ``{title}'' \\newline\n"
            item += f"            \\textit{{{pnum}}}"
            lines.append(item)
            lines.append("")
        lines.append(r"        \end{highlights}")
        lines.append(r"    \end{onecolentry}")

    return "\n".join(lines)


def build_awards(data: dict) -> str:
    lines = [r"\section{Awards and Honors}", ""]

    lines.append(r"\subsection{Scholarships and Grants}")
    lines.append(r"    \begin{onecolentry}")
    lines.append(r"        \begin{highlights}")
    for award in data.get("scholarships", []):
        lines.append(f"            \\item \\textbf{{{safe(award['title'])}}} \\newline")
        lines.append(f"            {safe(award['description'])}")
        lines.append("")
    lines.append(r"        \end{highlights}")
    lines.append(r"    \end{onecolentry}")

    lines.append("")
    lines.append(r"\subsection{Academic Awards}")
    lines.append(r"    \begin{onecolentry}")
    lines.append(r"        \begin{highlights}")
    for award in data.get("academic_awards", []):
        lines.append(f"            \\item \\textbf{{{safe(award['title'])}}} \\newline")
        lines.append(f"            {safe(award['description'])}")
        lines.append("")
    lines.append(r"        \end{highlights}")
    lines.append(r"    \end{onecolentry}")

    return "\n".join(lines)


def build_languages(data: list) -> str:
    lines = [r"\section{Languages}"]
    lines.append(r"    \begin{onecolentry}")
    lines.append(r"        \begin{highlights}")
    for lang in data:
        lines.append(f"            \\item \\textbf{{{safe(lang['language'])}:}} {safe(lang['level'])}")
    lines.append(r"        \end{highlights}")
    lines.append(r"    \end{onecolentry}")
    return "\n".join(lines)


def build_skills(data: list) -> str:
    lines = [r"\section{Programming Skills}"]
    lines.append(r"    \begin{onecolentry}")
    lines.append(r"        \begin{highlights}")
    for skill in data:
        lines.append(
            f"            \\item \\textbf{{{safe(skill['language'])}:}} {safe(skill['frameworks'])}"
        )
    lines.append(r"        \end{highlights}")
    lines.append(r"    \end{onecolentry}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Preamble (static)
# ---------------------------------------------------------------------------

PREAMBLE = r"""\documentclass[10pt, letterpaper]{article}

% Packages:
\usepackage[
    ignoreheadfoot,
    top=2 cm,
    bottom=2 cm,
    left=2 cm,
    right=2 cm,
    footskip=1.0 cm,
]{geometry}
\usepackage{titlesec}
\usepackage{tabularx}
\usepackage{array}
\usepackage[dvipsnames]{xcolor}
\definecolor{primaryColor}{RGB}{0, 79, 144}
\definecolor{accentColor}{RGB}{0, 102, 179}
\usepackage{enumitem}
\usepackage{fontawesome5}
\usepackage{amsmath}
\usepackage[
    pdftitle={Hikaru Asano's CV},
    pdfauthor={Hikaru Asano},
    pdfcreator={LaTeX},
    colorlinks=true,
    urlcolor=primaryColor
]{hyperref}
\usepackage[pscoord]{eso-pic}
\usepackage{calc}
\usepackage{bookmark}
\usepackage{lastpage}
\usepackage{changepage}
\usepackage{paracol}
\usepackage{ifthen}
\usepackage{needspace}
\usepackage{iftex}

\ifPDFTeX
    \input{glyphtounicode}
    \pdfgentounicode=1
    \usepackage[T1]{fontenc}
    \usepackage[utf8]{inputenc}
    \usepackage{lmodern}
\fi

\usepackage{charter}

\raggedright
\AtBeginEnvironment{adjustwidth}{\partopsep0pt}
\pagestyle{empty}
\setcounter{secnumdepth}{0}
\setlength{\parindent}{0pt}
\setlength{\topskip}{0pt}
\setlength{\columnsep}{0.15cm}
\pagenumbering{gobble}

\titleformat{\section}{\needspace{4\baselineskip}\bfseries\Large\color{primaryColor}}{}{0pt}{}[\vspace{1pt}\titlerule]

\titlespacing{\section}{-1pt}{0.3 cm}{0.2 cm}

\titleformat{\subsection}{\bfseries\large\color{accentColor}}{}{0pt}{}
\titlespacing{\subsection}{0pt}{0.3 cm}{0.15 cm}

\renewcommand\labelitemi{$\vcenter{\hbox{\small$\bullet$}}$}
\newenvironment{highlights}{
    \begin{itemize}[
        topsep=0.10 cm,
        parsep=0.10 cm,
        partopsep=0pt,
        itemsep=0pt,
        leftmargin=0 cm + 10pt
    ]
}{
    \end{itemize}
}

\newenvironment{highlightsforbulletentries}{
    \begin{itemize}[
        topsep=0.10 cm,
        parsep=0.10 cm,
        partopsep=0pt,
        itemsep=0pt,
        leftmargin=10pt
    ]
}{
    \end{itemize}
}

\newenvironment{onecolentry}{
    \begin{adjustwidth}{0 cm + 0.00001 cm}{0 cm + 0.00001 cm}
}{
    \end{adjustwidth}
}

\newenvironment{twocolentry}[2][]{
    \onecolentry
    \def\secondColumn{#2}
    \setcolumnwidth{\fill, 4.5 cm}
    \begin{paracol}{2}
}{
    \switchcolumn \raggedleft \secondColumn
    \end{paracol}
    \endonecolentry
}

\newenvironment{threecolentry}[3][]{
    \onecolentry
    \def\thirdColumn{#3}
    \setcolumnwidth{, \fill, 4.5 cm}
    \begin{paracol}{3}
    {\raggedright #2} \switchcolumn
}{
    \switchcolumn \raggedleft \thirdColumn
    \end{paracol}
    \endonecolentry
}

\newenvironment{header}{
    \setlength{\topsep}{0pt}\par\kern\topsep\centering\linespread{1.5}
}{
    \par\kern\topsep
}

\let\hrefWithoutArrow\href
"""


def build_last_updated() -> str:
    month = datetime.now().strftime("%B %Y")
    return (
        r"\newcommand{\placelastupdatedtext}{"
        + "\n"
        + r"  \AddToShipoutPictureFG*{"
        + "\n"
        + r"    \put("
        + "\n"
        + r"        \LenToUnit{\paperwidth-2 cm-0 cm+0.05cm},"
        + "\n"
        + r"        \LenToUnit{\paperheight-1.0 cm}"
        + "\n"
        + r"    ){\vtop{{\null}\makebox[0pt][c]{"
        + "\n"
        + r"        \small\color{gray}\textit{Last updated in "
        + month
        + r"}\hspace{\widthof{Last updated in "
        + month
        + r"}}"
        + "\n"
        + r"    }}}%"
        + "\n"
        + r"  }%"
        + "\n"
        + r"}%"
    )


def build_header(info: dict) -> str:
    name = safe(info["name"])
    email = safe(info["email"])
    website = safe(info["website"])
    website_url = info["website_url"]
    return rf"""
\begin{{document}}
    \newcommand{{\AND}}{{\unskip
        \cleaders\copy\ANDbox\hskip\wd\ANDbox
        \ignorespaces
    }}
    \newsavebox\ANDbox
    \sbox\ANDbox{{$|$}}

    \begin{{header}}
        \fontsize{{30 pt}}{{30 pt}}\selectfont\bfseries\color{{primaryColor}} {name}

        \vspace{{8 pt}}

        \normalsize\color{{black}}
        \mbox{{{{\faIcon{{envelope}}}} \hrefWithoutArrow{{mailto:{email}}}{{{email}}}}}%
        \kern 5.0 pt%
        \AND%
        \kern 5.0 pt%
        \mbox{{{{\faIcon{{globe}}}} \hrefWithoutArrow{{{website_url}}}{{{website}}}}}%
    \end{{header}}

    \vspace{{5 pt - 0.3 cm}}
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    info = load("cv_info.yml")
    education = load("education.yml")
    research = load("research_experience.yml")
    publications = load("publications.yml")
    awards = load("awards.yml")
    languages = load("languages.yml")
    skills = load("skills.yml")

    parts = [
        PREAMBLE,
        build_last_updated(),
        build_header(info),
        "    " + build_education(education).replace("\n", "\n    "),
        "",
        "    " + build_research_experience(research).replace("\n", "\n    "),
        "",
        "    " + build_publications(publications).replace("\n", "\n    "),
        "",
        "    " + build_awards(awards).replace("\n", "\n    "),
        "",
        "    " + build_languages(languages).replace("\n", "\n    "),
        "",
        "    " + build_skills(skills).replace("\n", "\n    "),
        "",
        r"\end{document}",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Generated: {OUT}")


if __name__ == "__main__":
    main()
