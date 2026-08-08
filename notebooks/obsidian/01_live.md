<!-- ~0 min -->

# Session 1 — Make the Computer Do Your Boring Work

Twelve months of lab results, twelve messy files. By hand in Excel this is an afternoon. We are going to do it in a few lines, live, together.

**By the end of this session you can:**

- Open a data file in Python and see what is inside it
- Combine many files into one table without copy-paste
- Clean the three messes that show up in almost every real dataset
- Summarise a whole year with one line, and draw a plot you could put in a paper
- Read an error message instead of fearing it

You will not write programs from scratch today. The goal is to *read, run, and safely change* code — the skills you actually need on Monday.

## Setup (Google Colab only)

The cell below installs the two tools we use. **Run it first, before we start.** If Colab shows a *Restart* button after it finishes, click it — that is normal and only happens once. If you are not on Colab you can skip this cell.


```python
# Colab only. Run this first, before we start.
!pip install -q pandas==2.2.2 matplotlib==3.9.2
print("Libraries ready.")
```

## Load the tools

An **import** loads a toolbox someone else wrote. `pandas` is a spreadsheet that lives in Python; we nickname it `pd`. `matplotlib` draws charts; we nickname its drawing part `plt`. A **variable** is just a name we give to a value so we can reuse it — here `DATA_BASE_URL` holds the web address our data lives at, written once so we never retype it.


```python
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

DATA_BASE_URL = "https://raw.githubusercontent.com/sanzidikawsar/python-crash-course/main/data/session1"

print("pandas version:", pd.__version__)
```

<!-- ~10 min -->

## The 30-minute Excel job, in six lines

We have twelve files, one per month, named `results_2025_01.csv` up to `results_2025_12.csv`. In Excel you would open each, copy, paste, and pray. Watch what happens instead. Do not worry about understanding every word yet — we take it apart right after.


```python
# TYPE THIS TOGETHER: read all 12 files and stack them into one big table called `year`
```

Here are the first rows of the whole year in one glance:


```python
# TYPE THIS TOGETHER: peek at the top of the combined table
```

Now count how many rows belong to each treatment. Look closely at the result — something is already wrong, and spotting it is your first real data-cleaning instinct.


```python
# TYPE THIS TOGETHER: count rows per treatment — notice `Control` appears more than once
```

`Control`, `control`, and `CONTROL` are counted as three different things, even though they mean the same treatment. That is the kind of silent mess we will learn to fix. First, let's slow all the way down and understand what we just did.

<!-- ~15 min -->

## How a notebook works

A notebook is a stack of **cells**. A cell holds either text (like this one) or code. You run a code cell with **Shift + Enter**. The `[ ]` on the left becomes a number showing the order things ran in. Cells share memory: a variable made in one cell is available in the next. Run order matters — if you skip around, Python only knows what it has actually run.


```python
# TYPE THIS TOGETHER: make a number variable and print it
```

Values come in types. A **number** you can do maths with; a **string** is text, written inside quotes. The `f"..."` below is an *f-string* — Python swaps anything in `{ }` for its value, so we can mix text and variables in one printed line.


```python
# TYPE THIS TOGETHER: store text in a variable and print it inside a sentence
```

Code can make a decision with **`if`**: the indented line runs only when the condition is true. A pH above 7.5 is slightly basic, so:


```python
# TYPE THIS TOGETHER: print a message only if pH is above 7.5
```

A **list** is an ordered collection, written in square brackets. You reach an item by its position, and Python counts from **0**, so the first item is `[0]`. `len(...)` tells you how many items there are.


```python
# TYPE THIS TOGETHER: make a list, grab the first item, count the items
```

### Break it on purpose

We are going to cause an error on purpose. Errors are not scars — they are the computer telling you exactly what it could not do. The single most useful habit today is to **read the last line first**. Here we ask for a variable name that does not exist:


```python
# TYPE THIS TOGETHER: ask Python for a variable name we never made
```

Read the traceback from the **bottom up**. The last line says `NameError: name 'monthss' is not defined`. `NameError` means *I have never heard of that name*. We simply misspelled `months`. The fix:


```python
# TYPE THIS TOGETHER: spell the variable name correctly
```

<!-- ~25 min -->

## Getting data in

This block is roughly 80% of everything you will ever do with data. We load **one** file first, so we can look at it slowly. `pd.read_csv(...)` reads a CSV file into a **DataFrame** — think of it as one sheet of a spreadsheet that Python can work on.


```python
# TYPE THIS TOGETHER: read January into a DataFrame and show the first rows
```

`.head()` shows the first five rows. Two more everyday questions: how big is the table, and what kind of value is in each column?


```python
# TYPE THIS TOGETHER: print the number of rows and columns
```

`.dtypes` lists the type of each column. `float64` means decimal numbers, `int64` whole numbers, `object` usually means text. Watch **`absorbance`** — it is a measurement, so we expect a number, but it comes in as `object`. That is a clue that something non-numeric is hiding in it.


```python
# TYPE THIS TOGETHER: show the type of every column
```

