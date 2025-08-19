import argparse
import os
from pathlib import Path

def rename_files(directory: Path) -> None:
    """
    Renames files in a directory by replacing the prefix 'report_' with 'summary_'.

    Args:
        directory: The path to the directory containing the files.
    """
    # Find all .txt files in the specified directory
    for file_path in directory.glob('*.txt'):
        if file_path.is_file() and file_path.name.startswith('report_'):
            # Construct the new file name
            new_name = file_path.name.replace('report_', 'summary_', 1)
            new_file_path = file_path.with_name(new_name)

            # Rename the file
            os.rename(file_path, new_file_path)

            # Print the renaming information
            print(f"Renamed: '{file_path.name}' to '{new_name}'")

def main():
    """
    Parses command-line arguments and initiates the file renaming process.
    """
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Rename files in a directory.")
    parser.add_argument("directory", type=str, help="The path to the directory.")

    args = parser.parse_args()

    # Convert the directory string to a Path object
    directory_path = Path(args.directory)

    # Check if the directory exists
    if not directory_path.is_dir():
        print(f"Error: Directory not found at '{directory_path}'")
        return

    rename_files(directory_path)

if __name__ == "__main__":
    main()
