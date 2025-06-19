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

        # Unique Code (was: Random Seed): Integer for reproducible randomization (use any number, or change for a new randomization)
        tk.Label(frm, text="Unique Code").grid(row=5, column=0, sticky="e")
        self.seed_var = tk.StringVar(value="42")
        seed_entry = tk.Entry(frm, textvariable=self.seed_var, width=8)
        seed_entry.grid(row=5, column=1)
        seed_entry.bind("<Enter>", lambda e: self.show_tooltip("A number to ensure a unique, repeatable randomization. Use any number; change for a new layout."))
        seed_entry.bind("<Leave>", lambda e: self.hide_tooltip())

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
            fg="black",
            width=15,
        )
        self.run_btn.grid(row=7, column=0, columnspan=3, pady=10)
        # --- FEEDBACK ---
        self.status = tk.Label(frm, text="", fg="blue")
        self.status.grid(row=8, column=0, columnspan=3)

        # Suggest Field Size Button
        tk.Button(
            frm,
            text="Suggest Field Size",
            command=self.suggest_field_size,
            bg="#2196F3",
            fg="black",
        ).grid(row=9, column=0, columnspan=3, pady=(5, 0))

        # Add tooltips to all fields
        for widget, tip in [
            (frm.grid_slaves(row=0, column=1)[0], "Total length of the field in inches (horizontal, along the rows)."),
            (frm.grid_slaves(row=1, column=1)[0], "Total width of the field in inches (vertical, across the rows)."),
            (frm.grid_slaves(row=2, column=1)[0], "Distance between plots within a row (inches)."),
            (frm.grid_slaves(row=3, column=1)[0], "Distance between rows (inches)."),
            (frm.grid_slaves(row=4, column=1)[0], "Comma-separated list of treatment codes and their replicate counts. Example: A:40,B:40,C:40"),
            (frm.grid_slaves(row=6, column=1)[0], "Path to save the Excel file. Defaults to your Desktop."),
        ]:
            widget.bind("<Enter>", lambda e, t=tip: self.show_tooltip(t))
            widget.bind("<Leave>", lambda e: self.hide_tooltip())

        # Tooltip label
        self.tooltip = tk.Label(frm, text="", bg="#ffffe0", fg="black", relief="solid", borderwidth=1, wraplength=300)
        self.tooltip.place_forget()

    def show_tooltip(self, text):
        self.tooltip.config(text=text)
        self.tooltip.place(relx=0, rely=1, anchor="sw")

    def hide_tooltip(self):
        self.tooltip.place_forget()

    def browse_file(self):
        f = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel files", ".xlsx")]
        )
        if f:
            self.outfile_var.set(f)

    def suggest_field_size(self):
        try:
            in_row_spacing = float(self.inrow_var.get())
            between_row_spacing = float(self.between_var.get())
            treatments = {}
            for pair in self.treat_var.get().split(","):
                code, reps = pair.split(":")
                treatments[code.strip()] = int(reps.strip())
            total_reps = sum(treatments.values())
            # Try to keep field width fixed, adjust length
            field_wid_in = float(self.wid_var.get())
            rows = int(round(field_wid_in / between_row_spacing))
            if rows == 0:
                raise ValueError("Field width or between-row spacing too small.")
            cols = int(np.ceil(total_reps / rows))
            new_field_len = cols * in_row_spacing
            self.len_var.set(str(round(new_field_len, 2)))
            self.status.config(
                text=f"Adjusted field length to {round(new_field_len,2)} in to fit {total_reps} plots.",
                fg="blue",
            )
        except Exception as e:
            self.status.config(text=f"Suggest error: {e}", fg="red")

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
            rows = int(round(field_wid_in / between_row_spacing))
            cols = int(round(field_len_in / in_row_spacing))
            plots = rows * cols
            total_reps = sum(treatments.values())
            if total_reps != plots:
                msg = (
                    f"Number of plots (rows x cols = {rows} x {cols} = {plots}) does not match total treatment replicates ({total_reps}).\n"
                    f"You can click 'Suggest Field Size' to auto-adjust the field length, or adjust your treatments/spacing."
                )
                self.status.config(text=msg, fg="red")
                messagebox.showerror("Mismatch", msg)
                return
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
