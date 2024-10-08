import os
import subprocess
import time
import zipfile
import requests
from pymongo import MongoClient

# Function to download MongoDB
def download_mongodb():
    url = "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-6.0.0.zip"
    output_path = "mongodb.zip"
    
    # Download MongoDB
    response = requests.get(url, stream=True)
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    
    # Extract MongoDB
    with zipfile.ZipFile(output_path, 'r') as zip_ref:
        zip_ref.extractall("C:\\MongoDB")
    
    # Create data directory
    os.makedirs("C:\\data\\db", exist_ok=True)
    print("MongoDB downloaded and extracted successfully.")

# Function to start MongoDB
def start_mongodb():
    try:
        subprocess.Popen(
            ["C:\\MongoDB\\mongodb-windows-x86_64-6.0.0\\bin\\mongod.exe", "--dbpath", "C:\\data\\db"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(10)  # Wait for MongoDB to start
        print("MongoDB started successfully.")
    except Exception as e:
        print(f"Failed to start MongoDB: {e}")

# Initialize MongoDB if not exists
def initialize_mongodb():
    try:
        client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=5000)
        client.server_info()  # Trigger exception if MongoDB is not available
        db = client['TestDb']
        if 'TestModels' not in db.list_collection_names():
            db.create_collection('TestModels')
            print("Initialized MongoDB and created 'TestModels' collection.")
    except Exception as e:
        print(f"MongoDB initialization failed: {e}")

# Main script flow

# Step 1: Download and start MongoDB
download_mongodb()
start_mongodb()

# Step 2: Initialize MongoDB
initialize_mongodb()

# Restore dependencies
subprocess.run(["dotnet", "restore"], check=True)

# Build solution
subprocess.run(["dotnet", "build", "--configuration", "Release", "--no-restore"], check=True)

# Run tests
subprocess.run(["dotnet", "test", "--configuration", "Release", "--no-build", "--logger", "trx"], check=True)

# Save Test Results
os.makedirs('TestResults', exist_ok=True)
subprocess.run(["cp", "-r", "**/TestResults/*.trx", "TestResults/"], shell=True, check=True)

# Generate Swagger Doc
process = subprocess.Popen(["dotnet", "run", "--project", "DotnetMongoApi/DotnetMongoApi.csproj"])
subprocess.run(["sleep", "20"], shell=True)
subprocess.run(["Invoke-RestMethod", "http://localhost:5000/swagger/v1/swagger.json", "-OutFile", "swagger.json"], shell=True, check=True)

# Modify Swagger Doc with Python Script
subprocess.run(["python", "modify_swagger.py"], check=True)

# Package Application
subprocess.run(["dotnet", "publish", "-c", "Release", "-o", "package"], check=True)

# Publish Application to GitHub Packages
subprocess.run(["python", "publish_to_github_packages.py"], check=True)