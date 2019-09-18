# igScrape

Scrape Instagram photos by hashtag. igScrape downloads all images from posts that have a given hashtag. The [Scrapy](https://github.com/scrapy/scrapy) web scraping framework is used to build the spider.

## To start using igScrape

You can run the spider using the `scrapy crawl igspider` command. To specify the hashtag, pass the `-a tag=<hashtag>` option and argument. For example:

    $ scrapy crawl igspider -a tag=chickenrice

If you want to crawl geotagged posts from a certain country, you can pass the `-a country=<country_code>` option and argument. For example:
    
    $ scrapy crawl chubbygrub -a tag=chickenrice -a country=SG

Country codes are in [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements) format. If `country` argument is passed, images from posts that are not geotagged will not be scraped.

## Downloaded images

Downloaded images are saved in `./images/full/` using a SHA1 hash of their URLs for the file names. Images are 640 pixels in width and of variable heights depending on the aspect ratio of each image.

## Autothrottle

Crawling speed is automatically throttled to avoid getting banned. For more details, see the [AutoThrottle extension section](https://doc.scrapy.org/en/latest/topics/autothrottle.html) in Scrapy's documentation.

## Scrape history

If the scraping process is taking too long to complete, the spider process can be killed by pressing CTRL+C twice. Unique shortcodes of crawled posts are saved in `./<hashtag>.csv` in CSV format. You may run the spider again without it re-downloading scraped images.

## Requirements

* Python 3.5+
* Scrapy

      $ pip install scrapy
