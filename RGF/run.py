from scrapy import cmdline

cmdline.execute("scrapy crawl jp_needs -o output.json".split())
# cmdline.execute("scrapy crawl jp_needs -o output_1.json -s FEED_EXPORT_ENCODING=utf-8".split())
# cmdline.execute("scrapy crawl jp_needs".split())