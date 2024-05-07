import pandas as pd
from presidio_analyzer import AnalyzerEngine
from pymongo import MongoClient
import logging


# Define a function to check for unexpected columns flagged by Presidio
def check_for_unexpected_pii_columns(
    mongo_connection_string,
    database_name,
    collection_name,
    table_name,
    csv_file_path,
    max_rows=2000,
):
    try:
        # Set up logging configuration
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

        # Connect to Cosmos DB for MongoDB
        client = MongoClient(mongo_connection_string)
        db = client[database_name]
        collection = db[collection_name]

        # Retrieve the schema for the given table
        schema = list(collection.find({"table name": table_name}))

        if not schema:
            logging.error(f"No schema found for table '{table_name}'.")
            raise ValueError("Schema not found for the specified table.")

        # Extract the set of schema-defined columns flagged as PII
        schema_pii_columns = {
            entry["Column Name"]
            for entry in schema
            if entry.get("PII") == "Y"
        }

        # Read the CSV data and limit rows if necessary
        data = pd.read_csv(csv_file_path)
        if len(data) > max_rows:
            data = data.head(max_rows)

        # Presidio Analyzer to scan for PII
        analyzer = AnalyzerEngine()

        # Store Presidio-flagged columns
        presidio_pii_columns = {}

        # Function to scan for PII in a column
        def scan_column_for_pii(column_data):
            pii_found = set()
            for item in column_data:
                results = analyzer.analyze(text=str(item), language="en")
                for result in results:
                    pii_found.add(result.entity_type)
            return pii_found

        # Scan each CSV column for PII
        for column_name in data.columns:
            pii_types = scan_column_for_pii(data[column_name])
            if pii_types:
                presidio_pii_columns[column_name] = pii_types

        # Set of Presidio-flagged columns
        presidio_column_names = set(presidio_pii_columns.keys())

        # Identify unexpected columns flagged by Presidio
        unexpected_columns = presidio_column_names - schema_pii_columns

        # Return True if unexpected columns are found, otherwise False
        if unexpected_columns:
            logging.warning(
                f"Unexpected columns detected by Presidio: {', '.join(unexpected_columns)}"
            )
            return True

        # If no unexpected columns, return False
        logging.info("No unexpected columns detected by Presidio.")
        return False

    except Exception as e:
        logging.error(f"Error during PII check: {str(e)}")
        raise
