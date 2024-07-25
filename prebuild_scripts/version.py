import subprocess
import configparser


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
        return f"{commit_count}.g{commit_hash}"
    else:
        return "Failed to get Git commit count"


if __name__ == "__main__":
    git_version = get_git_version()
    print("Current Git version:", git_version)
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Set the version number
    version = "1.0.0"

    if git_version != "Failed to get Git commit count":
        # Write the version number to the config file
        config['DEFAULT'] = {'Version': git_version}
    else:
        config['DEFAULT'] = {'Version': version}

    # Write the config to the file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    print("Config file has been updated!")
