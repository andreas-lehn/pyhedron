import os
from pathlib import Path

def get():
    """Determines the version of this project from the git branch name
    
    Release branches have the following syntax::

        release/<version_number>

    For such a branch, ``git_version`` returns ``<version_number>``.
    If the current branch is not a release branch,
    a ``ValueError``is raised.
    """

    stream = os.popen('git branch')
    for branch in stream.readlines():
        if branch[0] == '*':
            branch = branch[2:].strip()
            parts = branch.split('/')
            if parts[0] != 'release':
                raise ValueError(f'branch "{branch}" is not a release branch')
            else:
                return parts[1]

def create_version_file(dir, version):
    name = Path(dir) / '_version.py'
    file = open(name, 'w')
    print(f'__version__ = "{version}"', file=file)
    return name

if __name__ == '__main__':
    try:
        v = get()
        print('Version is:', v)
        f = create_version_file('.', v)
        print('Version file created:', str(f))
    except ValueError as err:
        print(err)
