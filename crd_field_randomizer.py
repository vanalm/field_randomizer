import sys

import numpy as np
import pandas as pd

# --- 1.  INPUTS --------------------------------------------------------------
field_len_in, field_wid_in = 144, 42  # inches
in_row_spacing, between_row_spacing = 6, 8  # inches
treatments = {  # code : replicates (must sum to total plots)
    "A": 40,
    "B": 40,
    "C": 40,
}
rng_seed = 42  # change for a new randomisation
outfile = "field_map.xlsx"  # or .csv

# --- 2.  DERIVED GRID DIMENSIONS --------------------------------------------
rows = int(round(field_wid_in / between_row_spacing))  # 42 / 8  ≈ 5
cols = int(round(field_len_in / in_row_spacing))  # 144 / 6 = 24
plots = rows * cols  # 120

assert sum(treatments.values()) == plots, "Rep counts must sum to 120"

# --- 3.  RANDOMISE TREATMENTS -----------------------------------------------
rng = np.random.default_rng(rng_seed)
flat = np.fromiter(
    (code for code, reps in treatments.items() for _ in range(reps)),
    dtype="U10",  # up to 10-char codes
    count=plots,
)
rng.shuffle(flat)  # in-place Fisher–Yates

# --- 4.  BUILD FIELD MAP -----------------------------------------------------
field_map = pd.DataFrame(
    flat.reshape(rows, cols),  # 2-D grid
    index=[f"Row{i+1}" for i in range(rows)],
    columns=[f"Pos{j+1}" for j in range(cols)],
)

# --- 5.  OUTPUT --------------------------------------------------------------
field_map.to_excel(outfile)
print(f"Saved to {outfile}\n")
print(field_map.head())  # quick visual check

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Welcome to the CRD Field Randomizer!")
        try:
            field_len_in = float(input("Field length (in): "))
            field_wid_in = float(input("Field width (in): "))
            in_row_spacing = float(input("In-row spacing (in): "))
            between_row_spacing = float(input("Between-row spacing (in): "))
            treat_str = input("Treatments (e.g. A:40,B:40,C:40): ")
            treatments = {}
            for pair in treat_str.split(","):
                code, reps = pair.split(":")
                treatments[code.strip()] = int(reps.strip())
            rng_seed = int(input("Random seed (e.g. 42): "))
            outfile = input("Output file (e.g. field_map.xlsx): ")
        except Exception as e:
            print(f"Input error: {e}")
            sys.exit(1)
        rows = int(round(field_wid_in / between_row_spacing))
        cols = int(round(field_len_in / in_row_spacing))
        plots = rows * cols
        if sum(treatments.values()) != plots:
            print(f"Error: Rep counts must sum to {plots} (rows x cols)")
            sys.exit(1)
        rng = np.random.default_rng(rng_seed)
        flat = np.fromiter(
            (code for code, reps in treatments.items() for _ in range(reps)),
            dtype="U10",
            count=plots,
        )
        rng.shuffle(flat)
        field_map = pd.DataFrame(
            flat.reshape(rows, cols),
            index=[f"Row{i+1}" for i in range(rows)],
            columns=[f"Pos{j+1}" for j in range(cols)],
        )
        field_map.to_excel(outfile)
        print(f"Saved to {outfile}\n")
        print(field_map.head())
    else:
        rows = int(round(field_wid_in / between_row_spacing))
        cols = int(round(field_len_in / in_row_spacing))
        plots = rows * cols
        assert sum(treatments.values()) == plots, "Rep counts must sum to 120"
        rng = np.random.default_rng(rng_seed)
        flat = np.fromiter(
            (code for code, reps in treatments.items() for _ in range(reps)),
            dtype="U10",
            count=plots,
        )
        rng.shuffle(flat)
        field_map = pd.DataFrame(
            flat.reshape(rows, cols),
            index=[f"Row{i+1}" for i in range(rows)],
            columns=[f"Pos{j+1}" for j in range(cols)],
        )
        field_map.to_excel(outfile)
        print(f"Saved to {outfile}\n")
        print(field_map.head())
