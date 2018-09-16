import requests
import time
from typing import Iterator, Tuple
from concurrent.futures import ThreadPoolExecutor


def fetch(url: str):  # returns: status_code, timeout
    try:
        res = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        return 0, True
    except requests.exceptions.ConnectionError:
        # Sometimes raised a following Exception:
        # requests.exceptions.ConnectionError: ('Connection aborted.', BrokenPipeError(32, 'Broken pipe'))
        return fetch(url)
    return res.status_code, False


def print_result(results: Iterator[Tuple[int, str]], elapsed: float):
    cnt_req, cnt2xx, cnt4xx, cnt5xx, cnt_timeout = 0, 0, 0, 0, 0

    for r in results:
        status_code = r[0]
        timeout = r[1]
        cnt_req += 1
        if timeout:
            cnt_timeout += 1
        elif 200 <= status_code < 300:
            cnt2xx += 1
        elif 400 <= status_code < 500:
            cnt4xx += 1
        elif 500 <= status_code:
            cnt5xx += 1

    print(f"{elapsed:.3f} secs / {cnt_req} req, 2xx={cnt2xx} 4xx={cnt4xx} 5xx={cnt5xx} timeout={cnt_timeout}")


def main():
    url = "http://127.0.0.1:8000/api/snippets/"
    while True:
        start = time.time()
        with ThreadPoolExecutor(10) as pool:
            results = pool.map(fetch, [url for _ in range(100)])
        end = time.time()
        elapsed = end - start
        print_result(results, elapsed)


if __name__ == '__main__':
    main()
