import requests


class HtmlDownloader(object):
    def download(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:46.0) Gecko/20100101 Firefox/46.0'}
        if url is None: return
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return
        return response.text
