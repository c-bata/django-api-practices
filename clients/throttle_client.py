from concurrent.futures.thread import ThreadPoolExecutor
import os
import requests
from requests.auth import HTTPBasicAuth
import time
from threading import Lock
from typing import Iterator, Tuple


do_login = os.environ.get("USE_AUTH") == "true"
username = "shibata"
password = "abcde10223"
url = "http://127.0.0.1:8000/api/snippets/"

if do_login:
    rate_per_second = 8
else:
    rate_per_second = 2


class Throttle:
    def __init__(self, rate):
        self._consume_lock = Lock()
        self.rate = rate  # per second
        self.tokens = 0.0
        self.last = 0

    def consume(self, amount=1):
        if amount > self.rate:
            raise ValueError("amount must be less or equal to rate")

        with self._consume_lock:
            while True:
                now = time.time()

                if self.last == 0:
                    self.last = now

                elapsed = now - self.last
                self.tokens += elapsed * self.rate
                self.last = now

                if self.tokens > self.rate:
                    self.tokens = self.rate

                if self.tokens >= amount:
                    self.tokens -= amount
                    return amount

                time.sleep((amount - self.tokens) / self.rate)


def fetch_with_throttle(throttle: Throttle):  # returns: status_code, timeout
    throttle.consume()

    try:
        if do_login:
            res = requests.get(url, timeout=5, auth=HTTPBasicAuth(username, password))
        else:
            res = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        return 0, True
    except requests.exceptions.ConnectionError:
        # Sometimes raised a following Exception:
        # requests.exceptions.ConnectionError: ('Connection aborted.', BrokenPipeError(32, 'Broken pipe'))
        return fetch_with_throttle(throttle)
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
    throttle = Throttle(rate_per_second)
    while True:
        start = time.time()
        with ThreadPoolExecutor(10) as pool:
            results = pool.map(fetch_with_throttle, [throttle for _ in range(20)])
        end = time.time()
        elapsed = end - start
        print_result(results, elapsed)


if __name__ == '__main__':
    main()
