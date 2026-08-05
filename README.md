<img src="assets/hero.png" width="100%" alt="Hritvik Gupta — AI Engineer @ Penn Medicine. I build agents that do real work, not demos." />

<p align="center">
  <a href="https://hritvikgupta.github.io/hritvik-gupta/"><img src="https://img.shields.io/badge/Portfolio-hritvikgupta.github.io-FF6B4A?style=for-the-badge&labelColor=0A0B0D&logo=googlechrome&logoColor=FF6B4A" alt="Portfolio" /></a>
  <a href="https://www.linkedin.com/in/hritvik-gupta-link/"><img src="https://img.shields.io/badge/LinkedIn-hritvik--gupta-0A66C2?style=for-the-badge&labelColor=0A0B0D&logo=linkedin&logoColor=0A66C2" alt="LinkedIn" /></a>
  <a href="mailto:hritvik2920@gmail.com"><img src="https://img.shields.io/badge/Email-hritvik2920@gmail.com-C5CAD3?style=for-the-badge&labelColor=0A0B0D&logo=gmail&logoColor=C5CAD3" alt="Email" /></a>
</p>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=hritvikgupta&label=Profile%20views&color=FF6B4A&style=flat-square" alt="Profile views" />
  <a href="https://github.com/hritvikgupta?tab=followers"><img src="https://img.shields.io/github/followers/hritvikgupta?label=Followers&style=flat-square&color=FF6B4A&labelColor=0A0B0D" alt="Followers" /></a>
  <img src="https://img.shields.io/badge/Focus-Autonomous%20Agents-FF6B4A?style=flat-square&labelColor=0A0B0D" alt="Focus" />
  <img src="https://img.shields.io/badge/Open%20to-Collaborations-C5CAD3?style=flat-square&labelColor=0A0B0D" alt="Open to collaborations" />
</p>

---

## 👋 About me

I'm **Hritvik** — an AI engineer at **Penn Medicine (Verma Lab)**, where I ship voice and chat systems that real patients actually use. Outside of work I build **autonomous agents**: things that read your code, operate your cloud, read the literature, and hand back a result you can verify.

My bet is simple: the interesting part of an agent isn't the model, it's the loop around it — memory, tools, and evals. Most agents feel dumb because they forget, not because they can't reason.

```yaml
name:      Hritvik Gupta
role:      AI Engineer @ Penn Medicine · Verma Lab
education: MS Computer Engineering, UC Riverside
thesis:    "agents should do real work — not demos"
building:  [autonomous agents, LLM infrastructure, agent evals & benchmarks]
languages: [Python, TypeScript, Swift, SQL, C++]
now:       multi-agent orchestration · longitudinal memory · self-hosted agent infra
ask-me-about: [RAG at scale, agent evals, multilingual speech pipelines, genomics ML]
```

<table>
<tr>
<td width="25%" align="center"><b>100K+</b><br /><sub>patients served by the voice&nbsp;&amp;&nbsp;chat system I built</sub></td>
<td width="25%" align="center"><b>27M</b><br /><sub>SNPs processed on Argonne's Aurora supercomputer</sub></td>
<td width="25%" align="center"><b>10M+</b><br /><sub>multilingual research documents in NLP pipelines</sub></td>
<td width="25%" align="center"><b>4</b><br /><sub>peer-reviewed publications</sub></td>
</tr>
</table>

---

## 🚀 What I'm building

