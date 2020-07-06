# coding=utf8

import url_manager, html_downloader, html_parser, html_outputer

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def crawl(self, root_url):
        self.urls.add_new_url(root_url)
        count = 1
        while self.urls.has_new_url():
            new_url = self.urls.get_new_url()
            print('crawl %d: %s' % (count, new_url))
            html_cont = self.downloader.download(new_url)
            new_urls, new_data = self.parser.parse(new_url, html_cont)
            self.urls.add_new_urls(new_urls)
            self.outputer.collect_data(new_data)

            if count == 10:
                break
            count += 1

        self.outputer.output_html()


def main():
    root_url = "https://baike.baidu.com/item/Python/407313"
    obj_spider = SpiderMain()
    obj_spider.crawl(root_url)


if __name__ == '__main__':
    main()
