"""Single source of truth for the two Session-1 notebooks.

Fundamentals-first structure, built bottom-up for learners with zero prior
programming:

  Part 1  Python basics on everyday values (print, variable, string ops, if,
          list/append, loop)
  Part 2  Your first real file: a taste of lab data, then one CSV
  Part 3  All the files at once: the loop, groupby, one plot
  Part 4  A taste of your field's tool (Biopython / MDAnalysis) — same skeleton

Every cell is defined ONCE below, then rendered two ways so the live skeleton
and the complete answer key stay identical in structure:

  notebooks/01_complete.ipynb  full worked version, executed end-to-end
  notebooks/01_live.ipynb      instructor cockpit + student legend + per-cell
                               role markers + pacing comments

Regenerate both:  python3 notebooks/build_session1.py

Cell ROLE (gradual release of responsibility):
  ido    "I DO"    — instructor runs it, students watch. Setup / long cells.
  wedo   "WE DO"   — everyone types it now, then checkpoint. The default.
  youdo  "YOU DO"  — students change ONE thing in working code.
  run    "RUN THIS"— students just run a pre-filled cell (Part 4 field tastes).

Deliberate-error cells are tagged `raises-exception`; Colab-only install cells
are tagged `skip-execution` so this local build installs nothing.
"""

from pathlib import Path

import nbformat
from nbclient import NotebookClient

HERE = Path(__file__).resolve().parent
DATA_BASE_URL = (
    "https://raw.githubusercontent.com/sanzidikawsar/"
    "python-crash-course/main/data/session1"
)

CELLS = []


def md(src, section=None, minutes=None):
    CELLS.append({"kind": "md", "src": src, "section": section, "minutes": minutes})


def code(src, role="wedo", hint="", youdo="", raises=False, skip=False):
    CELLS.append(
        {"kind": "code", "src": src, "role": role, "hint": hint, "youdo": youdo,
         "raises": raises, "skip": skip}
    )


# =========================================================================
# WELCOME
# =========================================================================
md(
    "# Session 1 — Make the Computer Do Your Boring Work\n"
    "\n"
    "You have never written code before. That is exactly who this is for. We "
    "start from the very beginning, on everyday examples, and build up — step by "
    "step — until you can take twelve messy files, clean them, summarise them, "
    "and draw a plot. At the end you will even peek at your own field's Python "
    "tool.\n"
    "\n"
    "**By the end of today you can:**\n"
    "\n"
    "- Read and run Python, and change one thing safely\n"
    "- Open a data file and see what is inside it\n"
    "- Clean the messes that show up in almost every real dataset\n"
    "- Summarise with one line and draw a plot you could put in a paper\n"
    "- Read an error message instead of fearing it\n"
    "\n"
    "You will *not* be asked to write programs from a blank page. The goal is to "
    "read, run, and safely change code — the skills you actually need on Monday.",
    section="Welcome", minutes=0,
)

# =========================================================================
# SETUP (Colab plumbing)
# =========================================================================
md(
    "## Setup (Google Colab only)\n"
    "\n"
    "Run the cell below **first**, before we start. It loads the two main tools "
    "we use. If Colab shows a *Restart* button afterwards, click it — that is "
    "normal and happens only once. Not on Colab? You can skip this cell."
)
code(
    "# Colab only. Run this first, before we start.\n"
    "!pip install -q pandas==2.2.2 matplotlib==3.9.2\n"
    'print("Libraries ready.")',
    role="ido", skip=True,
)

# =========================================================================
# PART 1 — PYTHON BASICS ON EVERYDAY VALUES
# =========================================================================
md(
    "# Part 1 · Python basics\n"
    "\n"
    "Five building blocks make up almost all code. We learn them on everyday "
    "things — fruit, temperature, a name — with nothing about your research yet. "
    "That comes in Part 2. Type each cell yourself and run it with "
    "**Shift + Enter**.",
    section="Part 1 · Python basics", minutes=15,
)

md(
    "**Variable and print.** A **variable** is just a name for a value. "
    "**`print(...)`** shows a value on the screen. Number variables can be added, "
    "subtracted, and so on."
)
code(
    "apples = 5\n"
    "oranges = 3\n"
    'print("total fruit:", apples + oranges)',
    role="wedo", hint="make two number variables and print their total",
)

