# Build Plan

Ordered tasks for building this repo in Claude Code. Each task has a
ready-to-paste prompt. Work in order — later tasks depend on earlier output.

## Before you start

```bash
mkdir python-crash-course && cd python-crash-course
git init
# drop CLAUDE.md, BUILD_PLAN.md, and docs/course-design.md in place
claude
```

Working notes:

- **Launch from the repo root** so `CLAUDE.md` loads. Run `/memory` to confirm
  which instruction files are active.
- **Keep `CLAUDE.md` under ~200 lines.** Past that it eats context and
  adherence drops. Detail belongs in `docs/`, loaded on demand.
- **Use plan mode for every notebook** before any cell gets written. Notebooks
  are hard to review as diffs, so agree the cell-by-cell outline first.
- **One task per session, committed before moving on.** Notebook diffs are
  noisy; small commits are the only way to review them.
- If you correct Claude on something that should be permanent, prefix the
  correction with `#` to add it to memory, then fold it into `CLAUDE.md`.

---

## Task 1 — Scaffold

> Read CLAUDE.md and docs/course-design.md. Create the directory structure in
> the repo map, with a `.gitkeep` in each empty directory and a short README.md
> that states what the repo is and points to docs/course-design.md. Add a
> .gitignore for Python, Jupyter checkpoints, and OS junk. Do not create any
> notebooks yet.

---

## Task 2 — Demo data generator

The dependency for everything in session 1. Get it right before authoring.

> Write `data/generate_demo_data.py` per §8 of docs/course-design.md. Seeded
> with numpy so output is byte-identical on re-run. It writes twelve monthly
> CSVs to `data/session1/`. Every deliberate defect listed in §8 must be
> present and each must be individually fixable in one line of pandas.
>
> After writing it: run it, then read three of the generated files back with
> pandas and print `.dtypes`, `.shape`, and `.head()` for each. Confirm that
> `absorbance` actually loads as `object` (not float) because of the "N/A"
> strings — that defect is load-bearing for the session 1 cleaning demo. Show
> me the output before we move on.

Then host `data/session1/` somewhere raw-fetchable and record the base URL in
`CLAUDE.md` under a `DATA_BASE_URL` heading.

---

## Task 3 — Session 1, complete notebook

> Read CLAUDE.md (especially the notebook authoring rules and the cut list) and
> §5 of docs/course-design.md.
>
> First, in plan mode: give me a cell-by-cell outline of
> `notebooks/01_complete.ipynb` — for each cell, its type, a one-line summary,
> and which time block from the §5 table it belongs to. Include the two
> deliberate-error cells and mark them. Confirm the outline respects the cut
> list. Do not write the notebook until I approve the outline.

Review the outline against three things: total cell count (aim 35–45), whether
any cut-list item sneaked in, and whether the six-line hook in block 1 is
genuinely impressive rather than a toy.

> Approved. Write the notebook. Then execute it end to end from a clean kernel
> with nbconvert and show me any cell that errored or produced empty output.

---

## Task 4 — Session 1, live skeleton

> Derive `notebooks/01_live.ipynb` from `01_complete.ipynb`. Same markdown
> cells, same structure, but the code cells I will type live are replaced with
> `# TYPE THIS TOGETHER` plus a comment naming what the cell will do. Keep
> fully-typed the cells that are too long to type live (imports, the data URL
> constant, anything over six lines) — I want to type roughly 60% of it.
>
> Add `<!-- ~N min -->` pacing markers above each section and print the total.
> If it exceeds 85 minutes, tell me which block to cut rather than shaving
> every block.

---

## Task 5 — Setup guides

Needed before you send HW0, so this can run in parallel with notebook work.

> Write three files in `setup/`, following the tone rule in CLAUDE.md:
>
> - `miniforge_windows.md` — install Miniforge on Windows, create a `pycourse`
>   environment with pandas, matplotlib, jupyter, openpyxl. Screenshots-worth
>   of detail in words. Name the three most likely failure points before they
>   happen and give the fix for each.
> - `wsl2.md` — `wsl --install`, the BIOS virtualization blocker, how to check
>   Windows version first, and what to do if the org has disabled it. Make
>   explicit that this does NOT replace or endanger Windows — that fear is the
>   main obstacle.
> - `verify_install.ipynb` — three cells that print the Python version, load a
>   tiny dataframe, and draw one plot. Output should be obviously
>   screenshot-able for the group chat.

---

## Task 6 — Handouts

> Write `handouts/error_cheatsheet.md`: one page, the six errors from §6 of
> docs/course-design.md. For each — what the traceback looks like, what it
> actually means in plain language, the two most common causes, and the first
> thing to try. Formatted to print on one side of A4.
>
> Then `handouts/ai_prompting_for_code.md`: how to ask an AI for research code.
> The context checklist (data shape, three sample rows, goal, environment), why
> to ask for an explanation alongside the code, and the verification checklist
> from §6. Include one fully worked before/after example of a bad prompt and a
> good one, using the session 1 dataset.

---

## Task 7 — The verification demo

Do this as its own task. It is the highest-value content in the course and it
will be mediocre if it is bolted onto a bigger prompt.

> Build the §6 verification block as a standalone notebook,
> `notebooks/02_verification_demo.ipynb`. I need a piece of AI-generated-looking
> code that runs without error, produces a plausible number, and is
> scientifically wrong in a way a domain researcher would plausibly miss —
> a merge that silently drops rows, or an aggregate over the wrong axis. Use
> the session 1 dataset.
>
> Structure: the plausible-looking result, then the four checks that catch it
> (row count before/after, value range, hand-check three rows, does the plot
> look physically sensible), then the corrected version. The wrongness must be
> subtle enough that I could believe it, and obvious in hindsight once checked.

---

## Task 8 — Session 2, both tracks

Blocked until you have real student data files from HW0. Author against the
synthetic data from §8 in the meantime.

> Read §6 and §7 of docs/course-design.md. Build `notebooks/02_complete.ipynb`
> as a shared core plus two track appendices — MD and genomics. Every domain
> example must be annotated with which of the five skeleton steps from §7 it
> is performing, in the markdown cell above it. Verify the MDAnalysis test-data
> import actually works before building on it; if it does not, tell me and
> propose a synthetic alternative rather than working around it silently.

---

## Task 9 — Homework specs

> Write the five homework files listed in the repo map. HW1 gets 6–8 tasks
> against the student's *own* data file, each ≤ 10 minutes, each stating what
> "done" looks like. Every homework must include the question "how did you
> check the answer was right?" as a required part of the submission.

---

## Task 10 — Session 3 (blocked)

Do not start until the cluster details in §12 are known. When they are:

> Fill in the `TODO(cluster)` placeholders throughout the repo, then build
> `notebooks/03_hpc.ipynb` and `handouts/slurm_template.sh`. The SLURM template
> is fill-in-the-blank with every line commented in plain language. Assume the
> student has never seen a terminal before today.

---

## Review checklist before session 1

- [ ] `01_live.ipynb` and `01_complete.ipynb` both execute clean-kernel
- [ ] You have run through `01_live.ipynb` once, out loud, with a timer
- [ ] Demo data URL fetches over the classroom Wi-Fi, from a phone hotspot too
- [ ] Offline zip fallback prepared
- [ ] HW0 sent at least 5 days ahead; you have screenshots from most students
- [ ] Pre-course survey responses read, and at least one demo example swapped
      to match something a student actually said was boring
- [ ] Error cheatsheet printed
- [ ] Two bonus tasks ready for whoever finishes early
