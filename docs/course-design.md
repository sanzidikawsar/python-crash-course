# Course Design Brief

The reasoning behind every decision in `CLAUDE.md`. Read this before authoring
any session material. When a design choice here conflicts with a general
"best practice" for teaching Python, this document wins — the constraints are
unusual and most intro-Python advice does not apply.

---

## 1. Learners

| | |
|---|---|
| Level | MSc and PhD, active researchers |
| Departments | Biochemistry, Bioinformatics, Agriculture, Pharmacy |
| Prior programming | None. Their bachelor's programs did not teach it. |
| Prior tooling | Excel, fluently. Not R, not SPSS, not a terminal. |
| Hardware | Own Windows laptops, brought to class |
| Setting | In-person classroom |
| Instructor time | 3 sessions × 90 min, no continuous teaching after |

Two research groups, and the split matters for session 2 onward:

- **MD track** — molecular dynamics simulations, biochemistry and
  bioinformatics. Simulation runs on HPC; the laptop is an analysis client.
  Python stack: MDAnalysis or MDTraj, NumPy, matplotlib.
- **Genomics track** — gene sequence analysis and trait prediction in plants,
  agriculture. Python stack: Biopython, pandas, scikit-learn.

**The instructor is not a domain expert in either.** This is a design input,
not a problem. See §7.

---

## 2. The design principle

With three hours of contact time and "reuse existing code with AI help" as the
stated goal, this is a **code literacy** course, not a programming course.

| Literacy (our target) | Authoring (not our target) |
|---|---|
| Run someone else's script | Write a program from a blank file |
| Read code and predict what it does | Design an algorithm |
| Change one parameter safely | Structure a codebase |
| Read a traceback and act on it | Handle errors gracefully |
| Recognize when output is wrong | Optimize |
| Get unstuck with an AI assistant | Work unassisted |

The bottleneck for a pharmacologist in 2026 is not writing a `for` loop. It is
environment friction, unreadable errors, and uncritical trust in generated
output. Aim the three hours at those.

---

## 3. What we cut, and why

Cutting is the hardest part of a 3-hour syllabus, and drift is the main failure
mode. The cut list in `CLAUDE.md` is binding. Rationale for the non-obvious ones:

- **User-defined functions.** They cost 20+ minutes to teach properly
  (scope, arguments, return) and buy nothing for someone reusing code.
  Students must *recognize* `def` in a script they've downloaded. That's it.
- **`try`/`except`.** Teaching beginners to suppress errors is actively
  harmful. They need to read errors, not hide them.
- **git.** A whole second tool with its own failure modes. A shared Drive
  folder does the job for three sessions.
- **Comprehensions.** They make code shorter and unreadable to a novice. The
  explicit loop is the teaching artifact.

---

## 4. Platform sequence and rationale

The platform changes across sessions on purpose. Each change is motivated.

**Session 1 — Google Colab.**
The enemy on day one is environment variance. Twenty Windows laptops produce
twenty different failure modes, and 40 minutes lost to installation kills the
session. Colab gives one shared link, an identical environment for everyone,
and Runtime → Restart as a universal undo. Since the instructor supplies the
demo data, hosting it at a raw URL removes the last friction point: no upload
step, no file paths, no `FileNotFoundError` on day one.

*Risk:* classroom Wi-Fi with 20 simultaneous Colab sessions. Test in the actual
room beforehand. Fallback: a zip of notebook + data, plus phone tethering.

**Between sessions — local Miniforge, as homework.**
Install failures then get debugged in the group chat over three days instead of
in 90 minutes of class time. Miniforge over full Anaconda: much smaller
download for weak laptops, conda-forge as the default channel, and it avoids
the institutional licensing question that caught several universities out —
worth confirming with campus IT either way. Conda rather than pip matters here
because bioconda is where BLAST, samtools, and similar binaries live, and pip
cannot supply them.

**Session 2 — local Jupyter, their own files.**
This is where the working directory, relative paths, and `read_csv("data/x.csv")`
belong — taught deliberately, once they have their own data and a reason to care.

**Session 3 — WSL2 shell, then SSH, then SLURM.**
The terminal is the most alienating possible surface for an Excel-fluent,
code-fearful audience: black screen, no undo, no visible data. Everything that
makes session 1 work (see the dataframe, see the plot) is a notebook
affordance. So the shell arrives only in session 3, when submitting a real
GROMACS job makes it obviously necessary.

**On Ubuntu: WSL2, not migration.** Dual-booting twenty random Windows laptops
means Secure Boot, BitLocker, OEM partitions, and Wi-Fi drivers — and every
failure gets blamed on the course. Several students almost certainly depend on
Windows-only instrument software. `wsl --install` gives a real Ubuntu shell,
the same conda, the same SSH, and the identical skillset needed for HPC, while
leaving Windows intact. Assign it before session 3, never as a prerequisite for
session 1. Most common blocker: virtualization disabled in BIOS — warn in advance.

