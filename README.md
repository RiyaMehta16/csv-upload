# 📊 Excel/CSV File Upload & Storage in MongoDB

This project allows users to upload Excel (`.xls`, `.xlsx`) or CSV (`.csv`) files from a React frontend. The uploaded files are processed in a Flask backend and stored in a MongoDB Atlas database.

---

## 🚀 Features
- Accepts **CSV, XLS, and XLSX** file formats.
- Parses and converts file content to JSON.
- Stores data in **MongoDB Atlas**.
- Displays API response in the frontend.

---

## 🛠️ Setup Instructions

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
##📌 Backend (Flask) Setup
### **2️⃣ Install Python & Virtual Environment**
Ensure Python 3.x is installed, then set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate      # For Windows
```
### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```
### **4️⃣ Set Up MongoDB Atlas**
Create a MongoDB Atlas account at MongoDB Atlas.
Create a cluster and get the connection string.
Replace the MONGO_URI in app.py with your own MongoDB connection string. 

### **5️⃣ Run Flask Server**
```bash
python app.py
```
Flask will start at http://127.0.0.1:5000
##📌 Frontend (React) Setup
### **6️⃣ Install Dependencies**
Navigate to the client/ directory and install dependencies:

```bash
cd client
npm install
```
### **7️⃣ Run React Frontend**
```bash
npm start
```
This will start the frontend at http://localhost:3000.

## Uploading a File
Open http://localhost:3000 in your browser.
Click Browse to select a CSV or Excel file.
Click Upload to send the file to Flask.
The response will show inserted document IDs from MongoDB.
##📜 Folder Structure
```bash
/your-repo-name
│── /client       # React Frontend
│── /server       # Flask Backend
│── app.py        # Flask API
│── requirements.txt  # Python Dependencies
│── README.md     # Documentation
```
