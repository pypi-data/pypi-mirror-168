import re

def verified_project(project_key: str):
    verify = re.search(project_key, project_key)

    if verify:
        print("Project key is verified")
    else:
        print("Project key is not verified")