md(
    "**Strings and string operations.** Text is a **string**, written in quotes. "
    "Strings have handy operations: `.strip()` removes stray spaces at the ends, "
    "and `.capitalize()` fixes the casing. Remember these two — we use them to "
    "clean messy data very soon."
)
code(
    'name = "  sara  "\n'
    'print("cleaned:", name.strip().capitalize())',
    role="wedo", hint="clean up a messy name with .strip() and .capitalize()",
)

md(
    "**Making a decision with `if`.** The indented line runs only when the "
    "condition is true. An everyday example — body temperature:"
)
code(
    "temperature = 38.0\n"
    "if temperature > 37.5:\n"
    '    print("that is a fever")',
    role="wedo", hint="print a warning only if the temperature is above 37.5",
)

md(
    "**Lists.** A **list** holds several values in order, inside square "
    "brackets. `.append(...)` adds one item to the end — this is exactly how we "
    "collect many files later. `len(...)` tells you how many items there are."
)
code(
    'fruits = ["apple", "banana"]\n'
    'fruits.append("mango")\n'
    "print(fruits)\n"
    'print("how many:", len(fruits))',
    role="wedo", hint="make a list, add an item, and count the items",
)

md(
    "**The `for` loop.** A loop repeats the same step once for each item in a "
    "list. Watch it print one line per fruit — that is the loop *going around* "
    "three times:"
)
code(
    "for fruit in fruits:\n"
    '    print("I have a", fruit)',
    role="wedo", hint="loop over the fruit list and print each one",
)

md(
    "### Break it on purpose\n"
    "\n"
    "Errors are not failures — they are the computer telling you what it could "
    "not do. The one habit that matters most today: **read the last line "
    "first.** Let's misspell a name on purpose and see:"
)
code("print(fruitss)", role="wedo", raises=True,
     hint="ask for a variable name we never made (a deliberate typo)")

md(
    "Read the traceback from the **bottom up**. The last line says "
    "`NameError: name 'fruitss' is not defined` — `NameError` means *I have "
    "never heard of that name*. We simply misspelled `fruits`. The fix:"
)
code("print(fruits)", role="wedo", hint="spell the variable name correctly")

# =========================================================================
# PART 2 — YOUR FIRST REAL FILE
# =========================================================================
md(
    "# Part 2 · Your first real file\n"
    "\n"
    "Now the same ideas, on real lab data. First a tiny taste to show your data "
    "is *just numbers and text* like Part 1 — then a whole file.",
    section="Part 2 · Your first real file", minutes=25,
)

md(
    "Here are a few **absorbance readings** — a list of numbers, exactly like "
    "the fruit list. We can loop over them and find the biggest with `max(...)`:"
)
code(
    "absorbance_readings = [0.42, 0.55, 0.38, 1.20]\n"
    "for reading in absorbance_readings:\n"
    '    print("reading:", reading)\n'
    'print("highest:", max(absorbance_readings))',
    role="wedo", hint="loop over the readings and print the highest",
)

md(
    "And a messy **treatment label** — clean it with the exact string operations "
    "you just learned:"
)
code(
    'treatment = "  CONTROL  "\n'
    'print("cleaned:", treatment.strip().capitalize())',
    role="wedo", hint="clean the messy treatment label",
)

md(
    "## Loading a whole file\n"
    "\n"
    "Real data lives in files. A **DataFrame** is just a table — rows and "
    "columns, like an Excel sheet — and each column behaves like the lists you "
    "just made, only with a name. `pd.read_csv(...)` loads one CSV file into a "
    "DataFrame. We load **one** month first, slowly. First bring in the tools "
    "and the address of our data:"
)
code(
    "import pandas as pd\n"
    "import matplotlib.pyplot as plt\n"
    "%matplotlib inline\n"
    "\n"
    'DATA_BASE_URL = "' + DATA_BASE_URL + '"\n'
    "\n"
    'print("ready, pandas", pd.__version__)',
    role="ido",
)

