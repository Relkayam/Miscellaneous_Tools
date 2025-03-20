import os
import re
import argparse
from PyPDF2 import PdfMerger
from pathlib import Path


def extract_number_prefix(filename):
    """Extract the numeric prefix from a filename."""
    # Match patterns like '1 - filename.pdf', '01 - filename.pdf', etc.
    match = re.match(r'^(\d+)\s*-\s*.*\.pdf$', filename.lower())
    if match:
        return int(match.group(1))
    return float('inf')  # For files without a numeric prefix


def merge_pdfs(input_folder='input', output_folder='results', output_filename='merged.pdf'):
    """
    Merge all PDF files in the input folder and save the result to the output folder.
    Files are merged in ascending order based on their numeric prefixes.

    Args:
        input_folder (str): Path to the folder containing PDF files to merge
        output_folder (str): Path to the folder where the merged PDF will be saved
        output_filename (str): Name of the output merged PDF file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create output folder if it doesn't exist
        Path(output_folder).mkdir(exist_ok=True)

        # Get all PDF files from the input folder
        pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]

        if not pdf_files:
            print(f"No PDF files found in the '{input_folder}' folder.")
            return False

        # Sort PDF files by their numeric prefix
        pdf_files.sort(key=extract_number_prefix)

        # Create a PDF merger object
        merger = PdfMerger()

        # Add each PDF to the merger
        for pdf in pdf_files:
            file_path = os.path.join(input_folder, pdf)
            print(f"Adding: {pdf}")
            merger.append(file_path)

        # Write the merged PDF to the output folder
        output_path = os.path.join(output_folder, output_filename)
        merger.write(output_path)
        merger.close()

        print(f"Successfully merged {len(pdf_files)} PDF files into '{output_path}'")
        return True

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Merge PDF files from an input folder')
    parser.add_argument('--input', default='input', help='Input folder containing PDF files')
    parser.add_argument('--output', default='results', help='Output folder for the merged PDF')
    parser.add_argument('--filename', default='merged.pdf', help='Name of the output merged PDF file')

    args = parser.parse_args()

    # Run the merge function
    merge_pdfs(args.input, args.output, args.filename)