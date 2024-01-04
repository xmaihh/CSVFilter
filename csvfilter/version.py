import subprocess


def _get_git_commit_count():
    cmd = "git rev-list --count HEAD"
    ret = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=1,
        text=True,
    )
    if ret.returncode == 0:
        return int(ret.stdout.strip())
    else:
        return -1


def _get_git_commit_hash():
    cmd = "git rev-parse --short=7 HEAD"
    ret = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=1,
        text=True,
    )
    if ret.returncode == 0:
        return ret.stdout.strip()
    else:
        return "Failed to get Git commit hash"


def get_git_version():
    commit_count = _get_git_commit_count()
    commit_hash = _get_git_commit_hash()
    if commit_count >= 0 and commit_hash != "Failed to get Git commit hash":
        return f"V{commit_count}.{commit_hash}"
    else:
        return "Failed to get Git commit count"


if __name__ == "__main__":
    git_version = get_git_version()
    print("Current Git version:", git_version)
