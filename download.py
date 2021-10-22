#http://docs.google.com/spreadsheets/d/1PzLHfWmVWJHrBGnNSsLTsdH0ibdk0hB4MpKHET1nkpU/export?format=xlsx&id=1PzLHfWmVWJHrBGnNSsLTsdH0ibdk0hB4MpKHET1nkpU
import os
import requests


def download(url:str):
    filename = 'main.xlsx'  # be careful with file names
    file_path = os.path.join(filename)
    r = requests.get(url, stream=True)
    if r.ok:
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))