import scrapy


class MySpider(scrapy.Spider):
    name = 'myspider'

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url += 'tag/' + tag
            print('url:------------>%s' % url)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
            }

        next_page = response.css('li.next a')
        if next_page:
            yield response.follow(next_page, self.parse)
