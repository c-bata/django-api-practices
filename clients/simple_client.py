import requests
from requests.auth import HTTPBasicAuth
import time

username = "shibata"
password = "abcde1223"


def fetch(url: str):  # returns: status_code, timeout
    try:
        res = requests.get(url, timeout=5, auth=HTTPBasicAuth(username, password))
    except requests.exceptions.Timeout:
        return 0, True
    except requests.exceptions.ConnectionError:
        # Sometimes raised a following Exception:
        # requests.exceptions.ConnectionError: ('Connection aborted.', BrokenPipeError(32, 'Broken pipe'))
        return fetch(url)
    return res.status_code, False


def main():
    url = "http://127.0.0.1:8000/api/snippets/"
    while True:
        start = time.time()
        status_code, timeout = fetch(url)
        end = time.time()
        elapsed = end - start
        print(f"{elapsed:.3f} secs / 1 req, {status_code} timeout={timeout}")
        time.sleep(1)


if __name__ == '__main__':
    main()
