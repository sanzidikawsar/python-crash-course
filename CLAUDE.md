# Python Crash Course — Non-CS Graduate Researchers

Repo for building teaching notebooks, demo data, homework, and handouts for a
3-session Python crash course. **Read `docs/course-design.md` before building any
teaching artifact.** This file is the short version; that file is the reasoning.

## Who the learners are

MSc/PhD students at a Bangladeshi-background graduate program, in Biochemistry,
Bioinformatics, Agriculture, and Pharmacy. They did bachelor's degrees where
non-CS departments teach no programming at all. **Zero prior coding.** All are
fluent in Excel. All are strong researchers in their own fields. Mostly Windows
laptops, brought to an in-person classroom.

Two working groups:
- **MD track** — molecular dynamics (biochemistry / bioinformatics)
- **Genomics track** — gene sequence analysis and prediction for plants (agriculture)

## The one design principle

We are teaching **code literacy, not code authoring.** Success is: they can run
it, read it, change one thing safely, tell when the output is wrong, and get
unstuck with AI help. Success is *not* writing programs from a blank file.

Every artifact in this repo is judged against: *does this reduce fear and
increase the odds they use Python on Monday?*

## Hard budget

3 sessions × 90 minutes, in-person. That is all the contact time there is.
Realistically ~60 minutes of content per session and ~30 minutes of students
struggling. Do not design past that. Homework carries the real learning load.

## Cut list — never introduce these in session 1 or 2

OOP/classes, user-defined functions (recognizing them is fine, writing them is
not), list/dict comprehensions, `lambda`, decorators, `try`/`except`, `git`,
virtual-environment theory, `apply`/`map`, method chains longer than two calls,
type hints, `if __name__ == "__main__"`, f-string format specifiers, matplotlib
customization beyond labels and a title.

If a task seems to need one of these, restructure the task instead.

## Notebook authoring rules

These are non-negotiable and are the most common thing to get wrong.

1. **Two variants per session.** `NN_live.ipynb` is the skeleton the instructor
   types into during class (key lines replaced with `# TYPE THIS TOGETHER`).
   `NN_complete.ipynb` is the full version released to students afterwards.
   They must be otherwise identical in structure.
2. **A markdown cell before every code cell.** Two to four sentences, plain
   English. Define any term the first time it appears. Explanation comes
   *before* the code, because students read top-down while typing.
3. **Code cells ≤ 8 lines** in session 1, ≤ 15 in session 2. No cell should
   require scrolling on a 1366×768 laptop.
4. **Every code cell produces visible output.** No silent cells. Print
   something, show a dataframe, draw a plot. A cell that runs and shows nothing
   teaches a beginner nothing.
5. **Domain-language variable names.** `absorbance`, `sample_id`, `gc_content`.
   Never `x`, `df2`, `temp`, `data1`.
6. **Explicit over clever.** Intermediate variables and plain `for` loops beat
   one-liners. `print()` liberally.
7. **At least two deliberate-error cells per notebook**, each under a markdown
   heading `### Break it on purpose`. Show the broken cell, show the full
   traceback, then a markdown cell reading the traceback bottom-up, then the
   fix. This is the core fear-removal mechanic — treat it as content, not filler.
8. **Pacing markers.** In `_live.ipynb`, put an HTML comment above each section:
   `<!-- ~8 min -->`. Section timings must sum to the session budget.
9. **Open and close every notebook** with a plain-language "by the end you can
   …" list and a "what to try in the homework" list.
10. **Data loads from a URL constant** defined once at the top for session 1.
    Local file paths are introduced deliberately in session 2, as a topic.
11. **Colab notebooks get one core install cell at the top** (pinned versions,
    Colab-only comment). A *second* install cell may appear once at the start of
    a later section that needs heavier domain libraries (e.g. Biopython +
    MDAnalysis in session 1 Part 4), so class start-up stays fast. Local
    notebooks get none.

## Definition of done for a notebook

A notebook is not done until it has been **executed end to end from a clean
kernel** and every cell produced its expected output:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/<name>.ipynb
```

A notebook that fails live in front of twenty beginners is worse than no
notebook. Never mark one complete without running it.

## Repo map

```
CLAUDE.md                  this file
BUILD_PLAN.md              ordered build tasks with ready-to-paste prompts
docs/course-design.md      full pedagogical brief — read before authoring
data/generate_demo_data.py reproducible demo data generator (seeded)
data/generate_genomics_data.py synthetic plant-gene FASTA generator (seeded)
data/session1/             12 messy monthly CSVs, produced by the generator
data/genomics/             plant_genes.fasta for the session-1 Part-4 taste
data/session2/md/          MD track sample inputs
data/session2/genomics/    genomics track sample inputs
notebooks/                 NN_live.ipynb and NN_complete.ipynb per session
homework/                  hw0_setup, hw1, hw2_md, hw2_genomics, capstone
handouts/                  error cheatsheet, AI prompting guide, SLURM template
setup/                     WSL2, Miniforge, and install-verification guides
```

## DATA_BASE_URL

Session-1 demo data is hosted (public) for raw fetch in Colab:

```
https://raw.githubusercontent.com/sanzidikawsar/python-crash-course/main/data/session1
```

Notebooks define this once at the top and build file URLs from it, e.g.
`f"{DATA_BASE_URL}/results_2025_{month:02d}.csv"`. Regenerate the files with
`python3 data/generate_demo_data.py` and `git push`; the URL does not change.

## Environment decisions (rationale in docs/course-design.md)

- **Session 1: Google Colab.** Zero install, identical environment on every
  laptop, data fetched by URL. Fundamentals-first (Python basics → one CSV →
  all files → a run-only taste of Biopython + MDAnalysis in Part 4). The MD
  taste uses the bundled `PSF`/`DCD` test files — verified working (3341 atoms,
  98 frames). Session 1 is built from one source: `notebooks/build_session1.py`
  emits both `01_live.ipynb` and `01_complete.ipynb`.
- **Between sessions: local Miniforge + Jupyter**, installed as homework, not
  in class. Prefer Miniforge over full Anaconda (smaller, conda-forge default,
  avoids institutional licensing questions).
- **Session 2: local Jupyter**, students' own files, real paths.
- **Session 3: WSL2 shell → SSH → SLURM.** WSL2, *not* a dual-boot or OS
  migration. The terminal appears only when submitting a real job requires it.

## Tone for all student-facing prose

Write for a smart adult who has never programmed and is slightly embarrassed
about it. No "simply", no "just", no "obviously". Never imply a step is easy.
Name the thing that is about to go wrong before it goes wrong.

## Open items

- Cluster specifics for session 3 (hostname, scheduler partitions, module
  names, account codes) are **not yet known**. Leave clearly marked
  `TODO(cluster)` placeholders rather than inventing plausible values.
