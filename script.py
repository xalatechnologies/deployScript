import os
import subprocess

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