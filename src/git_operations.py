import os
from typing import Union

from git import Repo

TEMP_PATH = os.getenv("TEMP_FOLDER_PATH", "/tmp")


def clone_git_repo(repo_url: str) -> Union[bool, str]:
    """
    Clone a git repository to a local directory.

    Args:
        repo_url (str): The URL of the git repository to clone.

    Returns:
        Union[bool, str]: A tuple containing a boolean indicating success and either the path to the cloned repo or an error message.
    """
    try:
        repo_name = repo_url.split('/')[-1]
        path = f'{TEMP_PATH}/git_repo/{repo_name}'

        if os.path.exists(path):
            os.system(f"rm -rf {path}")
        os.makedirs(path, exist_ok=True)
        Repo.clone_from(repo_url, path)
        return True, path
    except Exception as e:
        return False, f"Error cloning {repo_url}: {str(e)}"
