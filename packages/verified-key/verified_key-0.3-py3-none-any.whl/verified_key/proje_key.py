import os
import environ
from pathlib import Path
from dotenv import load_dotenv

ENVIRONMENT = os.environ.get("ENVIRONMENT")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

project_key = os.environ.get("project_key"),
user_id = os.environ.get("user_id")

def verified_project():
    # project_key = load_dotenv()

    print(project_key)
    print(user_id)

print(verified_project())
