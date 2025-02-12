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
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["excel_data"]
collection = db["records"]

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        # Detect file type and read accordingly
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file)
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        records = df.to_dict(orient="records")

        if records:
            inserted_ids = collection.insert_many(records).inserted_ids
            inserted_ids_str = [str(_id) for _id in inserted_ids]

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
