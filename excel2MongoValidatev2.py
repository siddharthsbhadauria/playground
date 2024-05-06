import pandas as pd
from pymongo import MongoClient
import logging
from jsonschema import validate, ValidationError
import json
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Load configuration from config.json
def load_config(config_path="config.json"):
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            logging.info("Configuration loaded successfully.")
            return config
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        raise

# Function to load the JSON schema from a file
def load_schema(schema_path):
    try:
        with open(schema_path, "r") as file:
            schema = json.load(file)
            logging.info("Schema loaded successfully.")
            return schema
    except Exception as e:
        logging.error(f"Error loading schema from file: {e}")
        raise

# Function to read the Excel file with specified sheet name
def read_excel(file_path, sheet_name=None):
    try:
        df = pd.read_excel(file_path, skiprows=3, sheet_name=sheet_name)  # Skip first 3 rows
        # Trim the column names and data to remove leading/trailing spaces
        df.columns = df.columns.str.strip()
        for col in df.columns:
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
        logging.info("Excel data read successfully.")
        return df
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        raise

# Function to validate each row of the data against the schema
def validate_data(df, schema):
    try:
        for _, row in df.iterrows():
            data = row.to_dict()
            validate(instance=data, schema=schema)
        logging.info("Data validation successful.")
    except ValidationError as ve:
        logging.error(f"Validation error: {ve}")
        raise
    except Exception as e:
        logging.error(f"Error during validation: {e}")
        raise

# Function to load the data into MongoDB
def load_to_mongodb(data, config):
    try:
        # Connect to MongoDB
        client = MongoClient(config["mongodb"]["connection_string"])
        db = client[config["mongodb"]["db_name"]]
        collection = db[config["mongodb"]["collection_name"]]
        collection.insert_many(data.to_dict("records"))
        logging.info("Data loaded into MongoDB successfully.")
    except Exception as e:
        logging.error(f"Error loading data into MongoDB: {e}")
        raise

# Main function to coordinate reading, validating, and loading data
def process_data():
    # Load configuration
    config = load_config()

    # Get the Excel file path and optional sheet name from command line arguments
    if len(sys.argv) < 2:
        logging.error("Excel file path not provided.")
        return

    excel_file_path = sys.argv[1]
    sheet_name = sys.argv[2] if len(sys.argv) > 2 else None

    # Load schema
    schema = load_schema(config["schema_path"])

    # Read Excel data
    df = read_excel(excel_file_path, sheet_name)

    # Validate data
    validate_data(df, schema)

    # Load data into MongoDB
    load_to_mongodb(df, config)

# Entry point for running the script
if __name__ == "__main__":
    process_data()

