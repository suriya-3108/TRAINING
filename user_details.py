from pymongo import MongoClient
import datetime

# Connect to MongoDB Atlas - REPLACE WITH YOUR CONNECTION STRING
connection_string = "mongodb+srv://<username>:<password>@cluster0.nz00g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)

# Create/access database and collection
db = client["user_management_db"]
users_collection = db["users"]

def add_user():
    print("\n=== ADD NEW USER ===")
    
    # Get user input
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    # Create user document
    user_data = {
        "username": username,
        "password": password,  # Note: In production, hash this password!
        "created_at": datetime.datetime.now()
    }
    
    # Insert into MongoDB
    try:
        result = users_collection.insert_one(user_data)
        print(f"\n✅ User '{username}' added successfully!")
        print(f"Database ID: {result.inserted_id}")
    except Exception as e:
        print(f"\n❌ Error adding user: {e}")

# Run the program
if __name__ == "__main__":
    add_user()
