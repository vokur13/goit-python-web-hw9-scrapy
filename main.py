import json

import scrapy
from itemadapter import ItemAdapter
from scrapy.item import Item, Field
from scrapy.crawler import CrawlerProcess


class QuoteItem(Item):
    tags = Field()
    author = Field()
    quote = Field()


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    biography = Field()


def parse_author(response):
    author = response.xpath("//div[@class='author-details']")

    fullname = author.xpath("h3/text()").get().strip()
    born_date = author.xpath("p/span[@class='author-born-date']/text()").get().strip()
    born_location = (
        author.xpath("p/span[@class='author-born-location']/text()").get().strip()
    )
    biography = author.xpath("div[@class='author-description']/text()").get().strip()

    yield AuthorItem(
        fullname=fullname,
        born_date=born_date,
        born_location=born_location,
        biography=biography,
    )


class SpiderPipeline(object):
    quotes = list()
    authors = list()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if "author" in adapter.keys():
            self.quotes.append(
                {
                    "tags": adapter["tags"],
                    "author": adapter["author"],
                    "quote": adapter["quote"],
                }
            )
        if "fullname" in adapter.keys():
            self.authors.append(
                {
                    "fullname": adapter["fullname"],
                    "born_date": adapter["born_date"],
                    "born_location": adapter["born_location"],
                    "biography": adapter["biography"],
                }
            )
        return item

    def close_spider(self, spider):
        with open("quotes.json", "w", encoding="utf-8") as fd:
            json.dump(self.quotes, fd, ensure_ascii=False, indent=4)

        with open("authors.json", "w", encoding="utf-8") as fd:
            json.dump(self.authors, fd, ensure_ascii=False, indent=4)


class Spider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]
    custom_settings = {
        "ITEM_PIPELINES": {
            SpiderPipeline: 300,
        },
    }

    def parse(self, response):
        for cite in response.xpath("//div[@class='quote']"):
            tags = cite.xpath("div[@class='tags']/a/text()").getall()
            author = cite.xpath("span/small/text()").get().strip()
            quote = cite.xpath("span[@class='text']/text()").get().strip()

            yield QuoteItem(tags=tags, author=author, quote=quote)
            yield response.follow(
                url=self.start_urls[0] + cite.xpath("span/a/@href").get(),
                callback=parse_author,
            )

        next_link = response.xpath('//li[@class="next"]/a/@href').get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(Spider)
    process.start()
