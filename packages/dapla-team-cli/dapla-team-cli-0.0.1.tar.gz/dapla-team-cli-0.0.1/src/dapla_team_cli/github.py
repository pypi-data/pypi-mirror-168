"""Git functionality."""
from typing import Set

from git.repo import Repo
from pydantic import BaseModel


class NewBranch(BaseModel):
    """Information used to create a new Git branch.

    Attributes:
        repo_path: Local path to the git repo
        branch_name: Name of the branch to create
        commit_msg: Message that describes the git commit
        files: Files included in the commit
        instruction_msg: Message that should be displayed after the branch was pushed
    """

    repo_path: str
    branch_name: str
    commit_msg: str
    files: Set[str]
    instruction_msg: str


def create_branch(branch: NewBranch) -> None:
    """Create a new git branch with a set of files."""
    repo = Repo(branch.repo_path)
    current = repo.create_head(branch.branch_name)
    current.checkout()
    main = repo.heads.main

    if repo.index.diff(None) or repo.untracked_files:
        repo.git.pull("origin", main)
        for f in branch.files:
            repo.git.add(f)
        repo.git.commit(m=branch.commit_msg)
        repo.git.push("--set-upstream", "origin", current)
        print(branch.instruction_msg)
    else:
        print("No changes...")