md("Now read January and look at the first rows with `.head()`:")
code(
    'jan = pd.read_csv(f"{DATA_BASE_URL}/results_2025_01.csv")\n'
    "jan.head()",
    role="wedo", hint="read January into a DataFrame and show the first rows",
)

md(
    "Two everyday questions about any table: how big is it, and what kind of "
    "value is in each column? `.shape` gives (rows, columns):"
)
code('print("rows, columns:", jan.shape)',
     role="wedo", hint="print the number of rows and columns")

md(
    "`.dtypes` lists each column's type. `float64` is decimal numbers, `int64` "
    "whole numbers, `object` usually means text. Watch **`absorbance`** — it is "
    "a measurement, so we expect a number, but it arrives as `object`. Something "
    "non-numeric is hiding in it."
)
code("jan.dtypes", role="ido", hint="show the type of every column")

md(
    "`.describe()` gives quick statistics for the number columns. Notice "
    "`absorbance` is **missing** — pandas will not do statistics on a column it "
    "thinks is text. We fix that below."
)
code("jan.describe()", role="ido", hint="summary statistics for numeric columns")

md("To look at one column, name it in square brackets:")
code('jan["ph"].head()', role="wedo", hint="show just the pH column")

md(
    "For several columns, pass a **list** of names — that is the two sets of "
    "brackets: the outer selects, the inner is the list."
)
code(
    'jan[["sample_id", "ph"]].head()',
    role="youdo",
    youdo='add a third column name to the list, e.g. "treatment", and rerun.',
)

md(
    "**Filtering** keeps only rows matching a condition — the same `>` idea as "
    "the fever check, applied to every row at once:"
)
code(
    'high_ph = jan[jan["ph"] > 7.5]\n'
    'print("high-pH rows:", high_ph.shape[0])\n'
    "high_ph.head()",
    role="wedo", hint="keep only the rows where pH is above 7.5",
)

md(
    "### Break it on purpose\n"
    "\n"
    "The error you will hit most: a column name that is not exactly right. "
    "pandas is **case-sensitive** — `ph` and `PH` are different:"
)
code('jan["PH"].head()', role="wedo", raises=True,
     hint="ask for a column with the wrong capitalisation (on purpose)")

md(
    "Last line: `KeyError: 'PH'`. A `KeyError` means *that column is not in the "
    "table*. Almost always a typo or wrong capitalisation. It is `ph`:"
)
code('jan["ph"].head()', role="wedo", hint="use the exact column name, lower-case")

md(
    "## Cleaning the three messes\n"
    "\n"
    "**Mess 1 — absorbance is text.** A few cells hold `n.d.` (*not detected*) "
    "and a few are blank. `pd.to_numeric(..., errors=\"coerce\")` turns the "
    "column into real numbers and replaces anything it cannot convert with "
    "`NaN` (pandas' word for missing). One line:"
)
code(
    'jan["absorbance"] = pd.to_numeric(jan["absorbance"], errors="coerce")\n'
    'print("new type:", jan["absorbance"].dtype)\n'
    'jan["absorbance"].describe()',
    role="wedo", hint="turn absorbance into real numbers, then summarise it",
)

md(
    "**Mess 2 — messy treatment labels** (`Control`, `control`, `CONTROL`). The "
    "same `.strip().capitalize()` from Part 1, applied to the whole column:"
)
code(
    'jan["treatment"] = jan["treatment"].str.strip().str.capitalize()\n'
    'jan["treatment"].value_counts()',
    role="wedo", hint="make every treatment label consistent, then recount",
)

md(
    "**Mess 3 — one fully-blank row** in every file. `dropna(how=\"all\")` "
    "removes only rows where *every* value is missing:"
)
code(
    'jan = jan.dropna(how="all")\n'
    'print("rows after cleaning:", jan.shape[0])',
    role="wedo", hint="drop the fully-empty row and recount",
)

# =========================================================================
# PART 3 — ALL THE FILES AT ONCE
# =========================================================================
md(
    "# Part 3 · All the files at once\n"
    "\n"
    "We have twelve monthly files. Doing them by hand is an afternoon; with a "
    "`for` loop it is a few lines. We build up in three small steps.",
    section="Part 3 · All the files at once", minutes=25,
)

