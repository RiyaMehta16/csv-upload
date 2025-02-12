from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv  # Import dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Use environment variables for MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
PORT = int(os.getenv("PORT", 5000)) # Default to 5000 if not set
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Connect to MongoDB
client = MongoClient(MONGO_URI)# Connect to MongoDB using the URI
db = client["excel_data"] # Select database
collection = db["records"]# Select collection

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400  #If no file is found, return { "error": "No file provided" } with status code 400.

    file = request.files["file"]#Extracts the uploaded file from the frontend (FormData)
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400 #If file name is empty, return { "error": "No selected file" }

    try:
        # Detect file type and read accordingly
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file) # Read CSV into a DataFrame 
        elif file.filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file) # Read Excel into a DataFrame
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        records = df.to_dict(orient="records")#After reading the file, we convert it to a list of dictionaries before inserting into MongoDB

        if records:
            inserted_ids = collection.insert_many(records).inserted_ids #Uses collection.insert_many(records) to insert multiple documents into MongoDB.
            inserted_ids_str = [str(_id) for _id in inserted_ids] #Converts ObjectId to string format (str(_id)) to avoid JSON serialization errors.

        return jsonify({
            "message": "File processed and data stored successfully",
            "inserted_ids": inserted_ids_str
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/test_db", methods=["GET"])
def test_db():
    try:
        test_record = {"test": "MongoDB connection successful"}
        collection.insert_one(test_record)

        last_entry = collection.find_one(sort=[("_id", -1)])
        return jsonify({"message": "MongoDB is connected!", "last_entry": last_entry}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=DEBUG, port=PORT)


'''
df is a Pandas DataFrame, which is a 2D table-like data structure in Python, similar to an Excel spreadsheet or a SQL table.

What Does a DataFrame Look Like?
Example: Suppose you upload a CSV file (students.csv) with this data:

Name	Age	Grade
Alice	20	A
Bob	    21	B
Charlie	22	A

If you read it using df = pd.read_csv("students.csv"), then df will contain:

    Name     Age    Grade
0   Alice    20     A
1   Bob      21     B
2   Charlie  22     A

After reading the file, we convert it to a list of dictionaries before inserting into MongoDB:

#records = df.to_dict(orient="records")

This turns it into:

[
    {"Name": "Alice", "Age": 20, "Grade": "A"},
    {"Name": "Bob", "Age": 21, "Grade": "B"},
    {"Name": "Charlie", "Age": 22, "Grade": "A"}
]

====================================================================================================
Why Convert ObjectId to a String?
In MongoDB, every document has a unique _id, which is automatically assigned as an ObjectId. However, ObjectId is not JSON serializable, meaning it cannot be sent directly as a response in Flask.

Where is the Conversion Done?

#inserted_ids = collection.insert_many(records).inserted_ids
#inserted_ids_str = [str(_id) for _id in inserted_ids]

insert_many(records).inserted_ids returns a list of ObjectIds.
str(_id) for _id in inserted_ids converts each ObjectId to a string.
-------------------------------------------------------------------------------
Example Before and After Conversion
Let's say MongoDB assigns these ObjectIds:

python
#inserted_ids = [ObjectId("65c1a5f8c5e7f3d24c8b4567"), ObjectId("65c1a5f8c5e7f3d24c8b4568")]

If you try to return this in a Flask response:

#return jsonify({"inserted_ids": inserted_ids})


🚨 Error:
TypeError: Object of type ObjectId is not JSON serializable

✅ Fix: Convert to string:

#inserted_ids_str = [str(_id) for _id in inserted_ids]
#return jsonify({"inserted_ids": inserted_ids_str})

Now the response will be:

json

{
  "inserted_ids": [
    "65c1a5f8c5e7f3d24c8b4567",
    "65c1a5f8c5e7f3d24c8b4568"
  ]
}

Why Does This Happen?
JSON only supports basic types like strings, numbers, lists, and dictionaries.
MongoDB’s ObjectId is a binary object, which Flask cannot convert to JSON.
Solution: Convert ObjectId to a string (str(_id)) before returning.

'''