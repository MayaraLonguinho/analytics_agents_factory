import urllib.request
import urllib.error
import time

class HealthChecker:
    def check_health(self, url: str, retries: int = 3, delay: int = 1) -> bool:
        for _ in range(retries):
            try:
                response = urllib.request.urlopen(url)
                if response.getcode() == 200:
                    return True
            except urllib.error.URLError:
                pass
            time.sleep(delay)
        return False