md(
    "**Step 1** — watch the loop run on just three files. It prints one line "
    "each time around, so you can *see* it repeat:"
)
code(
    'for month in ["01", "02", "03"]:\n'
    '    file_url = f"{DATA_BASE_URL}/results_2025_{month}.csv"\n'
    "    one_month = pd.read_csv(file_url)\n"
    '    print("month", month, "->", one_month.shape)',
    role="wedo", hint="loop over three files and print the size of each",
)

md("**Step 2** — here are all twelve month labels in one list:")
code(
    'months = ["01", "02", "03", "04", "05", "06",\n'
    '          "07", "08", "09", "10", "11", "12"]\n'
    'print("we have", len(months), "months")',
    role="wedo", hint="make the list of twelve month labels",
)

md(
    "**Step 3** — the full run. The same loop, but now we also **tag** each file "
    "with its month and **append** it to a list, then `pd.concat` stacks all "
    "twelve into one table. Every line is one you have already met:"
)
code(
    "all_months = []\n"
    "for month in months:\n"
    '    file_url = f"{DATA_BASE_URL}/results_2025_{month}.csv"\n'
    "    monthly = pd.read_csv(file_url)\n"
    '    monthly["month"] = month\n'
    "    all_months.append(monthly)\n"
    "year = pd.concat(all_months, ignore_index=True)\n"
    'print("total rows:", year.shape[0])',
    role="ido",
)

md(
    "The same three fixes as before, now applied once to the whole year — one "
    "line each:"
)
code(
    'year = year.dropna(how="all")\n'
    'year["absorbance"] = pd.to_numeric(year["absorbance"], errors="coerce")\n'
    'year["treatment"] = year["treatment"].str.strip().str.capitalize()\n'
    "year.dtypes",
    role="ido",
)

md(
    "**`groupby`** is the loop you do not have to write: it splits the table "
    "into groups and gives one number per group. Average absorbance per "
    "treatment:"
)
code(
    'year.groupby("treatment")["absorbance"].mean()',
    role="wedo", hint="average absorbance for each treatment",
)

md("Swap `.mean()` for `.count()` to count the samples in each group:")
code(
    'year.groupby("treatment")["absorbance"].count()',
    role="youdo",
    youdo="you just saw .mean(). Change .count() to .max() and rerun — what does it show?",
)

md(
    "Group by `month` instead, and we get an average for every month — a "
    "twelve-row table ready to plot:"
)
code(
    'monthly_mean = year.groupby("month")["absorbance"].mean()\n'
    "monthly_mean",
    role="wedo", hint="average absorbance for each month",
)

md(
    "## One picture worth keeping\n"
    "\n"
    "Our `monthly_mean` table has two parts: `.index` (the labels — the months) "
    "and `.values` (the numbers — the averages). `plt.plot` needs both. Always "
    "label the axes and add a title. `plt.savefig` writes an image you could "
    "drop into a paper:"
)
code(
    'plt.plot(monthly_mean.index, monthly_mean.values, marker="o")\n'
    'plt.xlabel("Month")\n'
    'plt.ylabel("Mean absorbance")\n'
    'plt.title("Average absorbance by month, 2025")\n'
    'plt.savefig("absorbance_by_month.png", dpi=150)\n'
    "plt.show()",
    role="wedo",
    hint="plot the monthly averages with labels, a title, and save it",
)

md(
    "A different question — how do the treatments compare overall? — wants a "
    "different picture. `plt.bar` draws one bar per group:"
)
code(
    'treatment_mean = year.groupby("treatment")["absorbance"].mean()\n'
    "plt.bar(treatment_mean.index, treatment_mean.values)\n"
    'plt.ylabel("Mean absorbance")\n'
    'plt.title("Absorbance by treatment")\n'
    "plt.show()",
    role="youdo",
    youdo='change the title, or change "treatment" to "month" to plot the monthly trend as bars.',
)

