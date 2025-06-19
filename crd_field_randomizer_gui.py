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
        import threading

        self.tooltip_timer = None

        def add_tooltip(widget, text):
            def show_bubble(event=None):
                self.tooltip.config(text=text)
                self.tooltip.update_idletasks()
                # Default offset from cursor
                offset_x, offset_y = 16, 24
                if event:
                    x = event.x_root - self.root.winfo_rootx() + offset_x
                    y = event.y_root - self.root.winfo_rooty() + offset_y
                else:
                    # fallback: center below widget
                    x = (
                        widget.winfo_rootx()
                        - self.root.winfo_rootx()
                        + widget.winfo_width() // 2
                    )
                    y = (
                        widget.winfo_rooty()
                        - self.root.winfo_rooty()
                        + widget.winfo_height()
                        + 8
                    )
                # Clamp to window bounds
                max_x = self.root.winfo_width() - self.tooltip.winfo_reqwidth() - 10
                max_y = self.root.winfo_height() - self.tooltip.winfo_reqheight() - 10
                x = max(10, min(x, max_x))
                y = max(10, min(y, max_y))
                self.tooltip.place(x=x, y=y)
                self.tooltip.lift()

            def on_enter(event):
                def delayed_show():
                    self.tooltip_timer = None
                    show_bubble(event)

                self.tooltip_timer = self.root.after(2000, delayed_show)
                widget.bind("<Motion>", show_bubble, add="+")

            def on_leave(event):
                if self.tooltip_timer:
                    self.root.after_cancel(self.tooltip_timer)
                    self.tooltip_timer = None
                self.tooltip.place_forget()
                widget.unbind("<Motion>")

            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

        # Field Length (in)
        tk.Label(frm, text="Field Length (in)").grid(row=0, column=0, sticky="e")
        self.len_var = tk.StringVar(value="144")
        len_entry = tk.Entry(frm, textvariable=self.len_var, width=8)
        len_entry.grid(row=0, column=1)
        add_tooltip(
            len_entry,
            "Total length of the field in inches (horizontal, along the rows).",
        )

        # Field Width (in)
        tk.Label(frm, text="Field Width (in)").grid(row=1, column=0, sticky="e")
        self.wid_var = tk.StringVar(value="42")
        wid_entry = tk.Entry(frm, textvariable=self.wid_var, width=8)
        wid_entry.grid(row=1, column=1)
        add_tooltip(
            wid_entry,
            "Total width of the field in inches (vertical, across the rows).",
        )

        # In-row Spacing (in)
        tk.Label(frm, text="In-row Spacing (in)").grid(row=2, column=0, sticky="e")
        self.inrow_var = tk.StringVar(value="6")
        inrow_entry = tk.Entry(frm, textvariable=self.inrow_var, width=8)
        inrow_entry.grid(row=2, column=1)
        add_tooltip(inrow_entry, "Distance between plots within a row (inches).")

        # Between-row Spacing (in)
        tk.Label(frm, text="Between-row Spacing (in)").grid(row=3, column=0, sticky="e")
        self.between_var = tk.StringVar(value="8")
        between_entry = tk.Entry(frm, textvariable=self.between_var, width=8)
        between_entry.grid(row=3, column=1)
        add_tooltip(between_entry, "Distance between rows (inches).")

        # Treatments
        tk.Label(frm, text="Treatments (e.g. A:40,B:40,C:40)").grid(
            row=4, column=0, sticky="e"
        )
        self.treat_var = tk.StringVar(value="A:40,B:40,C:40")
        treat_entry = tk.Entry(frm, textvariable=self.treat_var, width=20)
        treat_entry.grid(row=4, column=1)
        add_tooltip(
            treat_entry,
            "Comma-separated list of treatment codes and their replicate counts. Example: A:40,B:40,C:40",
        )

        # Unique Code (was: Random Seed)
        tk.Label(frm, text="Unique Code").grid(row=5, column=0, sticky="e")
        self.seed_var = tk.StringVar(value="42")
        seed_entry = tk.Entry(frm, textvariable=self.seed_var, width=8)
        seed_entry.grid(row=5, column=1)
        add_tooltip(
            seed_entry,
            "A number to ensure a unique, repeatable randomization. Use any number; change for a new layout.",
        )

        # Output File
        tk.Label(frm, text="Output File").grid(row=6, column=0, sticky="e")
        default_outfile = os.path.join(
            os.path.expanduser("~"), "Desktop", "field_map.xlsx"
        )
        self.outfile_var = tk.StringVar(value=default_outfile)
        outfile_entry = tk.Entry(frm, textvariable=self.outfile_var, width=20)
        outfile_entry.grid(row=6, column=1)
        add_tooltip(
            outfile_entry,
            "Path to save the Excel file. Defaults to your Desktop.",
        )
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
        add_tooltip(
            self.run_btn,
            "Click to generate the randomized field map and save as Excel.",
        )

        # --- FEEDBACK ---
        self.status = tk.Label(frm, text="", fg="#3f8fff")
        self.status.grid(row=8, column=0, columnspan=3)

        # Suggest Field Size Button
        suggest_btn = tk.Button(
            frm,
            text="Suggest Field Size",
            command=self.suggest_field_size,
            bg="#2196F3",
            fg="black",
        )
        suggest_btn.grid(row=9, column=0, columnspan=3, pady=(5, 0))
        add_tooltip(
            suggest_btn,
            "Auto-adjust the field length to fit the number of treatments.",
        )

        # Tooltip label (single instance, hidden by default)
        self.tooltip = tk.Label(
            frm,
            text="",
            bg="#222",
            fg="#fff",
            relief="solid",
            borderwidth=1,
            wraplength=250,
            font=("Arial", 10, "normal"),
            padx=8,
            pady=4,
        )
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
