# Python Crash Course — Non-CS Graduate Researchers

A build kit for a 3-session Python crash course for MSc/PhD researchers with
**zero prior programming**, in Biochemistry, Bioinformatics, Agriculture, and
Pharmacy. The goal is **code literacy, not code authoring**: run it, read it,
change one thing safely, spot a wrong answer, and get unstuck with AI help.

**Read [`docs/course-design.md`](docs/course-design.md) before building or
changing any teaching material.** It is the reasoning behind every decision.
[`CLAUDE.md`](CLAUDE.md) is the short operating brief; [`BUILD_PLAN.md`](BUILD_PLAN.md)
is the ordered task list.

## Layout

```
docs/course-design.md   full pedagogical brief (read first)
data/                   demo-data generator + generated session data
notebooks/              NN_live.ipynb (typed in class) + NN_complete.ipynb
homework/               homework specs and solution notebooks
handouts/               error cheatsheet, AI-prompting guide, SLURM template
setup/                  Miniforge / WSL2 / install-verification guides
```

## Session 1 quick start

Session 1 runs in **Google Colab** — no install. Notebooks fetch the demo data
from a raw GitHub URL, so students only open a link. See `data/session1/` for
the generated files and `notebooks/01_complete.ipynb` for the taught material.

Regenerate the demo data (reproducible, seeded):

```bash
python3 data/generate_demo_data.py
```