`.describe()` gives quick statistics for the number columns — count, mean, min, max. Notice `absorbance` is **missing** from this summary: pandas will not do statistics on a column it thinks is text. We will fix that shortly.


```python
# TYPE THIS TOGETHER: summary statistics for the numeric columns
```

To look at a single column, name it in square brackets:


```python
# TYPE THIS TOGETHER: show just the pH column
```

For several columns, pass a **list** of names — that is why there are two sets of brackets: the outer selects, the inner is the list.


```python
# TYPE THIS TOGETHER: show two columns side by side
```

**Filtering** keeps only the rows that match a condition. The part inside the brackets, `jan["ph"] > 7.5`, is a true/false test for every row; pandas keeps the true ones.


```python
# TYPE THIS TOGETHER: keep only the rows where pH is above 7.5
```

### Break it on purpose

The second error you will hit constantly: asking for a column name that is not exactly right. pandas is **case-sensitive** — `ph` and `PH` are different. Watch:


```python
# TYPE THIS TOGETHER: ask for a column using the wrong capitalisation
```

Last line: `KeyError: 'PH'`. A `KeyError` means *that column name is not in the table*. Ninety percent of the time it is a typo or the wrong capitalisation. The column is `ph`, lower-case:


```python
# TYPE THIS TOGETHER: use the exact column name, lower-case
```

Now the cleaning. `absorbance` loaded as text because a few cells contain `n.d.` (*not detected*) and a few are blank. `pd.to_numeric(..., errors="coerce")` turns the column into real numbers and quietly replaces anything it cannot convert with `NaN` (*not a number*, pandas' word for missing). One line fixes the whole column:


```python
# TYPE THIS TOGETHER: turn absorbance into real numbers, then summarise it
```

Second mess: the treatment labels. `.str.strip()` removes stray spaces and `.str.capitalize()` makes the casing consistent, so the three spellings of control collapse into one:


```python
# TYPE THIS TOGETHER: make every treatment label consistent, then recount
```

Third mess: every file has one completely empty row. `dropna(how="all")` removes only the rows where *every* value is missing, leaving real data untouched:


```python
# TYPE THIS TOGETHER: drop the fully-empty row and recount
```

<!-- ~20 min -->

## Doing it for all twelve files

A **`for` loop** repeats the same steps for each item in a list. `range(1, 13)` gives the numbers 1 through 12. Each time around we build that month's file name, read it, tag it with its month number, and add it to a growing list. At the end, `pd.concat` stacks them into one table. This is the loop from the hook — now you know every line.


```python
all_months = []
for month in range(1, 13):
    file_url = f"{DATA_BASE_URL}/results_2025_{month:02d}.csv"
    monthly = pd.read_csv(file_url)
    monthly["month"] = month
    all_months.append(monthly)

year = pd.concat(all_months, ignore_index=True)
print("total rows:", year.shape[0])
```

The same three fixes we did for January, now applied once to the whole year. One line each, and the entire dataset is clean:


```python
year = year.dropna(how="all")
year["absorbance"] = pd.to_numeric(year["absorbance"], errors="coerce")
year["treatment"] = year["treatment"].str.strip().str.capitalize()
year.dtypes
```

**`groupby`** is the loop you do not have to write. It splits the table into groups, computes one number per group, and hands back a tidy summary. Average absorbance for each treatment, in one line:


```python
# TYPE THIS TOGETHER: average absorbance for each treatment
```

Swap `.mean()` for `.count()` to ask how many samples are in each group:


```python
# TYPE THIS TOGETHER: count the samples in each treatment
```

Group by `month` instead, and we get the average for every month of the year — a twelve-row table that is begging to be a plot:


```python
# TYPE THIS TOGETHER: average absorbance for each month
```

<!-- ~15 min -->

## One picture worth keeping

`plt.plot` draws the monthly averages as a line. Always label the axes and give the plot a title — an unlabelled plot is useless to a reader. `plt.savefig` writes it to an image file you could drop straight into a paper or a slide.


```python
# TYPE THIS TOGETHER: plot the monthly averages with labels, a title, and save it
```

A different question — how do the two treatments compare overall? — wants a different picture. `plt.bar` draws one bar per group:


```python
# TYPE THIS TOGETHER: draw a bar chart comparing the two treatments
```

<!-- ~5 min -->

## Your turn

**What you can now do**, and could not an hour ago: open a data file, combine many of them, clean the three everyday messes, summarise with `groupby`, and draw a labelled plot. That is a real chunk of a research workflow.

**What to try in the homework** (on *your own* data file):

- Read your file with `pd.read_csv` and run `.head()`, `.shape`, `.dtypes`
- Find one column that loaded as `object` but should be a number, and fix it
- Filter to a subset of rows that matters to you, and count them
- Use `groupby` to get one number per group
- Draw one labelled plot and save it as a PNG
- For every answer, write one sentence: *how did you check it was right?*

Bring the notebook — working or broken — to next session. A broken cell with its error message is exactly what we want to look at together.
