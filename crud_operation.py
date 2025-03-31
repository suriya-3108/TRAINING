import os
import json
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
from datetime import datetime
from urllib.parse import parse_qs

# Local development setup - only for testing in VS Code
if __name__ == "__main__":
    os.environ['MONGODB_URI'] = "mongodb+srv://<user_name>:<password>@cluster0.nz00g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Local MongoDB
    os.environ['MONGODB_NAME'] = "test_db"

# Initialize MongoDB connection with error handling
def get_db():
    try:
        client = MongoClient(
            os.environ['MONGODB_URI'],
            connectTimeoutMS=3000,
            socketTimeoutMS=3000,
            serverSelectionTimeoutMS=3000
        )
        # Verify connection
        client.admin.command('ping')
        db = client[os.environ['MONGODB_NAME']]
        
        # Ensure collection and counter exist
        if 'dynamic_data' not in db.list_collection_names():
            db.create_collection('dynamic_data')
        
        if 'counters' not in db.list_collection_names():
            db.create_collection('counters')
            db.counters.insert_one({'_id': 'userid', 'seq': 0})
        
        return db
    except Exception as e:
        raise Exception(f"Database connection failed: {str(e)}")

def get_next_sequence(db, name):
    counter = db.counters.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return counter['seq']

def lambda_handler(event, context=None):
    try:
        db = get_db()
        collection = db['dynamic_data']
        
        # Parse request method and path
        http_method = event.get('httpMethod')
        path = event.get('path', '')
        
        # Parse request body
        body = {}
        if event.get('body'):
            try:
                if event.get('isBase64Encoded', False):
                    import base64
                    body_str = base64.b64decode(event['body']).decode('utf-8')
                else:
                    body_str = event['body']
                body = json.loads(body_str)
            except json.JSONDecodeError:
                return {'statusCode': 400, 'body': 'Invalid JSON format'}
        
        # STORE - Create new document
        if http_method == 'POST' and path.endswith('/store'):
            if not body:
                return {'statusCode': 400, 'body': 'No data provided'}
            
            try:
                # Get sequential ID
                seq_id = get_next_sequence(db, 'userid')
                
                # Insert document with sequential ID
                result = collection.insert_one({
                    '_id': seq_id,
                    **body,
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                })
                return {
                    'statusCode': 201,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        '_id': seq_id,
                        'message': 'Document created successfully'
                    })
                }
            except Exception as e:
                return {'statusCode': 400, 'body': f'Insert failed: {str(e)}'}
        
        # GET - Retrieve document by ID
        elif http_method == 'GET' and path.endswith('/get'):
            query_params = event.get('queryStringParameters', {})
            document_id = query_params.get('id')
            
            if not document_id:
                return {'statusCode': 400, 'body': 'ID parameter is required'}
            
            try:
                document_id = int(document_id)  # Convert to integer
                document = collection.find_one({'_id': document_id})
                if not document:
                    return {'statusCode': 404, 'body': 'Document not found'}
                
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': dumps(document)
                }
            except ValueError:
                return {'statusCode': 400, 'body': 'ID must be an integer'}
            except Exception as e:
                return {'statusCode': 400, 'body': f'Error: {str(e)}'}
        
        # UPDATE - Modify existing document
        elif http_method == 'PUT' and path.endswith('/update'):
            if not body.get('id'):
                return {'statusCode': 400, 'body': 'Document ID is required'}
            
            update_data = {k: v for k, v in body.items() if k != 'id'}
            if not update_data:
                return {'statusCode': 400, 'body': 'No update data provided'}
            
            try:
                doc_id = int(body['id'])  # Convert to integer
                result = collection.update_one(
                    {'_id': doc_id},
                    {
                        '$set': {
                            **update_data,
                            'updated_at': datetime.utcnow()
                        }
                    }
                )
                
                if result.matched_count == 0:
                    return {'statusCode': 404, 'body': 'Document not found'}
                
                # Return the updated document
                updated_doc = collection.find_one({'_id': doc_id})
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': dumps(updated_doc)
                }
            except ValueError:
                return {'statusCode': 400, 'body': 'ID must be an integer'}
            except Exception as e:
                return {'statusCode': 400, 'body': f'Update failed: {str(e)}'}
        
        # DELETE - Remove document
        elif http_method == 'DELETE' and path.endswith('/delete'):
            query_params = event.get('queryStringParameters', {})
            document_id = query_params.get('id')
            
            if not document_id:
                return {'statusCode': 400, 'body': 'ID parameter is required'}
            
            try:
                doc_id = int(document_id)  # Convert to integer
                result = collection.delete_one({'_id': doc_id})
                if result.deleted_count == 0:
                    return {'statusCode': 404, 'body': 'Document not found'}
                
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'message': 'Document deleted successfully',
                        'deleted_id': doc_id
                    })
                }
            except ValueError:
                return {'statusCode': 400, 'body': 'ID must be an integer'}
            except Exception as e:
                return {'statusCode': 400, 'body': f'Delete failed: {str(e)}'}
        
        else:
            return {'statusCode': 404, 'body': 'Endpoint not found'}
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Internal server error: {str(e)}'
        }

# Test harness for VS Code
if __name__ == "__main__":
    # Test cases
    test_events = [
        {
            "name": "Create document",
            "httpMethod": "POST",
            "path": "/store",
            "body": json.dumps({"username": "testuser", "email": "test@example.com"})
        },
        {
            "name": "Get document",
            "httpMethod": "GET",
            "path": "/get",
            "queryStringParameters": {"id": "1"}
        }
    ]
    
    # Run tests
    for test in test_events:
        print(f"\nTesting: {test['name']}")
        result = lambda_handler(test)
        print(f"Status: {result['statusCode']}")
        print(f"Response: {result['body']}\n")