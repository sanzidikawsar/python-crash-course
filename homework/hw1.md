# Homework — After Session 1

**Read this once, then keep it open while you work.** In class you watched the
steps and understood them. That is the easy half. This homework is the other
half: your own fingers, your own data, your own mistakes to fix. Watching
someone drive is not the same as driving — this is where you actually learn.

Expect to get stuck. Getting stuck and then unstuck *is* the skill we are
building. Nobody is judging speed.

- **Time:** about 60–90 minutes. Do it in small pieces across the week, not in
  one long sitting.
- **The one rule:** for every task, write one sentence answering
  *"How did I check this was right?"* A cell that runs is not the same as an
  answer that is correct — and telling the difference is the whole point.
- **Due at Session 2:** bring your notebook, working or broken. At the start
  you will show **one** thing you did, for five minutes. A plot you made or an
  error you defeated — both are equally welcome.

Keep the class answer notebook open in another tab for reference:
<https://colab.research.google.com/github/sanzidikawsar/python-crash-course/blob/main/notebooks/01_complete.ipynb>

---

## Step 0 — Get set up (about 10 minutes)

1. Open [Google Colab](https://colab.research.google.com) and start a **New
   notebook** (menu: *File → New notebook*).
2. In the first cell, load the tools — the same two lines from class — and run
   it with **Shift + Enter**:
   ```python
   import pandas as pd
   import matplotlib.pyplot as plt
   ```
3. **Get your data into Colab.** Choose one:
   - **Your own file (preferred).** If your file is an Excel file, open it and
     do *File → Save As → CSV* first. Then in Colab click the **folder icon** on
     the left edge, click **Upload**, and pick your `.csv`. Load it:
     ```python
     mydata = pd.read_csv("your_file_name.csv")
     mydata.head()
     ```
   - **No file ready yet? Use the class data**, so you are never blocked:
     ```python
     mydata = pd.read_csv("https://raw.githubusercontent.com/sanzidikawsar/python-crash-course/main/data/session1/results_2025_01.csv")
     mydata.head()
     ```

> **The error you will most likely hit here is `FileNotFoundError`.** It means
> Python cannot find that file name. Check the name matches *exactly* what you
> see in the Files panel, including the `.csv` ending. Names are
> case-sensitive: `Data.csv` and `data.csv` are different files.

---

## Part A — Seven tasks on your own data

Do them in order; each is about ten minutes. After each one, add a **text cell**
(the *+ Text* button) with your *"how I checked"* sentence.

### Task 1 — Open and look
Read your file into a variable and run `.head()`.
- **Done when:** you can see the first rows of your own data as a table.
- **How to check:** does the number of columns match what you would see if you
  opened the file in Excel?

### Task 2 — How big, and what type is each column
Run `.shape`, then `.dtypes`.
- **Done when:** you can say how many rows and columns you have, and which
  columns are numbers (`int64` / `float64`) versus text (`object`).
- **How to check:** pick one column you *know* holds numbers. Did it load as a
  number? If it came in as `object`, write down which one — you will fix it in
  Task 4.

### Task 3 — Quick statistics
Run `.describe()`.
- **Done when:** you see count, mean, min, and max for your numeric columns.
- **How to check:** look at one `min` and one `max`. Are they physically
  possible for your measurement? A negative concentration, or a pH of 99, is a
  sign something is wrong upstream.

### Task 4 — Fix one messy column
Pick a column that *should* be numbers but loaded as `object`, and convert it:
```python
mydata["your_column"] = pd.to_numeric(mydata["your_column"], errors="coerce")
```
Or, if you have a text column with inconsistent labels (like `Control` /
`control` / `CONTROL`), tidy it:
```python
mydata["your_column"] = mydata["your_column"].str.strip().str.capitalize()
```
- **Done when:** the column's type changed to a number, or the labels are now
  consistent.
- **How to check:** run `.dtypes` (or `.value_counts()` for text) **before and
  after**, and compare the two.

### Task 5 — Filter to what matters to you
Choose a condition that means something in your work — rows above a threshold,
one treatment group, one date — keep only those rows, and count them:
```python
subset = mydata[mydata["your_column"] > some_value]
print("matching rows:", subset.shape[0])
```
- **Done when:** you have a smaller table and a count of its rows.
- **How to check:** eyeball a few rows of `subset.head()` — do they really meet
  your condition?

### Task 6 — Group and summarise
Pick a category column and a number column, and get one number per group:
```python
mydata.groupby("category_column")["number_column"].mean()
```
- **Done when:** you have a short summary — one row per group.
- **How to check:** swap `.mean()` for `.count()` and confirm the group counts
  add up to your total number of rows.

### Task 7 — One picture
Make one labelled plot and save it:
```python
plt.bar(summary.index, summary.values)   # or plt.plot(...)
plt.xlabel("...")
plt.ylabel("...")
plt.title("...")
plt.savefig("my_plot.png")
plt.show()
```
- **Done when:** you have a labelled plot saved as `my_plot.png`.
- **How to check:** does the shape of the plot match what you expected? If it
  surprises you, decide which it is — a real discovery, or a mistake to chase
  down.

---

## Part B — Break it on purpose (required, 5 minutes)

On purpose, ask for a column name that does not exist:
```python
mydata["THIS_IS_WRONG"]
```
Run it, then read the error **from the bottom line up**. Fix it by using a real
column name.

- **Submit to the group chat this week:** paste the **last line** of the error
  as **text** (not a screenshot), plus one sentence on what it meant and how you
  fixed it.
- **Why text, never a screenshot:** text can be pasted straight into a search
  box or an AI assistant, which means anyone can help you in seconds. A picture
  of an error helps no one.

---

## If you get stuck — the four errors you will actually meet

| The error says… | It means… | First thing to try |
|---|---|---|
| `FileNotFoundError` | Python can't find that file | Check the file name matches the Files panel exactly, `.csv` and all |
| `KeyError: 'X'` | That column name isn't in the table | Check spelling and capitalisation; run `mydata.columns` to see the real names |
| `NameError: name 'x'` | You used a name Python hasn't seen | Did you run the earlier cell that creates it? Check the spelling |
| `ModuleNotFoundError` | A tool isn't loaded | Re-run your first cell with the `import` lines |

Read the **last line first**, every time. The rest of the error is just the trail
of how Python got there.

---

## How to hand it in

- **This week:** post your Part B error-and-fix in the group chat (as text).
- **At Session 2:** bring your notebook — working or broken, both are fine — and
  be ready to show **one** thing for five minutes.

## Looking ahead to Session 2

Session 2 runs on your **own laptop**, not in Colab, so beforehand you will
install Python at home (Miniforge + Jupyter). A separate step-by-step guide is
coming in the group chat — start it early, and post any hiccup as text so we can
sort it out together before we meet. Nothing about that install can harm your
laptop or your files.
