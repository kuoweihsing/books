import scrapy
import json

class BookSpider(scrapy.Spider):
    name = "book"
    # allowed_domains = ["x"]
    start_urls = [
        "https://www.books.com.tw/products/CN13297694?loc=P_0003_005",
        "https://www.books.com.tw/products/CN13175214?loc=P_0003_007",
        "https://www.books.com.tw/products/CN13081490?loc=P_0003_009",
        "https://www.books.com.tw/products/CN13095102?loc=P_0003_010",
        "https://www.books.com.tw/products/CN13278561?loc=P_0003_012",
        "https://www.books.com.tw/products/CN13368706?loc=P_0003_002"
    ]

    def parse(self, response):
        print(response)
        if response.status == 484:
            yield scrapy.Request(
                url=response.url,
                callback=self.parse,
                meta=meta
            )
        meta = response.meta
        categories = response.css('ul[typeof="BreadcrumbList"] > li > meta[property="name"]::attr(content)').getall()
        data = response.css('script[type="application/ld+json"]::text').get()
        if data and categories:
            jsonData = json.loads(data)
            category = []
            for c in categories:
                if c not in ['博客來', '商品介紹']:
                    category.append(c)
            meta['datePublished'] = jsonData['datePublished']
            meta['inLanguage'] = jsonData['inLanguage']
            meta['author'] = ', '.join([item['name'] for item in jsonData['author']])
            meta['publisher'] = ', '.join([item['name'] for item in jsonData['publisher']])
            meta['isbn'] = jsonData['workExample']['workExample']['isbn']
            meta['bookFormat'] = jsonData['workExample']['workExample']['bookFormat'].split('/')[-1]
            meta['title'] = jsonData['name']
            meta['mainImgUrl'] = jsonData['image']
            meta['id'] = jsonData['url'].split('/')[-1]
            meta['categories'] = category
            yield {
                'id': meta['id'],
                'title': meta['title'],
                'mainImgUrl': meta['mainImgUrl'],
                'datePublished': meta['datePublished'],
                'inLanguage': meta['inLanguage'],
                'author': meta['author'],
                'publisher': meta['publisher'],
                'isbn': meta['isbn'],
                'bookFormat': meta['bookFormat'],
                'categories': meta['categories']
            }
