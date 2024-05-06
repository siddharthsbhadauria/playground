import pandas as pd
import json
import logging
from jsonschema import validate, ValidationError
import numpy as np
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

# Read Excel data without changing it
def read_excel(file_path, sheet_name=None):
    try:
        df = pd.read_excel(file_path, skiprows=3, sheet_name=sheet_name)  # Skip first 3 rows
        df.columns = df.columns.str.strip()  # Trim column names
        logging.info("Excel data read successfully.")
        return df
    
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        raise

# Validate the data type of each field
def validate_data_types(df, schema):
    try:
        for col in df.columns:
            expected_type = schema["properties"].get(col, {}).get("type")
            
            if expected_type == "string":
                df[col] = df[col].astype(str).str.strip()  # Ensure it's a string
            
            elif expected_type == "integer":
                df[col] = pd.to_numeric(df[col], errors='coerce')  # Coerce to numeric
                # Allow blanks to not raise an error
            
            elif expected_type == "boolean":
                df[col] = df[col].astype(bool)  # Ensure it's a boolean
                
        logging.info("Data type validation successful.")
    
    except Exception as e:
        logging.error(f"Error during data type validation: {e}")
        raise

# Check for blank required fields
def check_required_fields(df, schema):
    try:
        required_fields = schema.get("required", [])
        for field in required_fields:
            if df[field].str.strip() == "" or df[field].isnull().any():  # Check for blanks
                raise ValueError(f"Missing or blank required field: '{field}'")
            
        logging.info("Required field validation successful.")
    
    except Exception as e:
        logging.error(f"Error during required field validation: {e}")
        raise

# Main processing function
def process_data():
    schema_path = "schema.json"  # Adjust to your schema file path
    excel_file_path = sys.argv[1]  # Get Excel file path from command line
    sheet_name = sys.argv[2] if given
    
    # Load the schema
    schema = load_schema(schema_path)

    # Read Excel data without changing it
    df = read_excel(excel_file_path, sheet_name)
    
    # Validate the data types
    validate_data_types(df, schema)
    
    # Check for required fields
    check_required_fields(df, schema)
    
    # Data is validated, ready for further processing or MongoDB insertion
    # Add any additional processing steps or MongoDB insertion logic
    
# Entry point for running the script
if __name__ == "__main__":
    process_data()
