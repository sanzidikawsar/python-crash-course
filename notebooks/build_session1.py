"""Single source of truth for the two Session-1 notebooks.

Every cell is defined ONCE below, then rendered two ways so the live skeleton
and the complete version are guaranteed identical in structure (CLAUDE.md
notebook rule 1):

  notebooks/01_complete.ipynb  full worked version, executed end-to-end
  notebooks/01_live.ipynb      skeleton: code the instructor types in class is
                               replaced with `# TYPE THIS TOGETHER: ...`, and
                               each section carries a `<!-- ~N min -->` pacing
                               marker.

Regenerate both:  python3 notebooks/build_session1.py

The complete notebook is executed here with a clean kernel; deliberate-error
cells are tagged `raises-exception` so their real traceback is captured as
output instead of halting the run. The Colab-only install cell is tagged
`skip-execution` so this local build does not pip-install anything.
"""

from pathlib import Path

import nbformat
from nbclient import NotebookClient

HERE = Path(__file__).resolve().parent
DATA_BASE_URL = (
    "https://raw.githubusercontent.com/sanzidikawsar/"
    "python-crash-course/main/data/session1"
)

# --- cell helpers ---------------------------------------------------------

CELLS = []


def md(src, section=None, minutes=None):
    CELLS.append({"kind": "md", "src": src, "section": section, "minutes": minutes})


def code(src, live=True, hint="", raises=False, skip=False):
    CELLS.append(
        {"kind": "code", "src": src, "live": live, "hint": hint,
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
    live=False, skip=True,
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
    live=False,
)

# =========================================================================
# BLOCK 1 — THE HOOK
# =========================================================================
md(
    "## The 30-minute Excel job, in six lines\n"
    "\n"
    "We have twelve files, one per month, named `results_2025_01.csv` up to "
    "`results_2025_12.csv`. In Excel you would open each, copy, paste, and pray. "
    "Watch what happens instead. Do not worry about understanding every word yet "
    "— we take it apart right after.",
    section="The hook", minutes=10,
)
code(
    "all_months = []\n"
    "for month in range(1, 13):\n"
    '    file_url = f"{DATA_BASE_URL}/results_2025_{month:02d}.csv"\n'
    "    all_months.append(pd.read_csv(file_url))\n"
    "\n"
    "year = pd.concat(all_months, ignore_index=True)\n"
    'print("Loaded", year.shape[0], "rows from 12 files")',
    hint="read all 12 files and stack them into one big table called `year`",
)

md("Here are the first rows of the whole year in one glance:")
code("year.head()", hint="peek at the top of the combined table")

md(
    "Now count how many rows belong to each treatment. Look closely at the "
    "result — something is already wrong, and spotting it is your first real "
    "data-cleaning instinct."
)
code(
    'year["treatment"].value_counts()',
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
    hint="make a number variable and print it",
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
    hint="store text in a variable and print it inside a sentence",
)

md(
    "Code can make a decision with **`if`**: the indented line runs only when "
    "the condition is true. A pH above 7.5 is slightly basic, so:"
)
code(
    "newest_ph = 7.6\n"
    "if newest_ph > 7.5:\n"
    '    print("this sample is slightly basic")',
    hint="print a message only if pH is above 7.5",
)

md(
    "A **list** is an ordered collection, written in square brackets. You reach "
    "an item by its position, and Python counts from **0**, so the first item is "
    "`[0]`. `len(...)` tells you how many items there are."
)
code(
    "months = [1, 2, 3, 4, 5, 6]\n"
    'print("first month:", months[0])\n'
    'print("how many:", len(months))',
    hint="make a list, grab the first item, count the items",
)

md(
    "### Break it on purpose\n"
    "\n"
    "We are going to cause an error on purpose. Errors are not scars — they are "
    "the computer telling you exactly what it could not do. The single most "
    "useful habit today is to **read the last line first**. Here we ask for a "
    "variable name that does not exist:"
)
code("print(monthss)", raises=True,
     hint="ask Python for a variable name we never made")

md(
    "Read the traceback from the **bottom up**. The last line says "
    "`NameError: name 'monthss' is not defined`. `NameError` means *I have never "
    "heard of that name*. We simply misspelled `months`. The fix:"
)
code("print(months)", hint="spell the variable name correctly")

# =========================================================================
# BLOCK 3 — DATA IN
# =========================================================================
md(
    "## Getting data in\n"
    "\n"
    "This block is roughly 80% of everything you will ever do with data. We load "
    "**one** file first, so we can look at it slowly. `pd.read_csv(...)` reads a "
    "CSV file into a **DataFrame** — think of it as one sheet of a spreadsheet "
    "that Python can work on.",
    section="Getting data in", minutes=25,
)
code(
    'jan = pd.read_csv(f"{DATA_BASE_URL}/results_2025_01.csv")\n'
    "jan.head()",
    hint="read January into a DataFrame and show the first rows",
)

md(
    "`.head()` shows the first five rows. Two more everyday questions: how big "
    "is the table, and what kind of value is in each column?"
)
code('print("rows, columns:", jan.shape)',
     hint="print the number of rows and columns")

md(
    "`.dtypes` lists the type of each column. `float64` means decimal numbers, "
    "`int64` whole numbers, `object` usually means text. Watch **`absorbance`** "
    "— it is a measurement, so we expect a number, but it comes in as `object`. "
    "That is a clue that something non-numeric is hiding in it."
)
code("jan.dtypes", hint="show the type of every column")

md(
    "`.describe()` gives quick statistics for the number columns — count, mean, "
    "min, max. Notice `absorbance` is **missing** from this summary: pandas will "
    "not do statistics on a column it thinks is text. We will fix that shortly."
)
code("jan.describe()", hint="summary statistics for the numeric columns")

md("To look at a single column, name it in square brackets:")
code('jan["ph"].head()', hint="show just the pH column")

md(
    "For several columns, pass a **list** of names — that is why there are two "
    "sets of brackets: the outer selects, the inner is the list."
)
code('jan[["sample_id", "ph"]].head()', hint="show two columns side by side")

md(
    "**Filtering** keeps only the rows that match a condition. The part inside "
    "the brackets, `jan[\"ph\"] > 7.5`, is a true/false test for every row; "
    "pandas keeps the true ones."
)
code(
    'high_ph = jan[jan["ph"] > 7.5]\n'
    'print("high-pH rows:", high_ph.shape[0])\n'
    "high_ph.head()",
    hint="keep only the rows where pH is above 7.5",
)

md(
    "### Break it on purpose\n"
    "\n"
    "The second error you will hit constantly: asking for a column name that is "
    "not exactly right. pandas is **case-sensitive** — `ph` and `PH` are "
    "different. Watch:"
)
code('jan["PH"].head()', raises=True,
     hint="ask for a column using the wrong capitalisation")

md(
    "Last line: `KeyError: 'PH'`. A `KeyError` means *that column name is not in "
    "the table*. Ninety percent of the time it is a typo or the wrong "
    "capitalisation. The column is `ph`, lower-case:"
)
code('jan["ph"].head()', hint="use the exact column name, lower-case")

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
    hint="turn absorbance into real numbers, then summarise it",
)