---

## 5. Session 1 — "Make the computer do your boring work" (90 min)

Built bottom-up for a genuinely zero-programming group: the five Python
building blocks first, on everyday values, then their data, then their field's
tool. Concepts still appear only as the story needs them — no "data types" or
"control flow" taxonomy — but the sequence is **fundamentals-first, not
hook-first**.

**Why not open with the "wow" hook?** The original design opened with an opaque
six-line demo ("watch this replace 30 minutes of Excel"). That motivates
learners who can tolerate not-understanding; for a truly zero-experience group
it intimidates. The impressive combined result now lands at the *end of Part 3*
as the payoff they can actually build. (Instructor's call for this cohort; if a
future group is more confident, restore a 30-second run-only teaser on top.)

| Time | Part | Content |
|---|---|---|
| 0–15 | **Part 1 · Python basics** | `print`, variable, string ops (`.strip`/`.capitalize`), one `if`, list + `.append`, one `for` — all on everyday values (fruit, temperature, a name). First **break-it-on-purpose** here. |
| 15–40 | **Part 2 · Your first real file** | A taste of lab data (a list of readings, a messy label), then one CSV: `read_csv`, DataFrame, `.head/.shape/.dtypes/.describe`, select, filter, second **break-it**, the three one-line cleanings (reusing Part 1's string ops). |
| 40–65 | **Part 3 · All the files at once** | The 3-step loop build (3 files → month list → full combine), `groupby`, one line plot + save, one bar chart. The old "hook", now earned. |
| 65–85 | **Part 4 · A taste of your field's tool** | Same five-step skeleton, richer: Biopython (read FASTA, GC%, central dogma → protein, reverse complement, GC bar chart) and MDAnalysis (atoms/residues/frames, radius of gyration + plot, RMSD). Run-only; hands-on in session 2. |
| 85–90 | **Wrap up** | Recap + HW1 handed out. |

Concepts permitted: variable, string, string methods, number, list, `.append`,
`len`, `max`, one `if`, one `for`, DataFrame, column, filter, `groupby`, one
plot. Nothing else. String operations are taught in Part 1 specifically so the
Part 2 cleaning step reuses them.

---

## 6. Session 2 — "Read it, borrow it, adapt it" (90 min)

| Time | Block | Content |
|---|---|---|
| 0–15 | **Homework debrief** | Solve two errors students actually hit, live, from their own submissions. Highest-value 15 minutes in the course — do not skip for content. |
| 15–35 | **Anatomy of someone else's script** | A short real script from their field. Identify: imports, where the file paths are, what a `def` looks like, which lines are safe to change and which to leave alone. Recognition only, no authoring. |
| 35–55 | **Reading a traceback** | Bottom line first. The six errors they will actually hit: `FileNotFoundError`, `ModuleNotFoundError`, `KeyError`, `NameError`, `TypeError`, `IndentationError`. Ships with a one-page handout. |
| 55–80 | **The AI workflow** | How to prompt: data shape, three sample rows, the goal, the environment; ask for explanation alongside code; run in small pieces. Then **verification** — see below. |
| 80–90 | **Packages and environments** | `conda install` / `pip install`, why "it works on my machine" happens. Bridges to session 3. |

**The verification block is the most important 10 minutes of the course.**
Show one piece of AI-generated code that runs cleanly and is *scientifically
wrong* — a silent unit mismatch, a merge that drops rows, a mean over the wrong
axis. Then teach the checks: row counts before and after, value ranges, spot-check
three rows by hand, does the plot look physically plausible. Silent wrong answers
are the real occupational hazard for a researcher, and this is the one thing in
the course that no tutorial will teach them.

---

## 7. The two tracks collapse into one lesson

This is the structural insight that makes the course teachable by a non-domain-expert.

**MD track:** open a trajectory → loop over frames → compute RMSD per frame →
build a table of frame vs. value → plot it.

**Genomics track:** open a FASTA → loop over records → compute GC content per
sequence → build a table of sequence vs. value → plot it.

That is the same program. The shape is:

```
read structured text  →  loop over records  →  one number each
                      →  collect into a table  →  summarize / plot
```

Only the parser differs: `MDAnalysis` for one, `Biopython` for the other.

**Therefore:** teach the skeleton once in session 1 on neutral data. Split into
two homework tracks in session 2, where the only new thing each group learns is
its own parser. The instructor needs to know the shape, not the science.

Every domain example authored for this repo must be traceable back to that
five-step skeleton, and should say so explicitly in its markdown cells.

---

## 8. Demo data specification

Generated by `data/generate_demo_data.py`, seeded for reproducibility, and
committed so it can be served from a raw URL.

### Session 1 — neutral, domain-flavoured, semantically obvious

Twelve monthly CSVs, `results_2025_01.csv` … `results_2025_12.csv`, ~80 rows each.

Columns: `sample_id`, `treatment`, `replicate`, `absorbance`, `ph`, `date`

Chosen because a biochemist and an agronomist both read it instantly, and
neither track feels the other's field was favoured. Nobody stalls on biology
while learning what a variable is.

**Twelve files, not one** — this is what makes the `for` loop feel necessary
rather than academic. Concatenating twelve files in four lines is the demo that
sells the course.

**Deliberate mess**, enough to motivate cleaning, not enough to derail:
- 3–5 missing values in `absorbance`
- the string `"N/A"` in a few numeric cells, so the column loads as `object`
- inconsistent capitalization in `treatment` (`Control`, `control`, `CONTROL`)
- one fully blank row per file
- one file with a trailing comma producing a phantom `Unnamed: 6` column
- one month where `date` uses a different format

Each defect must have a corresponding one-line fix demonstrated somewhere in
session 1 or HW1. Do not add mess with no teaching payoff.

### Session 2 — track-specific

- **MD track:** a small topology + trajectory pair. The `MDAnalysisTests`
  package ships sample files (`from MDAnalysis.tests.datafiles import PSF, DCD`)
  — *verify this import and the file sizes before relying on it*. If unsuitable,
  generate a synthetic short trajectory instead. Keep it under a few MB.
- **Genomics track:** a synthetic multi-FASTA of ~50 plant gene sequences plus
  a phenotype table keyed by sequence ID, so the exercise ends in a join. Generate
  synthetically — no network dependency, no licensing question, reproducible.

---

## 9. Homework — where the learning actually happens

Sessions remove discomfort. Homework builds skill. Design it with equal care.

| | |
|---|---|
| **HW0** (pre-course) | Install Miniforge, open Jupyter, run three cells, post the output to the group. Also: bring one real data file from your own research. Non-negotiable. |
| **HW1** (after S1) | 6–8 tasks on *their own* data file, 10 minutes each. Solution notebook released two days later. |
| **HW2** (after S2) | Track-specific. Find a published script or package in your field, get it to run, change one parameter, explain in two sentences what changed and how you verified it. |
| **Capstone** | Automate one recurring task from your own work. This is the deliverable that matters. |

The capstone resolves the instructor's domain gap cleanly: **students define the
problem, the instructor judges the code.**

Accountability without extra teaching load: a five-minute show-and-tell at the
start of each session. Peer pressure does the grading.

---

## 10. Running the room (instructor notes)

- **Type the code live, with typos, and fix them.** Do not paste from prepared
  cells. Watching an expert make and repair a mistake does more for fear than
  any amount of reassurance. This is why `_live.ipynb` exists.
- **"Everyone type this now"** — then actually stay silent for 90 seconds.
  Otherwise they watch and learn nothing.
- **Pair them up.** Peer debugging scales; one instructor does not.
- **Recruit two fast learners as floating helpers** after session 1. With
  twenty people, a stuck hand waits ten minutes and that student quietly quits.
- **Group chat between sessions.** One rule: paste errors as *text*, not
  screenshots — text goes straight into an AI.
- **Have two bonus tasks ready.** The skill spread will be visible by minute 30.

**Pre-course survey** (5 questions, send a week ahead): OS; comfort with Excel
formulas; can you install software on this laptop; *what is one boring task you
repeat every month*; can you bring one real data file. The fourth question
supplies real examples for the demos.

---

## 11. Known failure modes

| Risk | Mitigation |
|---|---|
| Setup chaos eats session 1 | Colab for S1; local install as HW0 |
| Classroom Wi-Fi collapses under 20 Colab sessions | Test the room in advance; offline zip fallback |
| Silent quitting after session 1 | Nudge in the group chat on day 3 |
| AI dependence without comprehension | The §6 verification block; every homework asks "how did you check?" |
| Wide skill spread | Bonus tasks; pairing strong with weak |
| Notebook fails live | Clean-kernel execution check before every session |
| Scope drift into "real" Python | The cut list in `CLAUDE.md` |

---

## 12. Open items

- `TODO(cluster)` — session 3 needs the real cluster hostname, scheduler
  partitions, module names, account/allocation codes, and whether students
  already have accounts. Do not invent plausible values; leave the placeholders
  visible.
- Session 3 is currently overloaded: HPC mechanics and applied ML are two
  sessions of material in one 90-minute slot. A weighting decision is pending.
  Author the HPC half first.
- Class size not yet fixed; helper-recruitment and pairing advice assumes ~20.
