import pandas as pd
import numpy as np
import json
import logging
from jsonschema import validate, ValidationError
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Load the schema from a file
def load_schema(schema_path):
    try:
        with open(schema_path, "r") as file:
            schema = json.load(file)
            logging.info("Schema loaded successfully.")
            return schema
    except Exception as e:
        logging.error(f"Error loading schema: {e}")
        raise

# Read Excel data and convert blanks to None
def read_excel_with_null_handling(file_path, sheet_name=None):
    try:
        df = pd.read_excel(file_path, skiprows=3, sheet_name=sheet_name)  # Skip the first 3 rows
        df.columns = df.columns.str.strip()  # Trim column names

        # Convert blank/whitespace-only fields to NaN
        for col in df.columns:
            df[col] = df[col].apply(lambda x: None if isinstance(x, str) and x.strip() == "" else x)
            
        logging.info("Excel data read and blanks handled successfully.")
        return df
    
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        raise

# Validate data against the schema
def validate_data(df, schema):
    try:
        for index, row in df.iterrows():
            data = row.to_dict()
            # Validate the instance against the schema
            validate(instance=data, schema=schema)
        logging.info("Data validation successful.")
    except ValidationError as ve:
        logging.error(f"Validation error at row {index + 1}: {ve.message}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during validation: {e}")
        raise

# Main processing function
def process_data():
    schema_path = "schema.json"  # Adjust to your schema file path
    excel_file_path = sys.argv[1]  # Get Excel file path from command line
    sheet_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Load the schema
    schema = load_schema(schema_path)
    
    # Read and clean Excel data
    df = read_excel_with_null_handling(excel_file_path, sheet_name)
    
    # Validate the data against the schema
    validate_data(df, schema)
    
    # Data is validated, ready for further processing or MongoDB insertion
    # Add any additional processing steps or MongoDB insertion logic
    
# Entry point for running the script
if __name__ == "__main__":
    process_data()
