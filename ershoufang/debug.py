from scrapy import cmdline
import os
import sys

paths = os.path.dirname(os.path.abspath(__file__))
sys.path.append(paths)
cmdline.execute('scrapy crawl fangtianxia'.split(' '))