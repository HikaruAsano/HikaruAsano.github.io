{%- comment -%}
  Shared body of the English (/) and Japanese (/ja/) pages.
  Edit the content here. Only the Education section differs by language.
{%- endcomment -%}

## About Me {#about-me}

I am a 3rd-year PhD student at the University of Tokyo. My research explores multi-agent reinforcement learning, computational social science, and language models for understanding human behavior.

## Research Interests {#research-interests}

<ul class="research-list">
  <li><strong>Multi-agent Reinforcement Learning</strong> — Cooperation in a decentralized manner.</li>
  <li><strong>Computational Social Science</strong> — Applying machine learning to social science.</li>
  <li><strong>LLM for Behavior Understanding</strong> — Replicating human behavior and utilizing common sense reasoning.</li>
</ul>

{% include news.html %}

{% include publications.html %}

## Education {#education}
{% if page.lang == "ja" %}
- 東京大学大学院 総合文化研究科 博士課程（2024.4–現在）
- 東京大学大学院 学際情報学府 修士課程（2022.4–2024.3）
- 東京大学 工学部 システム創成学科（2019.4–2022.3）
{: .education-ja lang="ja"}
{% else %}
- D.Sc in Graduate School of Arts and Sciences, The University of Tokyo (2024.4-present)
- M.S in Graduate School of Interdisciplinary Information Studies, The University of Tokyo (2022.4-2024.3)
- B.E in Systems Innovation, Faculty of Engineering, The University of Tokyo (2019.4-2022.3)
{% endif %}

## Job Experiences {#job-experiences}
- Sakana AI, Research Intern (2026.4-present)
- OMRON SINIC X Corporation, Research Intern (2025.12-2026.3)
- CyberAgent AI Lab, Part-time Researcher (2023.10-2025.10)
- OMRON SINIC X Corporation, Research Intern (2022.3-2023.8)
- OMRON SINIC X Corporation, Research Intern (2020.8-2020.9)

{% include awards.html %}

{% include services.html %}
