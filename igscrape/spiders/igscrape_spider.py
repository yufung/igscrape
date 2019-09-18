# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
from igscrape.items import IgscrapeItem
import json
import os

class IgSpider(scrapy.Spider):
    name = "igspider"

    def __init__(self, tag=None, country_code=None):
        self.tag = tag
        # Country code follows ISO 3166-1 alpha-2 codes
        self.country_code = country_code
        # Ask for tag argument if it is not passed by user
        if self.tag == None:
            self.tag = input("Name of tag? ")
        self.hist_path = self.tag + '.csv'
        self.load_history()

    def load_history(self):
        # Initialize empty set for shortcodes if history file does not exist
        if not os.path.exists(self.hist_path):
            self.shortcode_hist = set()
            return
        # Load shortcodes from history file into a set
        else:
            with open(self.hist_path, 'r') as f:
                self.shortcode_hist = set(f.read().split(';'))

    def write_history(self):
        # Write shortcodes to history file in csv format
        with open(self.hist_path, 'w') as f:
            f.write(';'.join(self.shortcode_hist))
            
    def start_requests(self):
        url = 'https://www.instagram.com/explore/tags/' + self.tag + '/?__a=1'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        output = json.loads(response.text)
        has_next_page = output['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
        edges = output['graphql']['hashtag']['edge_hashtag_to_media']['edges']
        for edge in edges:
            shortcode = edge['node']['shortcode']
            if shortcode in self.shortcode_hist:
                # Do nothing if shortcode is in history set
                pass
            else:
                # Add shortcode to history set
                self.shortcode_hist.add(shortcode)
                # Follow link to post
                yield scrapy.Request('https://www.instagram.com/p/' + shortcode + '/?__a=1', callback=self.parse_post)

        if has_next_page:
            end_cursor = output['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
            # Follow link to next page
            yield scrapy.Request('https://www.instagram.com/explore/tags/' + self.tag + '/?__a=1&max_id=' + end_cursor, self.parse)
            
        # Save shortcode history
        self.write_history()

    def parse_post(self, response):
        item = IgscrapeItem()
        output = json.loads(response.text)
        try:
            address = json.loads(output['graphql']['shortcode_media']['location']['address_json'])
        except:
            address = {'country_code': None}
        if address['country_code'] == self.country_code or self.country_code == None:
            # If post has multiple photos
            try:
                edges = output['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
                image_paths = [edge['node']['display_resources'][0]['src'] for edge in edges]
                item['image_urls'] = image_paths
                yield item
            # If post only has one photo
            except:
                item['image_urls'] = [output['graphql']['shortcode_media']['display_resources'][0]['src']]
                yield item