md(
    "Second mess: the treatment labels. `.str.strip()` removes stray spaces and "
    "`.str.capitalize()` makes the casing consistent, so the three spellings of "
    "control collapse into one:"
)
code(
    'jan["treatment"] = jan["treatment"].str.strip().str.capitalize()\n'
    'jan["treatment"].value_counts()',
    hint="make every treatment label consistent, then recount",
)

md(
    "Third mess: every file has one completely empty row. `dropna(how=\"all\")` "
    "removes only the rows where *every* value is missing, leaving real data "
    "untouched:"
)
code(
    'jan = jan.dropna(how="all")\n'
    'print("rows after cleaning:", jan.shape[0])',
    hint="drop the fully-empty row and recount",
)

# =========================================================================
# BLOCK 4 — REPEATING YOURSELF
# =========================================================================
md(
    "## Doing it for all twelve files\n"
    "\n"
    "A **`for` loop** repeats the same steps for each item in a list. `range(1, "
    "13)` gives the numbers 1 through 12. Each time around we build that month's "
    "file name, read it, tag it with its month number, and add it to a growing "
    "list. At the end, `pd.concat` stacks them into one table. This is the loop "
    "from the hook — now you know every line.",
    section="Doing it for all twelve files", minutes=20,
)
code(
    "all_months = []\n"
    "for month in range(1, 13):\n"
    '    file_url = f"{DATA_BASE_URL}/results_2025_{month:02d}.csv"\n'
    "    monthly = pd.read_csv(file_url)\n"
    '    monthly["month"] = month\n'
    "    all_months.append(monthly)\n"
    "\n"
    "year = pd.concat(all_months, ignore_index=True)\n"
    'print("total rows:", year.shape[0])',
    live=False,
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
    live=False,
)

