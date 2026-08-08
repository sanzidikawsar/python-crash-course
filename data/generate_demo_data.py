"""Generate the session-1 demo data: twelve messy monthly CSVs.

Reproducible: seeded with a single numpy Generator, so re-running this script
produces byte-identical files. Output goes to data/session1/.

This data is deliberately messy. Every defect below has a one-line pandas fix
that gets demonstrated in session 1 or HW1. Do not add mess with no teaching
payoff (see docs/course-design.md §8).

Deliberate defects, and the one-line fix each one teaches:

  1. Missing values in `absorbance` (empty cells)
       -> pd.to_numeric(df["absorbance"], errors="coerce")
  2. A non-numeric sentinel in `absorbance` so the column loads as `object`
       We use the string "n.d." (not detected), NOT "N/A".
       WHY: pandas' default read_csv treats "N/A" as NaN, which would make the
       column load as clean float64 and destroy this defect. "n.d." is not in
       pandas' default NA list, so absorbance genuinely loads as object.
       -> pd.to_numeric(df["absorbance"], errors="coerce")   (same one-liner as #1)
  3. Inconsistent capitalization in `treatment` (Control / control / CONTROL)
       -> df["treatment"].str.strip().str.capitalize()
  4. One fully blank row per file
       -> df.dropna(how="all")
  5. One file (July) has a trailing comma -> a phantom "Unnamed: 6" column
       -> df.loc[:, ~df.columns.str.startswith("Unnamed")]
  6. One file (March) writes `date` in a different format (DD/MM/YYYY)
       -> pd.to_datetime(df["date"], format="mixed", dayfirst=True)
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 12345
ROWS_PER_FILE = 80
OUT_DIR = Path(__file__).resolve().parent / "session1"

# Month that gets the trailing-comma / phantom-column defect, and the month
# that gets the odd date format. Kept as constants so the defects are findable.
TRAILING_COMMA_MONTH = 7   # July  -> results_2025_07.csv
ODD_DATE_MONTH = 3         # March -> results_2025_03.csv

# Messy casing variants injected into an otherwise-clean treatment label.
CASE_VARIANTS = {
    "Control": ["control", "CONTROL", "Control "],
    "Treated": ["treated", "TREATED", "treated "],
}


def build_month(rng: np.random.Generator, month: int) -> pd.DataFrame:
    """Build one month's DataFrame, with defects injected deterministically."""
    n = ROWS_PER_FILE

    sample_id = [f"S{month:02d}{i:03d}" for i in range(1, n + 1)]
    treatment = rng.choice(["Control", "Treated"], size=n).tolist()
    replicate = rng.integers(1, 4, size=n).tolist()

    # Realistic-looking absorbance and pH. absorbance starts as float; we then
    # poke string defects into it, which turns the column to object on write.
    absorbance = np.round(rng.uniform(0.08, 1.60, size=n), 3).astype(object)
    ph = np.round(rng.uniform(6.4, 7.9, size=n), 2)

    days = rng.integers(1, 29, size=n)
    date_fmt = "%d/%m/%Y" if month == ODD_DATE_MONTH else "%Y-%m-%d"
    date = [pd.Timestamp(2025, month, int(d)).strftime(date_fmt) for d in days]

    df = pd.DataFrame(
        {
            "sample_id": sample_id,
            "treatment": treatment,
            "replicate": replicate,
            "absorbance": absorbance,
            "ph": ph,
            "date": date,
        }
    )

    # Defect 3: messy capitalization in treatment (about 1 in 4 rows).
    n_messy = n // 4
    messy_rows = rng.choice(n, size=n_messy, replace=False)
    for r in messy_rows:
        base = df.at[r, "treatment"]
        df.at[r, "treatment"] = rng.choice(CASE_VARIANTS[base])

    # Defect 1: 4 genuinely-missing absorbance values (empty cells on write).
    missing_rows = rng.choice(n, size=4, replace=False)
    for r in missing_rows:
        df.at[r, "absorbance"] = np.nan

    # Defect 2: 4 "n.d." sentinels in absorbance -> column loads as object.
    remaining = [i for i in range(n) if i not in set(missing_rows)]
    nd_rows = rng.choice(remaining, size=4, replace=False)
    for r in nd_rows:
        df.at[r, "absorbance"] = "n.d."

    # Defect 4: one fully-blank row, inserted at a deterministic position.
    blank_at = int(rng.integers(1, n))
    blank = pd.DataFrame([{c: np.nan for c in df.columns}])
    df = pd.concat([df.iloc[:blank_at], blank, df.iloc[blank_at:]], ignore_index=True)

    return df


def write_month(df: pd.DataFrame, path: Path, month: int) -> None:
    """Write one month's CSV, applying the trailing-comma defect for July."""
    df.to_csv(path, index=False)

    # Defect 5: append a trailing comma to every line of the July file, which
    # makes read_csv invent an empty "Unnamed: 6" column.
    if month == TRAILING_COMMA_MONTH:
        lines = path.read_text().splitlines()
        path.write_text("\n".join(line + "," for line in lines) + "\n")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)

    for month in range(1, 13):
        df = build_month(rng, month)
        path = OUT_DIR / f"results_2025_{month:02d}.csv"
        write_month(df, path, month)
        print(f"wrote {path.name}  ({len(df)} rows)")

    print(f"\nDone. {len(list(OUT_DIR.glob('results_2025_*.csv')))} files in {OUT_DIR}")


if __name__ == "__main__":
    main()
