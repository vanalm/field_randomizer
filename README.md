# CRD Field Randomizer

A graphical tool for generating randomized field maps for Completely Randomized Design (CRD) experiments. Outputs an Excel file with the randomized layout.

## Features
- User-friendly GUI (no coding required)
- Supports custom field dimensions, spacing, treatments, and replicates
- Exports to Excel (.xlsx)
- Cross-platform: Windows and macOS

## How It Works
1. User enters field and treatment parameters in the GUI.
2. App calculates the number of plots and checks that treatment replicates match.
3. Treatments are randomly assigned to plots using a reproducible random seed.
4. The randomized field map is saved as an Excel file.

## Project Files

- `crd_field_randomizer_gui.py`: Main GUI application for randomizing field layouts and exporting to Excel.
- `crd_field_randomizer.py`: Console version of the randomizer (for advanced/CLI use).
- `requirements.txt`: List of required Python packages for building/running the app.
- `README.md`: Documentation and instructions (this file).
- `sample.csv.xlsx`: Example output file.
- `build/`, `dist/`: Build artifacts created by PyInstaller (not needed for source distribution).

## How Randomization and Seeds Work

This tool uses a pseudo-random number generator (PRNG) from NumPy (`numpy.random.default_rng`). The randomization process is controlled by a user-supplied **seed**:

- The **seed** is an integer that initializes the PRNG to a specific state.
- If you use the same seed and the same input parameters, you will get the exact same randomized field layout every time. This ensures full reproducibility for scientific and audit purposes.
- Changing the seed (or any input) will produce a different randomization.
- This is standard practice in scientific computing to allow experiments to be repeated and verified.

For more details on the NumPy PRNG used, see the official documentation: https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.default_rng

---

## Windows Installation & Usage
1. **Install Python**: Download from https://www.python.org/downloads/ (check "Add Python to PATH").
2. **Unzip project folder** and open Command Prompt in that folder:
   ```
   cd path\to\project_folder
   ```
3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   pip install pyinstaller
   ```
4. **Build the app**:
   ```
   pyinstaller --onefile --windowed crd_field_randomizer_gui.py
   ```
5. **Run the app**: Double-click `dist\crd_field_randomizer_gui.exe`.

## macOS Installation & Usage
1. **Install Python 3** (if needed): https://www.python.org/downloads/
2. **Open Terminal** and navigate to the project folder:
   ```
   cd /path/to/project_folder
   ```
3. **Install dependencies**:
   ```
   pip3 install -r requirements.txt
   pip3 install pyinstaller
   ```
4. **Build the app**:
   ```
   pyinstaller --onefile --windowed crd_field_randomizer_gui.py
   ```
5. **Run the app**: Double-click `dist/crd_field_randomizer_gui`.

---

## Notes for Auditors
- All dependencies are listed in `requirements.txt` and bundled via PyInstaller.
- The randomization logic is fully transparent in `crd_field_randomizer_gui.py`.
- The app uses `numpy` for randomization, `pandas` for data handling, and `openpyxl` for Excel export.
- The random seed ensures reproducibility.
- No data is sent outside the local machine.

## Extending/Customizing
- **Other Designs**: Logic can be adapted for RCBD, split-plot, etc.
- **Other Outputs**: CSV export, PDF map, or direct print.
- **Batch Runs**: Script can be modified for batch randomizations.
- **Integration**: Can be integrated with field hardware or data collection apps.

## Troubleshooting
- If you see `No module named 'openpyxl'`, ensure all dependencies are installed before building.
- For any issues, rerun the install and build steps.

## GUI Inputs Explained

- **Field Length (in):** Total length of the field in inches (horizontal, along the rows).
- **Field Width (in):** Total width of the field in inches (vertical, across the rows).
- **In-row Spacing (in):** Distance between plots within a row (inches).
- **Between-row Spacing (in):** Distance between rows (inches).
- **Treatments:** Comma-separated list of treatment codes and their replicate counts. Example: `A:40,B:40,C:40` means 40 plots of A, 40 of B, 40 of C. The sum must match the total number of plots (rows × columns).
- **Random Seed:** Integer for reproducible randomization. Use any number; change for a new randomization.
- **Output File:** Path to save the Excel file. Defaults to your Desktop. Use the "Browse..." button to select a location.

---

**How the GUI works:**
- The app calculates the number of rows and columns based on field size and spacing.
- It checks that the total number of treatment replicates matches the number of plots.
- Treatments are randomly assigned to plots using the seed.
- The randomized map is saved as an Excel file at the chosen location.

---

## What is the .spec file?

- The `.spec` file (e.g. `crd_field_randomizer_gui.spec`) is generated by PyInstaller when you build the app. It contains build instructions and configuration for PyInstaller, such as which script to bundle, what files to include, and how to package the output. You can edit this file for advanced customization, but for most users, it is auto-generated and can be ignored or deleted.

---

## Building a Windows .exe from macOS (Apple Silicon/M1/M2)

**Note:** Building a Windows `.exe` using Docker+Wine is not supported on Apple Silicon (M1/M2) Macs, even with Rosetta 2. You will see errors like `run_wineboot failed to start wineboot`. This is a known limitation.

**Recommended solutions:**

1. **Use a Windows VM or real Windows machine**
   - Use [UTM](https://mac.getutm.app/), [Parallels Desktop](https://www.parallels.com/), or [VirtualBox](https://www.virtualbox.org/) to run Windows on your Mac.
   - Build your `.exe` using PyInstaller inside the VM.

2. **Use GitHub Actions (cloud build)**
   - This repo includes a workflow that builds your `.exe` on every push to `main`.
   - Download the `.exe` from the GitHub Actions "Artifacts" tab after the build completes.

**How to remove Rosetta 2 (if you want to):**

Rosetta 2 is lightweight and safe to leave installed, but if you want to remove it:

```sh
sudo /usr/sbin/softwareupdate --remove-rosetta
```

---

For questions or improvements, contact the project maintainer.
