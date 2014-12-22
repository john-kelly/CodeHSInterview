# -*- coding: utf-8 -*-

# Scrapy settings for CodeHSWikiBot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'CodeHSWikiBot'

SPIDER_MODULES = ['CodeHSWikiBot.spiders']
NEWSPIDER_MODULE = 'CodeHSWikiBot.spiders'

DUPEFILTER_CLASS = 'CodeHSWikiBot.custom_filters.DupeFilter'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'CodeHSWikiBot (+http://www.yourdomain.com)'
