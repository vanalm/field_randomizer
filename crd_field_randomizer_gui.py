import os
import tkinter as tk

from tkinter import filedialog, messagebox

import numpy as np
import pandas as pd


# --- Core logic as a function ---
def randomize_field(
    field_len_in,
    field_wid_in,
    in_row_spacing,
    between_row_spacing,
    treatments,
    rng_seed,
    outfile,
):
    rows = int(round(field_wid_in / between_row_spacing))
    cols = int(round(field_len_in / in_row_spacing))
    plots = rows * cols
    if sum(treatments.values()) != plots:
        raise ValueError(f"Rep counts must sum to {plots} (rows x cols)")
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
    return field_map, outfile


# --- GUI ---
class FieldRandomizerApp:
    def __init__(self, root):
        self.root = root
        root.title("CRD Field Randomizer")
        self.make_widgets()

    def make_widgets(self):
        frm = tk.Frame(self.root, padx=10, pady=10)
        frm.pack()

        # --- FIELD DIMENSIONS ---

        # Field Length (in): Total length of the field in inches (horizontal, along the rows)
        tk.Label(frm, text="Field Length (in)").grid(row=0, column=0, sticky="e")
        self.len_var = tk.StringVar(value="144")
        tk.Entry(frm, textvariable=self.len_var, width=8).grid(row=0, column=1)

        # Field Width (in): Total width of the field in inches (vertical, across the rows)
        tk.Label(frm, text="Field Width (in)").grid(row=1, column=0, sticky="e")
        self.wid_var = tk.StringVar(value="42")
        tk.Entry(frm, textvariable=self.wid_var, width=8).grid(row=1, column=1)

        # --- PLOT SPACING ---

        # In-row Spacing (in): Distance between plots within a row (inches)
        tk.Label(frm, text="In-row Spacing (in)").grid(row=2, column=0, sticky="e")
        self.inrow_var = tk.StringVar(value="6")
        tk.Entry(frm, textvariable=self.inrow_var, width=8).grid(row=2, column=1)

        # Between-row Spacing (in): Distance between rows (inches)
        tk.Label(frm, text="Between-row Spacing (in)").grid(row=3, column=0, sticky="e")
        self.between_var = tk.StringVar(value="8")
        tk.Entry(frm, textvariable=self.between_var, width=8).grid(row=3, column=1)

        # --- TREATMENTS ---

        # Treatments: Comma-separated list of treatment codes and their replicate counts (e.g. A:40,B:40,C:40)
        tk.Label(frm, text="Treatments (e.g. A:40,B:40,C:40)").grid(
            row=4, column=0, sticky="e"
        )
        self.treat_var = tk.StringVar(value="A:40,B:40,C:40")
        tk.Entry(frm, textvariable=self.treat_var, width=20).grid(row=4, column=1)

        # --- RANDOM SEED ---

        # Random Seed: Integer for reproducible randomization (use any number, or change for a new randomization)

        tk.Label(frm, text="Random Seed").grid(row=5, column=0, sticky="e")
        self.seed_var = tk.StringVar(value="42")
        tk.Entry(frm, textvariable=self.seed_var, width=8).grid(row=5, column=1)

        # --- OUTPUT FILE ---

        # Output File: Path to save the Excel file (default: Desktop)
        tk.Label(frm, text="Output File").grid(row=6, column=0, sticky="e")
        default_outfile = os.path.join(
            os.path.expanduser("~"), "Desktop", "field_map.xlsx"
        )
        self.outfile_var = tk.StringVar(value=default_outfile)
        tk.Entry(frm, textvariable=self.outfile_var, width=20).grid(row=6, column=1)
        tk.Button(frm, text="Browse...", command=self.browse_file).grid(row=6, column=2)

        # --- RUN BUTTON ---
        self.run_btn = tk.Button(
            frm,
            text="Randomize!",
            command=self.run_randomizer,
            bg="#4CAF50",
            fg="white",
            width=15,
        )
        self.run_btn.grid(row=7, column=0, columnspan=3, pady=10)
        # --- FEEDBACK ---
        self.status = tk.Label(frm, text="", fg="blue")
        self.status.grid(row=8, column=0, columnspan=3)

    def browse_file(self):
        f = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel files", ".xlsx")]
        )
        if f:
            self.outfile_var.set(f)

    def run_randomizer(self):
        try:
            field_len_in = float(self.len_var.get())
            field_wid_in = float(self.wid_var.get())
            in_row_spacing = float(self.inrow_var.get())
            between_row_spacing = float(self.between_var.get())
            treatments = {}
            for pair in self.treat_var.get().split(","):
                code, reps = pair.split(":")
                treatments[code.strip()] = int(reps.strip())
            rng_seed = int(self.seed_var.get())
            outfile = self.outfile_var.get()
            field_map, outpath = randomize_field(
                field_len_in,
                field_wid_in,
                in_row_spacing,
                between_row_spacing,
                treatments,
                rng_seed,
                outfile,
            )
            self.status.config(text=f"Saved to {os.path.abspath(outpath)}", fg="green")
            messagebox.showinfo(
                "Success", f"Field map saved to:\n{os.path.abspath(outpath)}"
            )
        except Exception as e:
            self.status.config(text=f"Error: {e}", fg="red")
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = FieldRandomizerApp(root)
    root.mainloop()
