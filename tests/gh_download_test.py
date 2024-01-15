import requests

username = "xmaihh"
repo = "CSVFilter"
url = f"https://api.github.com/repos/{username}/{repo}/releases/latest"

if __name__ == "__main__":
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print(data["tag_name"])
    assert_url = data["assets"][0]
    download_url = assert_url["browser_download_url"]
    filename = assert_url["name"]
    print(assert_url)
    print(download_url)
    print(filename)
    print(f"Downloading {filename}")
    r = requests.get(download_url, stream=True)
    r.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print("File download completed! ", filename)                                                                                                                                                                                                                                                                                                                                                                                                
