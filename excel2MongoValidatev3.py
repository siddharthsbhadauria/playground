import pandas as pd
import numpy as np
from jsonschema import validate, ValidationError
import json
import logging
from pymongo import MongoClient
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Function to load the configuration
def load_config(config_path="config.json"):
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            logging.info("Configuration loaded successfully.")
            return config
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        raise

# Function to load the schema
def load_schema(schema_path):
    try:
        with open(schema_path, "r") as file:
            schema = json.load(file)
            logging.info("Schema loaded successfully.")
            return schema
    except Exception as e:
        logging.error(f"Error loading schema: {e}")
        raise

# Function to read the Excel file and clean NaN values
def read_excel(file_path, sheet_name=None):
    try:
        df = pd.read_excel(file_path, skiprows=3, sheet_name=sheet_name)  # Skip the first 3 rows
        # Trim column names
        df.columns = df.columns.str.strip()
        
        # Fill NaN with appropriate default values
        for col in df.columns:
            if df[col].dtype == 'O':  # If the column is expected to be object/string
                df[col] = df[col].fillna("").str.strip()  # Replace NaN with empty string
            else:
                df[col] = df[col].fillna(0)  # Replace NaN with zero for numerical columns
                
        logging.info("Excel data read and cleaned successfully.")
        return df
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        raise

# Function to validate the data
def validate_data(df, schema):
    # Validate each row against the schema
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

# Function to load data into MongoDB
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

# Main process function
def process_data():
    # Load configuration
    config = load_config()

    # Get Excel file path and optional sheet name from command line arguments
    if len(sys.argv) < 2:
        logging.error("Excel
