import os
import shutil
import pandas as pd
from pathlib import Path

def rename_audio_files(csv_path, input_dir=None, output_dir=None):
    """
    Renames audio files according to their start date in the CSV.
    
    Parameters
    ----------
    csv_path : str or Path
        Path to the CSV file containing 'File name ' and ' Start date ' columns.
    input_dir : str or Path, optional
        Folder containing the original audio files. Defaults to './input'.
    output_dir : str or Path, optional
        Folder where renamed files will be saved. Defaults to './output'.
    """

    # Set default folders
    input_dir = Path(input_dir or Path.cwd() / "input")
    output_dir = Path(output_dir or Path.cwd() / "output")

    # Create output directory if not exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load CSV
    df = pd.read_csv(csv_path)

    # Clean column names (trim whitespace)
    df.columns = [col.strip() for col in df.columns]
    
    # Check required columns
    if "File name" not in df.columns or "Start date" not in df.columns:
        raise ValueError("CSV must contain 'File name' and 'Start date' columns.")

    # Iterate through rows
    for _, row in df.iterrows():
        original_name = str(row["File name"]).strip()
        start_date = str(row["Start date"]).strip()

        try:
            # Convert to datetime object
            dt = pd.to_datetime(start_date)
            new_name = dt.strftime("%Y%m%d_%H%M%S") + ".WAV"

            src = input_dir / original_name
            dst = output_dir / new_name

            if src.exists():
                shutil.copy2(src, dst)
                print(f"✔ Renamed: {original_name} → {new_name}")
            else:
                print(f"⚠ File not found: {src}")

        except Exception as e:
            print(f"❌ Error processing {original_name}: {e}")

    print(f"\n✅ Done! Renamed files saved in: {output_dir}")

if __name__ == "__main__":
    # Example usage
    csv_file = "OsloWaveTankAuralHydrophone_2025-11-05.csv"

    input_dir = None
    output_dir = None
    rename_audio_files(csv_file, input_dir, output_dir)
