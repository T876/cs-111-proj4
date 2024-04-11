import requests
import re


class RequestGuard:
    def __init__(self, domain):
        self.domain = domain
        self.forbidden = self.parse_robots()

    def can_follow_link(self, url):
        if self.domain not in url:
            return False
        for path in self.forbidden:
            if self.domain + path in url:
                return False
        return True

    def make_get_request(self, *args, **kwargs):
        url = args[0]
        if self.can_follow_link(url):
            return requests.get(*args, **kwargs)
        return None

    def parse_robots(self):
        return re.findall(r'Disallow: (.*)', requests.get(self.domain + '/robots.txt').text)
