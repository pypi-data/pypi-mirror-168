from enum import Flag
import os
import environ
from pathlib import Path
from dotenv import load_dotenv

from users.models import User
from home.models import CreateProject

ENVIRONMENT = os.environ.get("ENVIRONMENT")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

project_key = os.environ.get("project_key")
user_id = os.environ.get("user_id")


def verified_project():
    project = CreateProject.objects.filter(project_key=project_key).first()
    user = User.objects.filter(id=user_id).first()

    if user and project and user == project.user:
        return True
    return False