# =========================================================================
# PART 4 — A TASTE OF YOUR FIELD'S TOOL
# =========================================================================
md(
    "# Part 4 · A taste of your field's tool\n"
    "\n"
    "Everything today had the same shape: **open something → loop over its "
    "records → get one number each → collect into a table → summarise or plot.** "
    "Your research tools follow the *exact same shape* — only the opener "
    "changes. Here is a tiny taste. **Run the cell for your own field.** Next "
    "session we go hands-on.",
    section="Part 4 · A taste of your field's tool", minutes=15,
)
code(
    "# Colab only. Installs your field libraries (this one is a bit slower).\n"
    "!pip install -q biopython MDAnalysis MDAnalysisTests\n"
    'print("Field libraries ready.")',
    role="ido", skip=True,
)
code(
    "import warnings\n"
    'warnings.filterwarnings("ignore")\n'
    "from Bio.Seq import Seq\n"
    "from Bio.SeqUtils import gc_fraction\n"
    "import MDAnalysis as mda\n"
    "from MDAnalysis.tests.datafiles import PSF, DCD\n"
    'print("imported")',
    role="run", hint="load both field tools",
)

md(
    "**Genomics** — read three DNA sequences and get one number each (their GC "
    "content). Same shape as absorbance-per-file: *loop → one number each*:"
)
code(
    'sequences = ["ATATATATATATATAT", "ATGCATGCATGCATGC", "GCGCGCGCGCGCGCGC"]\n'
    "for dna in sequences:\n"
    '    print("GC%:", round(gc_fraction(Seq(dna)) * 100, 1))',
    role="run", hint="genomics — GC content of each sequence",
)

md(
    "**Molecular dynamics** — open a small simulation and get one number per "
    "frame (the protein's size). Same shape again: *loop over frames → one "
    "number each → collect into a list*:"
)
code(
    "import warnings\n"
    'warnings.filterwarnings("ignore")\n'
    "universe = mda.Universe(PSF, DCD)\n"
    'protein = universe.select_atoms("protein")\n'
    "sizes = []\n"
    "for frame in universe.trajectory:\n"
    "    sizes.append(round(float(protein.radius_of_gyration()), 2))\n"
    'print("measured", len(sizes), "frames; first 5 sizes:", sizes[:5])',
    role="run", hint="molecular dynamics — protein size per frame",
)

# =========================================================================
# WRAP UP
# =========================================================================
md(
    "# Wrap up\n"
    "\n"
    "**What you can do now**, and could not an hour ago: read and run Python, "
    "open and clean a data file, combine many files, summarise with `groupby`, "
    "draw a labelled plot, and read an error message calmly. You even saw your "
    "own field's tool follow the very same pattern.\n"
    "\n"
    "**Homework** (on *your own* data file):\n"
    "\n"
    "- Read your file with `pd.read_csv` and run `.head()`, `.shape`, `.dtypes`\n"
    "- Find one column that loaded as `object` but should be a number, and fix it\n"
    "- Filter to a subset of rows that matters to you, and count them\n"
    "- Use `groupby` to get one number per group\n"
    "- Draw one labelled plot and save it as a PNG\n"
    "- For every answer, write one sentence: *how did you check it was right?*\n"
    "\n"
    "Bring the notebook — working or broken — next session. A broken cell with "
    "its error message is exactly what we want to look at together.",
    section="Wrap up", minutes=10,
)


# --- instructor cockpit + student legend (live notebook only) -------------

