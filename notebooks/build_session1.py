"""Single source of truth for the two Session-1 notebooks.

Every cell is defined ONCE below, then rendered two ways so the live skeleton
and the complete version are guaranteed identical in structure (CLAUDE.md
notebook rule 1):

  notebooks/01_complete.ipynb  full worked version, executed end-to-end (the
                               answer key; released to students afterwards)
  notebooks/01_live.ipynb      what you teach from: an instructor "cockpit"
                               run-sheet on top, a student "how to follow"
                               legend, per-cell role markers, and pacing.

Regenerate both:  python3 notebooks/build_session1.py

Each code cell has a teaching ROLE (gradual release of responsibility):

  ido   "I DO"   — instructor types/runs it, students watch. Setup + long cells.
  demo  "I DO"   — instructor types it LIVE for drama (the hook). Blank in live.
  wedo  "WE DO"  — everyone types it now, then checkpoint. The default.
  youdo "YOU DO" — students change ONE thing in working code (the target skill).

Deliberate-error cells are tagged `raises-exception` so their real traceback is
captured as output instead of halting the clean-kernel run. The Colab-only
install cell is tagged `skip-execution` so this local build installs nothing.
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
# OPENING
# =========================================================================
md(
    "# Session 1 — Make the Computer Do Your Boring Work\n"
    "\n"
    "Twelve months of lab results, twelve messy files. By hand in Excel this is "
    "an afternoon. We are going to do it in a few lines, live, together.\n"
    "\n"
    "**By the end of this session you can:**\n"
    "\n"
    "- Open a data file in Python and see what is inside it\n"
    "- Combine many files into one table without copy-paste\n"
    "- Clean the three messes that show up in almost every real dataset\n"
    "- Summarise a whole year with one line, and draw a plot you could put in a paper\n"
    "- Read an error message instead of fearing it\n"
    "\n"
    "You will not write programs from scratch today. The goal is to *read, run, "
    "and safely change* code — the skills you actually need on Monday.",
    section="Welcome", minutes=0,
)

# =========================================================================
# SETUP (Colab plumbing)
# =========================================================================
md(
    "## Setup (Google Colab only)\n"
    "\n"
    "The cell below installs the two tools we use. **Run it first, before we "
    "start.** If Colab shows a *Restart* button after it finishes, click it — "
    "that is normal and only happens once. If you are not on Colab you can skip "
    "this cell."
)
code(
    "# Colab only. Run this first, before we start.\n"
    "!pip install -q pandas==2.2.2 matplotlib==3.9.2\n"
    'print("Libraries ready.")',
    role="ido", skip=True,
)

md(
    "## Load the tools\n"
    "\n"
    "An **import** loads a toolbox someone else wrote. `pandas` is a spreadsheet "
    "that lives in Python; we nickname it `pd`. `matplotlib` draws charts; we "
    "nickname its drawing part `plt`. A **variable** is just a name we give to a "
    "value so we can reuse it — here `DATA_BASE_URL` holds the web address our "
    "data lives at, written once so we never retype it."
)
code(
    "import pandas as pd\n"
    "import matplotlib.pyplot as plt\n"
    "%matplotlib inline\n"
    "\n"
    'DATA_BASE_URL = "' + DATA_BASE_URL + '"\n'
    "\n"
    'print("pandas version:", pd.__version__)',
    role="ido",
)

# =========================================================================
# BLOCK 1 — THE HOOK
# =========================================================================
md(
    "## The 30-minute Excel job, in a few lines\n"
    "\n"
    "We have twelve files, one per month, named `results_2025_01.csv` up to "
    "`results_2025_12.csv`. In Excel you would open each, copy, paste, and pray. "
    "Watch what happens instead. Do not worry about understanding every word yet "
    "— we take it apart right after.",
    section="The hook", minutes=10,
)
code(
    'months = ["01", "02", "03", "04", "05", "06",\n'
    '          "07", "08", "09", "10", "11", "12"]\n'
    "all_months = []\n"
    "for month in months:\n"
    '    file_url = f"{DATA_BASE_URL}/results_2025_{month}.csv"\n'
    "    all_months.append(pd.read_csv(file_url))\n"
    "year = pd.concat(all_months, ignore_index=True)\n"
    'print("Loaded", year.shape[0], "rows from 12 files")',
    role="demo",
    hint="list the 12 months, read each file, stack them into one table `year`",
)

md(
    "Here are the first rows of the whole year in one glance. That table has a "
    "name: a **DataFrame** — Python's version of a spreadsheet. We will get to "
    "know it properly in a few minutes; for now just notice it is rows and "
    "columns, exactly like Excel."
)
code("year.head()", role="wedo", hint="peek at the top of the combined table")

md(
    "Now count how many rows belong to each treatment. Look closely at the "
    "result — something is already wrong, and spotting it is your first real "
    "data-cleaning instinct."
)
code(
    'year["treatment"].value_counts()',
    role="wedo",
    hint="count rows per treatment — notice `Control` appears more than once",
)

md(
    "`Control`, `control`, and `CONTROL` are counted as three different things, "
    "even though they mean the same treatment. That is the kind of silent mess "
    "we will learn to fix. First, let's slow all the way down and understand "
    "what we just did."
)

# =========================================================================
# BLOCK 2 — NOTEBOOK MECHANICS
# =========================================================================
md(
    "## How a notebook works\n"
    "\n"
    "A notebook is a stack of **cells**. A cell holds either text (like this "
    "one) or code. You run a code cell with **Shift + Enter**. The `[ ]` on the "
    "left becomes a number showing the order things ran in. Cells share memory: "
    "a variable made in one cell is available in the next. Run order matters — "
    "if you skip around, Python only knows what it has actually run.",
    section="Notebook mechanics", minutes=15,
)
code(
    "sample_count = 81\n"
    'print("rows in one file:", sample_count)',
    role="wedo", hint="make a number variable and print it",
)

md(
    "Values come in types. A **number** you can do maths with; a **string** is "
    "text, written inside quotes. The `f\"...\"` below is an *f-string* — Python "
    "swaps anything in `{ }` for its value, so we can mix text and variables in "
    "one printed line."
)
code(
    'treatment_name = "Control"\n'
    'print(f"the treatment is {treatment_name}")',
    role="wedo", hint="store text in a variable and print it inside a sentence",
)

md(
    "Code can make a decision with **`if`**: the indented line runs only when "
    "the condition is true. A pH above 7.5 is slightly basic, so:"
)
code(
    "newest_ph = 7.6\n"
    "if newest_ph > 7.5:\n"
    '    print("this sample is slightly basic")',
    role="wedo", hint="print a message only if pH is above 7.5",
)

md(
    "A **list** is an ordered collection, written in square brackets. You reach "
    "an item by its position, and Python counts from **0**, so the first item is "
    "`[0]`. `len(...)` tells you how many items there are."
)
code(
    "plate_wells = [1, 2, 3, 4, 5, 6]\n"
    'print("first well:", plate_wells[0])\n'
    'print("how many:", len(plate_wells))',
    role="wedo", hint="make a list, grab the first item, count the items",
)

md(
    "Lists can grow. `.append(...)` adds one item to the end. This is exactly "
    "the trick we use to collect twelve files into one list:"
)
code(
    "collected = []\n"
    'collected.append("first")\n'
    'collected.append("second")\n'
    "print(collected)",
    role="wedo", hint="start an empty list and add two items to it",
)

md(
    "### Break it on purpose\n"
    "\n"
    "We are going to cause an error on purpose. Errors are not scars — they are "
    "the computer telling you exactly what it could not do. The single most "
    "useful habit today is to **read the last line first**. Here we ask for a "
    "variable name that does not exist:"
)
code("print(plate_wellss)", role="wedo", raises=True,
     hint="ask Python for a variable name we never made (a deliberate typo)")

md(
    "Read the traceback from the **bottom up**. The last line says "
    "`NameError: name 'plate_wellss' is not defined`. `NameError` means *I have "
    "never heard of that name*. We simply misspelled `plate_wells`. The fix:"
)
code("print(plate_wells)", role="wedo", hint="spell the variable name correctly")

# =========================================================================
# BLOCK 3 — DATA IN
# =========================================================================
md(
    "## Getting data in\n"
    "\n"
    "This block is roughly 80% of everything you will ever do with data. First, "
    "properly: a **DataFrame** is just a table — rows and columns, like an Excel "
    "sheet. Each column behaves like the lists you met earlier, only with a "
    "name. `pd.read_csv(...)` loads one CSV file into a DataFrame; we load "
    "**one** file first, so we can look at it slowly.",
    section="Getting data in", minutes=25,
)
code(
    'jan = pd.read_csv(f"{DATA_BASE_URL}/results_2025_01.csv")\n'
    "jan.head()",
    role="wedo", hint="read January into a DataFrame and show the first rows",
)

md(
    "`.head()` shows the first five rows. Two more everyday questions: how big "
    "is the table, and what kind of value is in each column?"
)
code('print("rows, columns:", jan.shape)',
     role="wedo", hint="print the number of rows and columns")

md(
    "`.dtypes` lists the type of each column. `float64` means decimal numbers, "
    "`int64` whole numbers, `object` usually means text. Watch **`absorbance`** "
    "— it is a measurement, so we expect a number, but it comes in as `object`. "
    "That is a clue that something non-numeric is hiding in it."
)
code("jan.dtypes", role="ido", hint="show the type of every column")

md(
    "`.describe()` gives quick statistics for the number columns — count, mean, "
    "min, max. Notice `absorbance` is **missing** from this summary: pandas will "
    "not do statistics on a column it thinks is text. We will fix that shortly."
)
code("jan.describe()", role="ido", hint="summary statistics for the numeric columns")

md("To look at a single column, name it in square brackets:")
code('jan["ph"].head()', role="wedo", hint="show just the pH column")

md(
    "For several columns, pass a **list** of names — that is why there are two "
    "sets of brackets: the outer selects, the inner is the list."
)
code(
    'jan[["sample_id", "ph"]].head()',
    role="youdo",
    youdo='add a third column name to the list, e.g. "treatment", and rerun.',
)

md(
    "**Filtering** keeps only the rows that match a condition. The part inside "
    "the brackets, `jan[\"ph\"] > 7.5`, is a true/false test for every row; "
    "pandas keeps the true ones."
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
    "The second error you will hit constantly: asking for a column name that is "
    "not exactly right. pandas is **case-sensitive** — `ph` and `PH` are "
    "different. Watch:"
)
code('jan["PH"].head()', role="wedo", raises=True,
     hint="ask for a column using the wrong capitalisation (on purpose)")

md(
    "Last line: `KeyError: 'PH'`. A `KeyError` means *that column name is not in "
    "the table*. Ninety percent of the time it is a typo or the wrong "
    "capitalisation. The column is `ph`, lower-case:"
)
code('jan["ph"].head()', role="wedo", hint="use the exact column name, lower-case")

md(
    "Now the cleaning. `absorbance` loaded as text because a few cells contain "
    "`n.d.` (*not detected*) and a few are blank. `pd.to_numeric(..., "
    "errors=\"coerce\")` turns the column into real numbers and quietly replaces "
    "anything it cannot convert with `NaN` (*not a number*, pandas' word for "
    "missing). One line fixes the whole column:"
)
code(
    'jan["absorbance"] = pd.to_numeric(jan["absorbance"], errors="coerce")\n'
    'print("new type:", jan["absorbance"].dtype)\n'
    'jan["absorbance"].describe()',
    role="wedo", hint="turn absorbance into real numbers, then summarise it",
)

md(
    "Second mess: the treatment labels. `.str.strip()` removes stray spaces and "
    "`.str.capitalize()` makes the casing consistent, so the three spellings of "
    "control collapse into one:"
)
code(
    'jan["treatment"] = jan["treatment"].str.strip().str.capitalize()\n'
    'jan["treatment"].value_counts()',
    role="wedo", hint="make every treatment label consistent, then recount",
)

md(
    "Third mess: every file has one completely empty row. `dropna(how=\"all\")` "
    "removes only the rows where *every* value is missing, leaving real data "
    "untouched:"
)
code(
    'jan = jan.dropna(how="all")\n'
    'print("rows after cleaning:", jan.shape[0])',
    role="wedo", hint="drop the fully-empty row and recount",
)

# =========================================================================
# BLOCK 4 — REPEATING YOURSELF
# =========================================================================
md(
    "## Doing it for all twelve files\n"
    "\n"
    "A **`for` loop** repeats the same steps once for each item in a list — no "
    "copy-paste. We build up to all twelve files in three small steps, so "
    "nothing stays a mystery.",
    section="Doing it for all twelve files", minutes=20,
)
md(
    "**Step 1** — watch the loop run on just three files. It prints one line "
    "each time it goes around, so you can *see* it repeat three times:"
)
code(
    'for month in ["01", "02", "03"]:\n'
    '    file_url = f"{DATA_BASE_URL}/results_2025_{month}.csv"\n'
    "    one_month = pd.read_csv(file_url)\n"
    '    print("month", month, "->", one_month.shape)',
    role="wedo", hint="loop over three files and print the size of each",
)
md(
    "**Step 2** — here are all twelve month labels in one list. We will loop "
    "over this instead of just three:"
)
code(
    'months = ["01", "02", "03", "04", "05", "06",\n'
    '          "07", "08", "09", "10", "11", "12"]\n'
    'print("we have", len(months), "months")',
    role="wedo", hint="make the list of twelve month labels",
)
md(
    "**Step 3** — the full run. Same loop, but now we also **tag** each file "
    "with its month and **append** it to the list, then `pd.concat` stacks all "
    "twelve into one table. This is the hook — and now you know every line:"
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
    "The same three fixes we did for January, now applied once to the whole "
    "year. One line each, and the entire dataset is clean:"
)
code(
    'year = year.dropna(how="all")\n'
    'year["absorbance"] = pd.to_numeric(year["absorbance"], errors="coerce")\n'
    'year["treatment"] = year["treatment"].str.strip().str.capitalize()\n'
    "year.dtypes",
    role="ido",
)

md(
    "**`groupby`** is the loop you do not have to write. It splits the table "
    "into groups, computes one number per group, and hands back a tidy summary. "
    "Average absorbance for each treatment, in one line:"
)
code(
    'year.groupby("treatment")["absorbance"].mean()',
    role="wedo", hint="average absorbance for each treatment",
)

md("Swap `.mean()` for `.count()` to ask how many samples are in each group:")
code(
    'year.groupby("treatment")["absorbance"].count()',
    role="youdo",
    youdo="you just saw .mean(). Change .count() to .max() and rerun — what does it tell you?",
)

md(
    "Group by `month` instead, and we get the average for every month of the "
    "year — a twelve-row table that is begging to be a plot:"
)
code(
    'monthly_mean = year.groupby("month")["absorbance"].mean()\n'
    "monthly_mean",
    role="wedo", hint="average absorbance for each month",
)

# =========================================================================
# BLOCK 5 — ONE PLOT
# =========================================================================
md(
    "## One picture worth keeping\n"
    "\n"
    "Our `monthly_mean` table has two parts: `.index` (the labels — here the "
    "months) and `.values` (the numbers — the averages). `plt.plot` needs both, "
    "one for each axis. Always label the axes and give the plot a title — an "
    "unlabelled plot is useless to a reader. `plt.savefig` writes it to an image "
    "file you could drop straight into a paper or a slide.",
    section="One picture", minutes=15,
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
    "A different question — how do the two treatments compare overall? — wants a "
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
# CLOSING
# =========================================================================
md(
    "## Your turn\n"
    "\n"
    "**What you can now do**, and could not an hour ago: open a data file, "
    "combine many of them, clean the three everyday messes, summarise with "
    "`groupby`, and draw a labelled plot. That is a real chunk of a research "
    "workflow.\n"
    "\n"
    "**What to try in the homework** (on *your own* data file):\n"
    "\n"
    "- Read your file with `pd.read_csv` and run `.head()`, `.shape`, `.dtypes`\n"
    "- Find one column that loaded as `object` but should be a number, and fix it\n"
    "- Filter to a subset of rows that matters to you, and count them\n"
    "- Use `groupby` to get one number per group\n"
    "- Draw one labelled plot and save it as a PNG\n"
    "- For every answer, write one sentence: *how did you check it was right?*\n"
    "\n"
    "Bring the notebook — working or broken — to next session. A broken cell "
    "with its error message is exactly what we want to look at together.",
    section="Your turn", minutes=5,
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
    "“write from scratch.” When you fall behind, cut *content*, never the "
    "error-reading or the students’ own typing time.\n"
    "\n"
    "## Cell roles (printed as a comment at the top of every code cell)\n"
    "- **`# I DO`** — you type or run it, students **watch**. Setup and long "
    "cells. Move fast, narrate.\n"
    "- **`# WE DO`** — **everyone types it now.** Say “type this,” then go "
    "quiet ~90 seconds. Checkpoint before moving on.\n"
    "- **`# YOU DO`** — students **change one thing** in working code. This is "
    "the real target skill; fast finishers try more variations.\n"
    "\n"
    "## Say this out loud in the first 5 minutes\n"
    "> “If you ever fall behind typing, open **01_complete** (the answer "
    "notebook), run down to where we are, and rejoin. That is allowed and "
    "encouraged. Nobody gets stuck.”\n"
    "\n"
    "## Timing — markers are in the notebook, total 90 min\n"
    "\n"
    "| Section | Min | If you’re behind, cut… |\n"
    "|---|---|---|\n"
    "| The hook | 10 | nothing — this sells the whole course |\n"
    "| Notebook mechanics | 15 | the list cell; keep **both** break-it cells |\n"
    "| Getting data in | 25 | the two-column select (YOU DO) |\n"
    "| All 12 files | 20 | already an I DO — just run it, don’t linger |\n"
    "| One picture | 15 | the bar chart (YOU DO); keep the line plot |\n"
    "| Your turn | 5 | never — this is the homework handoff |\n"
    "\n"
    "## Room mechanics\n"
    "- **Checkpoint, don’t wait per cell.** Run 2–3 `I DO` cells, then pause "
    "on a `WE DO`.\n"
    "- **“Thumbs up when your cell ran”** — read the room in 3 seconds "
    "instead of asking aloud.\n"
    "- **Pair fast + slow**; one types, one reads the code aloud and checks the "
    "output. Swap each section.\n"
    "- **Recruit 2 fast finishers as floating helpers** after the first 30 min.\n"
    "- **Break-it-on-purpose cells: slow down.** Trigger the error, let it sit, "
    "read the **last line first**, out loud.\n"
    "\n"
    "## Pre-class checklist (do before the room fills)\n"
    "- [ ] Ran through this live notebook once, out loud, with a timer\n"
    "- [ ] Opened the data URL on classroom Wi-Fi **and** a phone hotspot\n"
    "- [ ] Offline zip of notebook + data on a USB stick as backup\n"
    "- [ ] `01_complete` open in a second tab as your answer key\n"
    "- [ ] Two bonus prompts ready for whoever finishes early\n"
    "\n"
    "## Dialing the typing load\n"
    "Default split is about **two-thirds WE DO** (type), **10% YOU DO** "
    "(modify), the rest **I DO** (watch). To change it, edit the `role=` on a "
    "cell in "
    "`build_session1.py` and rerun it:\n"
    "- More confident typing live? Turn some `I DO` into `WE DO`.\n"
    "- Want them typing less? Turn some `WE DO` into `I DO` or `YOU DO`."
)

STUDENT_LEGEND = (
    "## How to follow along\n"
    "\n"
    "Every code cell starts with a comment telling you what to do:\n"
    "\n"
    "- **`# I DO`** — just watch; I’ll type or run it.\n"
    "- **`# WE DO`** — everyone type it now, then run it (**Shift + Enter**).\n"
    "- **`# YOU DO`** — change the one thing I point to, then run it.\n"
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
    elif role == "demo":
        src = "# I DO — watch me type this live:\n# " + c["hint"]
    elif role == "ido":
        src = "# I DO — I'll run this, just watch:\n" + c["src"]
    elif role == "youdo":
        src = "# YOU DO — change one thing: " + c["youdo"] + "\n" + c["src"]
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
    # cockpit first, then the welcome cell, then the student legend, then the rest
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
        complete, timeout=120, kernel_name="python3",
        resources={"metadata": {"path": "/tmp"}},
    )
    client.execute()
    nbformat.write(complete, HERE / "01_complete.ipynb")

    nbformat.write(build_live(), HERE / "01_live.ipynb")

    code_cells = [c for c in CELLS if c["kind"] == "code"]
    n = len(code_cells)
    counts = {r: sum(1 for c in code_cells if c["role"] == r)
              for r in ("ido", "demo", "wedo", "youdo")}
    total_min = sum(c["minutes"] for c in CELLS if c.get("minutes"))
    print(f"cells: {len(CELLS)} total, {n} code, {len(CELLS) - n} markdown")
    print(f"roles: WE DO {counts['wedo']} ({round(100*counts['wedo']/n)}%) | "
          f"YOU DO {counts['youdo']} | I DO {counts['ido'] + counts['demo']} "
          f"(incl. {counts['demo']} live-typed hook)")
    print(f"pacing markers sum to: {total_min} min")


if __name__ == "__main__":
    main()
