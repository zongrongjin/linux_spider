from scrapy.commands import ScrapyCommand
from scrapy.crawler import CrawlerRunner
from scrapy.utils.conf import arglist_to_dict
import logging

class MyCommand(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all spiders'

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")
    
    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UserWarning("Invalid -a value, use -a NAME=VALUE", print_help=False)

    def run(self, args, opts):
        spider_loader = self.crawler_process.spider_loader
        total_list = list(args) + spider_loader.list()
        for spider_name in total_list:
            logging.debug('scrapy crawl all is running, %s begin now' % (spider_name))
            self.crawler_process.crawl(spider_name, **opts.spargs)
        self.crawler_process.start()