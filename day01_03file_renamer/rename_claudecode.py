#!/usr/bin/env python3
"""
File Renamer Script

This script renames files in a specified directory by replacing the 'report_' prefix 
with 'summary_' for all .txt files.
"""

import argparse
import os
from pathlib import Path
from typing import List, Tuple


def find_txt_files(directory: Path) -> List[Path]:
    """
    Find all .txt files in the specified directory.
    
    Args:
        directory: Path object representing the target directory
        
    Returns:
        List of Path objects for all .txt files found
    """
    return list(directory.glob("*.txt"))


def rename_files_with_prefix(directory: Path, old_prefix: str = "report_", new_prefix: str = "summary_") -> None:
    """
    Rename files by replacing the old prefix with the new prefix.
    
    Args:
        directory: Path object representing the target directory
        old_prefix: The prefix to be replaced (default: "report_")
        new_prefix: The prefix to replace with (default: "summary_")
    """
    # Find all .txt files in the directory
    txt_files = find_txt_files(directory)
    
    if not txt_files:
        print(f"No .txt files found in directory: {directory}")
        return
    
    renamed_count = 0
    
    # Process each .txt file
    for file_path in txt_files:
        filename = file_path.name
        
        # Check if the file has the target prefix
        if filename.startswith(old_prefix):
            # Create new filename by replacing the prefix
            new_filename = new_prefix + filename[len(old_prefix):]
            new_file_path = file_path.parent / new_filename
            
            try:
                # Rename the file
                file_path.rename(new_file_path)
                print(f"Renamed: '{filename}' -> '{new_filename}'")
                renamed_count += 1
            except OSError as e:
                print(f"Error renaming '{filename}': {e}")
    
    print(f"\nTotal files renamed: {renamed_count}")


def validate_directory(directory_path: str) -> Path:
    """
    Validate that the provided directory path exists and is accessible.
    
    Args:
        directory_path: String path to the directory
        
    Returns:
        Path object if valid
        
    Raises:
        argparse.ArgumentTypeError: If directory is invalid
    """
    path = Path(directory_path)
    
    if not path.exists():
        raise argparse.ArgumentTypeError(f"Directory does not exist: {directory_path}")
    
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"Path is not a directory: {directory_path}")
    
    return path


def main() -> None:
    """
    Main function to handle command-line arguments and execute the renaming process.
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Rename .txt files by replacing 'report_' prefix with 'summary_'"
    )
    
    parser.add_argument(
        "directory",
        type=validate_directory,
        help="Path to the directory containing files to rename"
    )
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    print(f"Processing directory: {args.directory}")
    print("Looking for .txt files with 'report_' prefix...")
    print("-" * 50)
    
    # Execute the renaming process
    rename_files_with_prefix(args.directory)


if __name__ == "__main__":
    main()