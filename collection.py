import time
from pymongo import MongoClient
from datetime import datetime

def create_and_store_numbers(connection_string, db_name, collection_name, input_number):
    """
    Creates database and collection, stores numbers with custom IDs, and records operation time.
    
    Args:
        connection_string (str): MongoDB connection URL
        db_name (str): Database name to create
        collection_name (str): Collection name to create
        input_number (int): Number of records to store (1 to input_number)
    
    Returns:
        dict: Operation results with timing information
    """
    try:
        # Connect to MongoDB
        client = MongoClient(connection_string)
        
        # Create database (automatically created when we use it)
        db = client[db_name]
        
        # Create collection (automatically created when we insert)
        collection = db[collection_name]
        
        # Clear collection if it exists
        collection.drop()
        
        # Prepare documents with custom _id from 1 to input_number
        documents = [{"_id": i, "number": i} for i in range(1, input_number+1)]
        
        # Time the insertion
        start_time = time.time()
        collection.insert_many(documents)
        time_taken = time.time() - start_time
        
        # Store metadata
        metadata = {
            "operation": "number_insertion",
            "total_numbers": input_number,
            "time_taken_seconds": time_taken,
            "timestamp": datetime.now()
        }
        db["operation_metrics"].insert_one(metadata)
        
        return {
            "status": "success",
            "database": db_name,
            "collection": collection_name,
            "numbers_stored": input_number,
            "time_taken": time_taken
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    # Configuration
    CONNECTION_STRING = "mongodb+srv://suriya3108:beast000720S@cluster0.nz00g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DB_NAME = "number_database"
    COLLECTION_NAME = "numbers"
    
    print(f"Connecting to MongoDB at: {CONNECTION_STRING}")
    print(f"Will create database '{DB_NAME}' and collection '{COLLECTION_NAME}'")
    
    try:
        input_number = int(input("Enter how many numbers to store (1 to n): "))
        
        result = create_and_store_numbers(
            connection_string=CONNECTION_STRING,
            db_name=DB_NAME,
            collection_name=COLLECTION_NAME,
            input_number=input_number
        )
        
        if result["status"] == "success":
            print("\nOperation successful!")
            print(f"Database: {result['database']}")
            print(f"Collection: {result['collection']}")
            print(f"Numbers stored: 1 to {result['numbers_stored']}")
            print(f"Time taken: {result['time_taken']:.4f} seconds")
            
            # Show sample data
            client = MongoClient(CONNECTION_STRING)
            sample = client[DB_NAME][COLLECTION_NAME].find().limit(3)
            
            print("\nSample documents:")
            for doc in sample:
                print(doc)
        else:
            print(f"\nError occurred: {result['error']}")
            
    except ValueError:
        print("Please enter a valid integer for the number count.")