COCKPIT = (
    "# \U0001F39B️ Instructor cockpit — READ BEFORE CLASS, then collapse / scroll past\n"
    "\n"
    "*This cell is for you, not the students. Collapse it (click the arrow) or "
    "scroll past it before you project the screen.*\n"
    "\n"
    "## The one job\n"
    "Reduce fear and build “I can run and change code” confidence — **not** "
    "“write from scratch.” This session is deliberately bottom-up: everyday "
    "values first, their data second, their field's tool last. When you fall "
    "behind, cut *content*, never the error-reading or the students' typing.\n"
    "\n"
    "## Cell roles (a comment at the top of every code cell)\n"
    "- **`# I DO`** — you run it, students **watch**. Setup and long cells.\n"
    "- **`# WE DO`** — **everyone types it now.** Say “type this,” then go quiet "
    "~90 seconds. Checkpoint before moving on.\n"
    "- **`# YOU DO`** — students **change one thing** in working code.\n"
    "- **`# RUN THIS`** — students just run a ready-made cell (Part 4 tastes).\n"
    "\n"
    "## Say this out loud in the first 5 minutes\n"
    "> “If you ever fall behind typing, open **01_complete** (the answer "
    "notebook), run down to where we are, and rejoin. Nobody gets stuck.”\n"
    "\n"
    "## Timing — markers are in the notebook, total 90 min\n"
    "\n"
    "| Part | Min | If you're behind, cut… |\n"
    "|---|---|---|\n"
    "| 1 · Python basics | 15 | nothing — this is the foundation |\n"
    "| 2 · Your first real file | 25 | the two-column select (YOU DO) |\n"
    "| 3 · All the files at once | 25 | the bar chart (YOU DO); keep the line plot |\n"
    "| 4 · A taste of your field's tool | 15 | run only your own track's cell |\n"
    "| Wrap up | 10 | never — this is the homework handoff |\n"
    "\n"
    "## Room mechanics\n"
    "- **Checkpoint, don't wait per cell.** Run 2–3 cells, then pause on a "
    "`WE DO`.\n"
    "- **“Thumbs up when your cell ran”** — read the room in 3 seconds.\n"
    "- **Pair fast + slow**; one types, one reads aloud. Swap each part.\n"
    "- **Recruit 2 fast finishers as helpers** after the first 30 min.\n"
    "- **Break-it-on-purpose cells: slow down.** Trigger the error, let it sit, "
    "read the **last line first**, out loud.\n"
    "- **Part 4 is a confidence taste, not a lesson.** Let each student run "
    "their own field's cell and be impressed. Do not explain the internals.\n"
    "\n"
    "## Pre-class checklist\n"
    "- [ ] Ran through this live notebook once, out loud, with a timer\n"
    "- [ ] Opened the data URL on classroom Wi-Fi **and** a phone hotspot\n"
    "- [ ] Ran the Part 4 install once yourself — MDAnalysis takes a minute\n"
    "- [ ] `01_complete` open in a second tab as your answer key\n"
    "- [ ] Two bonus prompts ready for whoever finishes early\n"
    "\n"
    "## Domain crib sheet (you know code; here's the science the terms mean)\n"
    "You are a CS grad, not a biochemist — you never need the science, only "
    "enough to answer “what is that?” without stalling. The plan is built so you "
    "teach the *shape*, and students supply the domain.\n"
    "\n"
    "**Session data (Parts 2–3):**\n"
    "- `absorbance` — a light-absorption reading from a spectrophotometer; "
    "higher = more of the substance present. Just a measurement column.\n"
    "- `ph` — acidity, 0–14 (7 = neutral). A number.\n"
    "- `treatment` = `Control` vs `Treated` — experimental groups (control got "
    "nothing, treated got the intervention). Think A/B test.\n"
    "- `replicate` — the same experiment repeated (1/2/3) for reliability.\n"
    "- `n.d.` — “not detected” (below the instrument's limit); this is why "
    "`absorbance` loads as text.\n"
    "\n"
    "**Part 4 — Genomics (Biopython):**\n"
    "- A DNA **sequence** is a string of letters `A/T/G/C` (the bases).\n"
    "- **GC content** = the percentage of bases that are `G` or `C`. A standard, "
    "simple property (higher GC ≈ more thermally stable). Literally count G+C, "
    "divide by length.\n"
    "- **Biopython** (`Bio`) — the standard Python library for biological "
    "sequences (reading FASTA files, computing sequence properties).\n"
    "\n"
    "**Part 4 — Molecular dynamics (MDAnalysis):**\n"
    "- **Molecular dynamics (MD)** — a physics simulation of how a molecule (here "
    "a protein) wiggles over time. Output is a **trajectory**: many snapshots "
    "(**frames**), each holding the 3-D positions of every atom.\n"
    "- **Radius of gyration** — one number for how compact vs spread-out the "
    "protein is in a frame; it moves as the protein folds/unfolds. We compute "
    "one per frame → a table over time.\n"
    "- **MDAnalysis** (`mda`) — the standard Python library to read MD "
    "trajectories and measure things. **PSF/DCD** are file formats (PSF = which "
    "atoms exist, DCD = their positions per frame); the sample files ship with "
    "the library.\n"
    "\n"
    "**Why the two tracks are one lesson:** open → loop over records → one number "
    "each → collect into a table → summarise/plot. Absorbance-per-file, "
    "GC-per-sequence, and radius-per-frame are the same shape. Teach the shape.\n"
    "\n"
    "## Dialing the typing load\n"
    "Change a cell's `role=` in `build_session1.py` and rerun it. More confident "
    "typing live? Turn some `I DO` into `WE DO`. Want them typing less? Turn "
    "some `WE DO` into `I DO` or `YOU DO`."
)

