#!/usr/bin/env python3
"""
CSV to JSON Converter
A robust script for converting CSV files to JSON format following best practices.
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Union


def csv_to_dict_list(csv_content: str) -> List[Dict[str, str]]:
    """
    Convert CSV content string to a list of dictionaries.
    
    Args:
        csv_content: Raw CSV content as a string
        
    Returns:
        List of dictionaries where each dictionary represents a CSV row
        with column headers as keys
    """
    csv_reader = csv.DictReader(csv_content.strip().split('\n'))
    return [row for row in csv_reader]


def dict_list_to_json(data: List[Dict[str, str]], indent: int = 2) -> str:
    """
    Convert a list of dictionaries to JSON string.
    
    Args:
        data: List of dictionaries to convert
        indent: JSON indentation level for pretty printing
        
    Returns:
        JSON formatted string
    """
    return json.dumps(data, indent=indent, ensure_ascii=False)


def detect_and_convert_types(data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Detect and convert data types in dictionary values from strings to appropriate types.
    
    Args:
        data: List of dictionaries with string values
        
    Returns:
        List of dictionaries with properly typed values
    """
    if not data:
        return data
        
    converted_data = []
    
    for row in data:
        converted_row = {}
        for key, value in row.items():
            converted_row[key] = _convert_value(value)
        converted_data.append(converted_row)
    
    return converted_data


def _convert_value(value: str) -> Union[str, int, float, bool, None]:
    """
    Convert a string value to its most appropriate type.
    
    Args:
        value: String value to convert
        
    Returns:
        Converted value with appropriate type
    """
    if value is None or value.strip() == '':
        return None
    
    value = value.strip()
    
    # Boolean detection
    if value.lower() in ('true', 'false'):
        return value.lower() == 'true'
    
    # Integer detection
    try:
        if '.' not in value and 'e' not in value.lower():
            return int(value)
    except ValueError:
        pass
    
    # Float detection
    try:
        return float(value)
    except ValueError:
        pass
    
    # Return as string if no conversion possible
    return value


def read_csv_file(file_path: Path) -> str:
    """
    Read CSV file content with proper error handling.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        CSV file content as string
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        PermissionError: If there are insufficient permissions to read the file
        UnicodeDecodeError: If the file encoding is not supported
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied to read file: {file_path}")
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except UnicodeDecodeError:
            raise UnicodeDecodeError(
                f"Unable to decode file {file_path}. Please check file encoding."
            )


def write_json_file(json_content: str, file_path: Path) -> None:
    """
    Write JSON content to file with proper error handling.
    
    Args:
        json_content: JSON content as string
        file_path: Path where to write the JSON file
        
    Raises:
        PermissionError: If there are insufficient permissions to write the file
        OSError: If there are other OS-level issues writing the file
    """
    try:
        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json_content)
    except PermissionError:
        raise PermissionError(f"Permission denied to write file: {file_path}")
    except OSError as e:
        raise OSError(f"Error writing to file {file_path}: {e}")


def convert_csv_to_json(input_path: Path, output_path: Path) -> None:
    """
    Convert CSV file to JSON file with type detection.
    
    Args:
        input_path: Path to input CSV file
        output_path: Path to output JSON file
    """
    try:
        # Read CSV file
        csv_content = read_csv_file(input_path)
        print(f"Successfully read CSV file: {input_path}")
        
        # Convert CSV to dictionary list
        dict_data = csv_to_dict_list(csv_content)
        print(f"Converted {len(dict_data)} rows from CSV")
        
        # Detect and convert types
        typed_data = detect_and_convert_types(dict_data)
        print("Applied type detection and conversion")
        
        # Convert to JSON
        json_content = dict_list_to_json(typed_data)
        
        # Write JSON file
        write_json_file(json_content, output_path)
        print(f"Successfully wrote JSON file: {output_path}")
        
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except csv.Error as e:
        print(f"CSV parsing error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONEncodeError as e:
        print(f"JSON encoding error: {e}", file=sys.stderr)
        sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Convert CSV files to JSON format with automatic type detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python csv_to_json_v3_prompted.py input.csv output.json
  python csv_to_json_v3_prompted.py data/sales.csv results/sales.json
        """
    )
    
    parser.add_argument(
        'input_csv',
        type=Path,
        help='Path to the input CSV file'
    )
    
    parser.add_argument(
        'output_json',
        type=Path,
        help='Path to the output JSON file'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='CSV to JSON Converter v3.0'
    )
    
    return parser.parse_args()


def main() -> None:
    """
    Main function to handle command line execution.
    """
    args = parse_arguments()
    
    # Validate input file exists
    if not args.input_csv.exists():
        print(f"Error: Input file does not exist: {args.input_csv}", file=sys.stderr)
        sys.exit(1)
    
    # Validate input file is a file (not a directory)
    if not args.input_csv.is_file():
        print(f"Error: Input path is not a file: {args.input_csv}", file=sys.stderr)
        sys.exit(1)
    
    # Convert CSV to JSON
    convert_csv_to_json(args.input_csv, args.output_json)


if __name__ == "__main__":
    main()