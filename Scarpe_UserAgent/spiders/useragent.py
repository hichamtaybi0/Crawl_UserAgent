# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import base64

script = '''
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  splash:set_viewport_full()
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
'''


def save_png(data, name):
    imgdata = base64.b64decode(data)
    with open(name, 'wb') as f:
        f.write(imgdata)
        f.close()


class UseragentSpider(scrapy.Spider):
    name = 'useragent'
    allowed_domains = ['udger.com']

    # start_urls = ['http://udger.com/resources/ua-list/']

    def start_requests(self):
        url = 'http://udger.com/resources/ua-list'
        yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'lua_source': script})

    def parse(self, response):
        # save_png(response.data['png'], 'img.png')
        links = response.xpath("//*[@id='container']/table/tbody/tr/td[2]/a/@href").getall()
        for link in links:
            yield SplashRequest(url=response.urljoin(link), callback=self.parse_link, endpoint='execute',
                                args={'lua_source': script})

    def parse_link(self, response):
        # save_png(response.data['png'], 'img01.png')
        yield {
            response.xpath("//*[@id='container']/h2/text()").get(): response.xpath(
                '//*[@id="container"]/table/tbody/tr/td/p/a/text()').getall()
        }