STUDENT_LEGEND = (
    "## How to follow along\n"
    "\n"
    "Every code cell starts with a comment telling you what to do:\n"
    "\n"
    "- **`# I DO`** — just watch; I'll run it.\n"
    "- **`# WE DO`** — everyone type it now, then run it (**Shift + Enter**).\n"
    "- **`# YOU DO`** — change the one thing I point to, then run it.\n"
    "- **`# RUN THIS`** — just run the ready-made cell (no typing).\n"
    "\n"
    "Fallen behind? Open **01_complete**, run down to where we are, and rejoin — "
    "that is completely fine."
)


# --- rendering ------------------------------------------------------------

def _tags(c):
    tags = []
    if c["raises"]:
        tags.append("raises-exception")
    if c["skip"]:
        tags.append("skip-execution")
    return {"tags": tags} if tags else {}


def render_complete_code(c):
    return nbformat.v4.new_code_cell(c["src"], metadata=_tags(c))


def render_live_code(c):
    role = c["role"]
    if role == "wedo":
        src = "# WE DO — everyone type this now:\n# " + c["hint"]
    elif role == "ido":
        src = "# I DO — I'll run this, just watch:\n" + c["src"]
    elif role == "youdo":
        src = "# YOU DO — change one thing: " + c["youdo"] + "\n" + c["src"]
    elif role == "run":
        src = "# RUN THIS (" + c["hint"] + ") — just run it, no typing:\n" + c["src"]
    else:
        src = c["src"]
    return nbformat.v4.new_code_cell(src, metadata=_tags(c))


def build_complete():
    nb = nbformat.v4.new_notebook()
    cells = []
    for c in CELLS:
        if c["kind"] == "md":
            cells.append(nbformat.v4.new_markdown_cell(c["src"]))
        else:
            cells.append(render_complete_code(c))
    nb.cells = cells
    nb.metadata["language_info"] = {"name": "python"}
    return nb


def build_live():
    rendered = []
    for c in CELLS:
        if c["kind"] == "md":
            src = c["src"]
            if c["minutes"] is not None:
                src = f"<!-- ~{c['minutes']} min -->\n\n" + src
            rendered.append(nbformat.v4.new_markdown_cell(src))
        else:
            rendered.append(render_live_code(c))

    nb = nbformat.v4.new_notebook()
    nb.cells = (
        [nbformat.v4.new_markdown_cell(COCKPIT), rendered[0],
         nbformat.v4.new_markdown_cell(STUDENT_LEGEND)]
        + rendered[1:]
    )
    nb.metadata["language_info"] = {"name": "python"}
    return nb


def main():
    complete = build_complete()
    client = NotebookClient(
        complete, timeout=300, kernel_name="python3",
        resources={"metadata": {"path": "/tmp"}},
    )
    client.execute()
    nbformat.write(complete, HERE / "01_complete.ipynb")

    nbformat.write(build_live(), HERE / "01_live.ipynb")

    code_cells = [c for c in CELLS if c["kind"] == "code"]
    n = len(code_cells)
    counts = {r: sum(1 for c in code_cells if c["role"] == r)
              for r in ("ido", "wedo", "youdo", "run")}
    total_min = sum(c["minutes"] for c in CELLS if c.get("minutes"))
    print(f"cells: {len(CELLS)} total, {n} code, {len(CELLS) - n} markdown")
    print(f"roles: WE DO {counts['wedo']} | YOU DO {counts['youdo']} | "
          f"RUN {counts['run']} | I DO {counts['ido']}")
    print(f"pacing markers sum to: {total_min} min")


if __name__ == "__main__":
    main()
