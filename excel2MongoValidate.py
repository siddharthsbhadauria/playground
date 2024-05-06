import pandas as pd
from pymongo import MongoClient
import json
import logging
from jsonschema import validate, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_excel_to_mongodb_with_validation(file_path, sheet_name, connection_string, database_name, collection_name, schema_path):
    """
    Load data from an Excel file into MongoDB after validating against a JSON schema.
    """
    try:
        # Load the JSON schema
        with open(schema_path, 'r') as schema_file:
            schema = json.load(schema_file)
        
        # Read the Excel file
        try:
            excel_file = pd.ExcelFile(file_path)
        except FileNotFoundError:
            logger.error(f"The file {file_path} was not found.")
            return
        
        if sheet_name not in excel_file.sheet_names:
            logger.error(f"The sheet '{sheet_name}' does not exist in {file_path}.")
            return
        
        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        # Connect to MongoDB
        with MongoClient(connection_string) as client:
            db = client[database_name]
            collection = db[collection_name]

            # Convert DataFrame to JSON and validate
            json_data = json.loads(df.to_json(orient='records'))

            # Validate each record against the schema
            valid_data = []
            for record in json_data:
                try:
                    validate(instance=record, schema=schema)
                    valid_data.append(record)
                except ValidationError as e:
                    logger.warning(f"Validation error for record: {record} - {e.message}")

            # Insert valid data into MongoDB
            if valid_data:
                collection.insert_many(valid_data)
                logger.info("Valid data loaded into MongoDB successfully.")
            else:
                logger.warning("No valid data to load into MongoDB.")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# Example Usage
file_path = "path/to/your/excel_file.xlsx"
sheet_name = "Sheet1"
connection_string = "mongodb://localhost:27017"
database_name = "your_database_name"
collection_name = "your_collection_name"
schema_path = "path/to/your/schema.json"

load_excel_to_mongodb_with_validation(file_path, sheet_name, connection_string, database_name, collection_name, schema_path)
