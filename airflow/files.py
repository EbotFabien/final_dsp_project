import pandas as pd
import os

def split_csv(input_file, output_dir, chunk_size=100):
    """
    Splits a CSV file into multiple smaller files.

    Args:
        input_file (str): Path to the original CSV file.
        output_dir (str): Folder to save split files.
        chunk_size (int): Number of rows per chunk (default = 100).
    """

    # Make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Read CSV in chunks to avoid memory overload
    chunk_iter = pd.read_csv(input_file, chunksize=chunk_size)

    for i, chunk in enumerate(chunk_iter, start=1):
        output_path = os.path.join(output_dir, f"data_part_{i}.csv")
        chunk.to_csv(output_path, index=False)
        print(f"✅ Created: {output_path} ({len(chunk)} rows)")

    print("\n🎉 Splitting complete!")


if __name__ == "__main__":
    input_csv = "/Users/ebotfabien/Desktop/school/air_new/ParisHousing.csv"
    output_folder = "/Users/ebotfabien/Desktop/school/air_new/raw"

    split_csv(input_csv, output_folder, chunk_size=100)