md(
    "**`groupby`** is the loop you do not have to write. It splits the table "
    "into groups, computes one number per group, and hands back a tidy summary. "
    "Average absorbance for each treatment, in one line:"
)
code(
    'year.groupby("treatment")["absorbance"].mean()',
    hint="average absorbance for each treatment",
)

md("Swap `.mean()` for `.count()` to ask how many samples are in each group:")
code(
    'year.groupby("treatment")["absorbance"].count()',
    hint="count the samples in each treatment",
)

md(
    "Group by `month` instead, and we get the average for every month of the "
    "year — a twelve-row table that is begging to be a plot:"
)
code(
    'monthly_mean = year.groupby("month")["absorbance"].mean()\n'
    "monthly_mean",
    hint="average absorbance for each month",
)

# =========================================================================
# BLOCK 5 — ONE PLOT
# =========================================================================
md(
    "## One picture worth keeping\n"
    "\n"
    "`plt.plot` draws the monthly averages as a line. Always label the axes and "
    "give the plot a title — an unlabelled plot is useless to a reader. "
    "`plt.savefig` writes it to an image file you could drop straight into a "
    "paper or a slide.",
    section="One picture", minutes=15,
)
code(
    'plt.plot(monthly_mean.index, monthly_mean.values, marker="o")\n'
    'plt.xlabel("Month")\n'
    'plt.ylabel("Mean absorbance")\n'
    'plt.title("Average absorbance by month, 2025")\n'
    'plt.savefig("absorbance_by_month.png", dpi=150)\n'
    "plt.show()",
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
    hint="draw a bar chart comparing the two treatments",
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


# --- rendering ------------------------------------------------------------

def build_complete():
    nb = nbformat.v4.new_notebook()
    cells = []
    for c in CELLS:
        if c["kind"] == "md":
            cells.append(nbformat.v4.new_markdown_cell(c["src"]))
        else:
            tags = []
            if c["raises"]:
                tags.append("raises-exception")
            if c["skip"]:
                tags.append("skip-execution")
            meta = {"tags": tags} if tags else {}
            cells.append(nbformat.v4.new_code_cell(c["src"], metadata=meta))
    nb.cells = cells
    nb.metadata["language_info"] = {"name": "python"}
    return nb


def build_live():
    nb = nbformat.v4.new_notebook()
    cells = []
    for c in CELLS:
        if c["kind"] == "md":
            src = c["src"]
            if c["minutes"] is not None:
                src = f"<!-- ~{c['minutes']} min -->\n\n" + src
            cells.append(nbformat.v4.new_markdown_cell(src))
        else:
            tags = []
            if c["raises"]:
                tags.append("raises-exception")
            if c["skip"]:
                tags.append("skip-execution")
            meta = {"tags": tags} if tags else {}
            if c["live"]:
                src = "# TYPE THIS TOGETHER: " + c["hint"]
            else:
                src = c["src"]
            cells.append(nbformat.v4.new_code_cell(src, metadata=meta))
    nb.cells = cells
    nb.metadata["language_info"] = {"name": "python"}
    return nb


def main():
    complete = build_complete()
    # Execute with a clean kernel; run from /tmp so the saved PNG does not
    # land in the repo. Deliberate-error cells are tagged raises-exception.
    client = NotebookClient(
        complete, timeout=120, kernel_name="python3",
        resources={"metadata": {"path": "/tmp"}},
    )
    client.execute()
    nbformat.write(complete, HERE / "01_complete.ipynb")

    live = build_live()
    nbformat.write(live, HERE / "01_live.ipynb")

    n_code = sum(1 for c in CELLS if c["kind"] == "code")
    n_live = sum(1 for c in CELLS if c["kind"] == "code" and c["live"])
    total_min = sum(c["minutes"] for c in CELLS if c.get("minutes"))
    print(f"cells: {len(CELLS)} total, {n_code} code, "
          f"{len(CELLS) - n_code} markdown")
    print(f"typed-live code cells: {n_live}/{n_code} "
          f"({round(100 * n_live / n_code)}%)")
    print(f"pacing markers sum to: {total_min} min")


if __name__ == "__main__":
    main()
