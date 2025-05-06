import os

AUTHORITY = os.getenv("AUTHORITY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")
# Tells the Flask-session extension to store sessions in the filesystem. Don't use in production apps.
SESSION_TYPE = "filesystem"
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
ENDPOINT = os.getenv("ENDPOINT")
LLM_SCOPE = os.getenv("LLM_SCOPE")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
