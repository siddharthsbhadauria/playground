import pandas as pd
import json
import logging
from jsonschema import ValidationError, validate
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

# Read Excel data and handle NaN according to expected data types from the schema
def read_excel_with_dtype(file_path, schema, sheet_name=None):
    try:
        df = pd.read_excel(file_path, skiprows=3, sheet_name=sheet_name)  # Skip the first 3 rows
        df.columns = df.columns.str.strip()  # Trim column names
        
        # Apply expected data types from the schema and handle NaN
        for column_name, property_info in schema["properties"].items():
            expected_type = property_info["type"]
            
            if expected_type == "string":
                df[column_name] = df[column_name].fillna("")  # Replace NaN with empty string
                df[column_name] = df[column_name].astype(str).str.strip()  # Ensure it's a string
            
            elif expected_type == "integer":
                df[column_name] = pd.to_numeric(df[column_name], errors='coerce').fillna(0).astype(int)  # Coerce to integer
            
            elif expected_type == "boolean":
                # Replace NaN with False for boolean data
                df[column_name] = df[column_name].fillna(False).astype(bool)
            
            elif expected_type == "number":
                # Replace NaN with zero for numeric data
                df[column_name] = pd.to_numeric(df[column_name], errors='coerce').fillna(0)
                
        logging.info("Excel data read and NaN handled successfully.")
        return df
    
    except Exception as e:
        logging.error(f"Error reading Excel file or handling NaN: {e}")
        raise

# Validate data against the schema
def validate_data(df, schema):
    try:
        for index, row in df.iterrows():
            data = row.to_dict()
            validate(instance=data, schema=schema)
        logging.info("Data validation successful.")
    except ValidationError as ve:
        logging.error(f"Validation error at row {index + 1}: {ve.message}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during validation: {e}")
        raise

# Function to load the data into MongoDB
def load_to_mongodb(data, config):
    try:
        client = MongoClient(config["mongodb"]["connection_string"])
        db = client[config["mongodb"]["db_name"]]
        collection = db[config["mongodb"]["collection_name"]]
        collection.insert_many(data.to_dict("records"))
        logging.info("Data loaded into MongoDB successfully.")
    except Exception as e:
        logging.error(f"Error loading data into MongoDB: {e}")
        raise

# Main processing function
def process_data():
    # Load configuration
    config_path = "config.json"  # Adjust to your config file path
    schema_path = "schema.json"  # Adjust to your schema file path
    
    # Load configuration and schema
    config = load_config(config_path)
    schema = load_schema(schema_path)
    
    # Get Excel file path and optional sheet name from command line arguments
    excel_file_path = sys.argv[1]
    sheet_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Read and clean Excel data
    df = read_excel_with_dtype(excel_file_path, schema, sheet_name)
    
    # Validate the data against the schema
    validate_data(df, schema)
    
    # Load into MongoDB
    load_to_mongodb(df, config)
    
# Entry point for running the script
if __name__ == "__main__":
    process_data()