<div>
<a href="https://github.com/hritvikgupta/nimbus"><img src="assets/card-nimbus.svg" width="48.6%" alt="nimbus — an AI cloud control plane. One agent that reads your code and acts on real AWS and GCP credentials to fix your infra." /></a>
<a href="https://github.com/hritvikgupta/reagent"><img src="assets/card-reagent.svg" width="48.6%" alt="reagent — autonomous research agents that read the literature, weigh the evidence, and return a cited, reproducible answer." /></a>
<a href="https://github.com/hritvikgupta/Archimyst-Terminal"><img src="assets/card-archimyst.svg" width="48.6%" alt="Archimyst Terminal — a council of agents in your terminal. Symbol indexing and coordinated edits across million-line codebases." /></a>
<a href="https://github.com/hritvikgupta/trytine"><img src="assets/card-tine.svg" width="48.6%" alt="Tine — a second cursor that watches your screen, suggests help, and on your say-so takes over and finishes the task." /></a>
</div>

<details>
<summary><b>More projects →</b></summary>

<br />

| Project | What it is |
|---|---|
| [**chytra**](https://github.com/hritvikgupta/chytra) | AI-powered research and creative canvas — Figma-style design surface wired to 200+ models, with a graph-memory architecture that connects ideas, documents, and findings |
| [**worklone**](https://github.com/hritvikgupta/worklone) | Next-generation AI spreadsheet and agentic framework — natural-language data workflows, a built-in Data Scientist agent, and multi-agent request routing |
| [**probeqa**](https://github.com/hritvikgupta/probeqa) | Agentic QA — a real testing agent that drives the app instead of asserting on mocks |
| [**voiceai**](https://github.com/hritvikgupta/voiceai) | Real-time voice agent stack: streaming STT → LLM brain → TTS |
| [**docuwriters**](https://github.com/hritvikgupta/docuwriters) | Documentation that writes and maintains itself from the codebase |

</details>

---

## 🧠 How I build agents

```mermaid
flowchart LR
    U(["User · event · schedule"]) --> P
    P["Perception<br/>speech · code · logs · papers"] --> R
    R{{"Reasoning<br/>plan · route · decompose"}} -->|delegate| S["Specialist sub-agents<br/>research · rank · reproduce"]
    R -->|tools| A["Action<br/>PRs · queries · deploys"]
    S --> A
    A --> V["Verification<br/>evals · deterministic checks"]
    V -->|regress| R
    V -->|ship| O(["Real-world side effect"])
    M[("Longitudinal<br/>memory")] <--> R

    classDef n fill:#0f1115,stroke:#30363d,color:#e6edf3
    classDef h fill:#1e1113,stroke:#FF6B4A,color:#f0f3f6
    class U,P,S,A,V,O n
    class R,M h
```

**Tools over talk.** An agent's output is a side effect in the real world — a merged PR, a rolled-back deploy, an escalation — not a paragraph that reads well.

**Memory is the hard part.** Continuity across sessions beats brilliance inside one. Every agent I ship gets a working-memory document it maintains itself.

**Evals or it didn't happen.** A benchmark harness with deterministic checks goes in *before* the agent meets a user, not after it embarrasses one.

**Self-hostable by default.** Your data, your infrastructure, your keys. Anything holding production credentials should run where you can watch it.

---

## 💼 Experience

```mermaid
gantt
    title       Career timeline
    dateFormat  YYYY-MM
    axisFormat  %Y
    todayMarker off

    section Industry
    Data Analyst · Cognizant               :c1, 2021-08, 2022-08
    AI Engineer · Penn Medicine            :active, p1, 2024-07, 2026-09

    section Research
    Graduate Researcher NLP · UC Riverside :r1, 2022-10, 2023-12

    section Education
    MS Computer Engineering · UCR          :e1, 2022-09, 2023-12
```

<details open>
<summary><b>AI Engineer</b> · Penn Medicine · <i>Jul 2024 – Present</i></summary>

- Built an **AI voice & chat system for Perception Care** used by **100K+ West Coast patients** — a multilingual `speech → RAG → LLM` pipeline on LlamaIndex, FAISS, LangChain, FastAPI, and Docker.
- Engineered data generation for speech and language model retrieval, vector search, and prompt-routing workflows — **~28% lower response latency**, **+22% clinical-text retrieval accuracy**.
- Enhanced the **PLATLAS genomics platform** with ML-based variant ranking and phenotype-similarity scoring; ran **27M-SNP Nextflow pipelines on Argonne's Aurora supercomputer**.
- Developed **PySpark + Delta Lake** pipelines standardizing **30+ clinical datasets into OMOP**, enabling real-time cohort building and disease-trend dashboards.

</details>

<details>
<summary><b>Graduate Researcher (NLP)</b> · University of California, Riverside · <i>Oct 2022 – Dec 2023</i></summary>

- Built large-scale NLP pipelines (Python, Spark, SQL) over **10M+ multilingual research documents**, improving tokenization and embedding generation speed by **~40%**.
- Optimized RAG systems with LlamaIndex + LangChain, raising scientific-text retrieval accuracy by **22%**.

</details>

<details>
<summary><b>Data Analyst</b> · Cognizant · <i>Aug 2021 – Aug 2022</i></summary>

- Built Python + SQL ETL pipelines over **20K+ HR, payroll, and marketing records across 50 datasets**, improving data accuracy by **~35%**.
- Developed Scikit-learn + SAS predictive models for attrition and hiring demand, improving workforce planning for **5,000+ employees**.

</details>

---

## 🛠️ Tech stack

<table>
<tr><td><b>Languages</b></td><td>
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" />
<img src="https://img.shields.io/badge/Swift-F05138?style=flat-square&logo=swift&logoColor=white" />
<img src="https://img.shields.io/badge/C++-00599C?style=flat-square&logo=cplusplus&logoColor=white" />
<img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white" />
<img src="https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white" />
</td></tr>
<tr><td><b>AI &amp; agents</b></td><td>
<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" />
<img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white" />
<img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" />
<img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square&logo=langgraph&logoColor=white" />
<img src="https://img.shields.io/badge/LlamaIndex-0A0B0D?style=flat-square&logo=llama&logoColor=white" />
<img src="https://img.shields.io/badge/MCP-000000?style=flat-square&logo=modelcontextprotocol&logoColor=white" />
<img src="https://img.shields.io/badge/RAG-FF6B4A?style=flat-square&logoColor=white" />
<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" />
</td></tr>
<tr><td><b>Backend</b></td><td>
<img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white" />
<img src="https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB" />
<img src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" />
<img src="https://img.shields.io/badge/GraphQL-E10098?style=flat-square&logo=graphql&logoColor=white" />
</td></tr>
<tr><td><b>Data</b></td><td>
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" />
<img src="https://img.shields.io/badge/pgvector-4169E1?style=flat-square&logo=postgresql&logoColor=white" />
<img src="https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white" />
<img src="https://img.shields.io/badge/Neo4j-4581C3?style=flat-square&logo=neo4j&logoColor=white" />
<img src="https://img.shields.io/badge/Spark-E25A1C?style=flat-square&logo=apachespark&logoColor=white" />
<img src="https://img.shields.io/badge/Delta%20Lake-00ADD4?style=flat-square&logo=delta&logoColor=white" />
<img src="https://img.shields.io/badge/Databricks-FF3621?style=flat-square&logo=databricks&logoColor=white" />
</td></tr>
<tr><td><b>Cloud &amp; infra</b></td><td>
<img src="https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white" />
<img src="https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=googlecloud&logoColor=white" />
<img src="https://img.shields.io/badge/Azure-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white" />
<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" />
<img src="https://img.shields.io/badge/Nextflow-24B064?style=flat-square&logo=nextflow&logoColor=white" />
</td></tr>
</table>

---

## 📊 GitHub statistics

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=hritvikgupta&show_icons=true&include_all_commits=true&count_private=true&hide_border=false&border_color=1E222A&bg_color=0A0B0D&title_color=FF6B4A&text_color=C5CAD3&icon_color=FF6B4A&border_radius=12" height="180" alt="Hritvik's GitHub stats" />
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=hritvikgupta&layout=compact&langs_count=8&hide_border=false&border_color=1E222A&bg_color=0A0B0D&title_color=FF6B4A&text_color=C5CAD3&border_radius=12" height="180" alt="Top languages" />
</p>

<p align="center">
  <img src="https://streak-stats.demolab.com?user=hritvikgupta&hide_border=false&border=1E222A&background=0A0B0D&stroke=1E222A&ring=FF6B4A&fire=FF6B4A&currStreakNum=F4F5F7&currStreakLabel=FF6B4A&sideNums=C5CAD3&sideLabels=C5CAD3&dates=5A616D&border_radius=12" height="180" alt="GitHub streak" />
</p>

<p align="center">
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=hritvikgupta&theme=github_dark&utcOffset=-8" height="200" alt="Productive time" />
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=hritvikgupta&theme=github_dark" height="200" alt="Repos per language" />
</p>

### 🏆 Trophies

<p align="center">
  <img src="https://github-profile-trophy.vercel.app/?username=hritvikgupta&theme=darkhub&no-frame=true&no-bg=true&column=7&margin-w=6&margin-h=6" alt="Trophies" />
</p>

### 📈 Contribution activity

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=hritvikgupta&bg_color=0A0B0D&color=C5CAD3&line=FF6B4A&point=F4F5F7&area=true&area_color=FF6B4A&hide_border=false&border_color=1E222A&radius=12" width="100%" alt="Contribution activity graph" />
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/hritvikgupta/hritvikgupta/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/hritvikgupta/hritvikgupta/output/github-snake.svg" />
  <img src="https://raw.githubusercontent.com/hritvikgupta/hritvikgupta/output/github-snake.svg" width="100%" alt="Contribution snake" />
</picture>

---

## 📄 Publications &amp; recognition

| Year | Work | Venue |
|:--|:--|:--|
| 2025 | Levin, M.G., *et al.* (incl. **Gupta, H.**) — *Genome-Wide Assessment of Pleiotropy Across >1000 Traits from Global Biobanks* | medRxiv |
| 2021 | **Gupta, H.** & Patel, M. — *Text Summarization: LSA Topic Modelling with BERT* | AI Smart Systems |
| 2021 | Gupta, S. & Kal, H. — *Microstate EEG Analysis via RNN* | i-PACT |
| 2020 | Patel, M. & **Gupta, H.** — *Extractive Text Summarization Using ELMo* | IEEE I-SMAC |

> 🏅 **Health-Tech Innovation Accelerator Award** — Penn Health-Tech, 2025
> *CIRCA: Voice-AI for general healthcare services to patients.*

---

## 🤝 Let's build something

I'm always up for a conversation about agents that have to work in the real world — production credentials, messy data, users who notice when it's wrong.

<p align="center">
  <a href="https://hritvikgupta.github.io/hritvik-gupta/"><img src="https://img.shields.io/badge/Portfolio-FF6B4A?style=for-the-badge&labelColor=0A0B0D&logo=googlechrome&logoColor=FF6B4A" alt="Portfolio" /></a>
  <a href="https://www.linkedin.com/in/hritvik-gupta-link/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&labelColor=0A0B0D&logo=linkedin&logoColor=0A66C2" alt="LinkedIn" /></a>
  <a href="mailto:hritvik2920@gmail.com"><img src="https://img.shields.io/badge/Email-C5CAD3?style=for-the-badge&labelColor=0A0B0D&logo=gmail&logoColor=C5CAD3" alt="Email" /></a>
  <a href="https://github.com/hritvikgupta?tab=repositories"><img src="https://img.shields.io/badge/Repositories-C5CAD3?style=for-the-badge&labelColor=0A0B0D&logo=github&logoColor=C5CAD3" alt="Repositories" /></a>
</p>

<p align="center"><sub><code>~/hritvik $ agents --status</code> → <b>shipping</b></sub></p>
