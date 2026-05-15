import os
import requests

# Intentional secrets for testing our scanner
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
api_key = "sk-abc123def456ghi789jkl"
password = "admin123"
db_url = "mysql://root:password123@localhost/mydb"
github_token = "ghp_16C7e42F292c6912E7710c838347Ae298v54"

def get_user_data(user_id):
    response = requests.get(f"http://api.example.com/users/{user_id}", 
                           headers={"Authorization": f"Bearer {api_key}"})
    return response.json()

def connect_db():
    connection_string = db_url
    return connection_string