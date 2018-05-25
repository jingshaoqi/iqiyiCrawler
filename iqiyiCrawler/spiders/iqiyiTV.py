# -*- coding: utf-8 -*-
import json
import re
import sys

import scrapy

reload(sys)
sys.setdefaultencoding('utf-8')


class IqiyiSpider(scrapy.Spider):
    name = 'iqiyiTV'
    start_urls = ["http://cache.video.iqiyi.com/jp/vi/638956700/6f7d21d9091f57c0e66ccb1df14867f4/"]
    # http://mixer.video.iqiyi.com/jp/mixin/videos/1033851800
    urls = "http://mixer.video.iqiyi.com/jp/recommend/videos?referenceId=1033851800&albumId=207771601&channelId=2&cookieId=496db0c22d9a27a875d612af58b6e7c6&withRefer=false&area=bee&size=36&type=video&pru=&locale=&userId=&playPlatform=PC_QIYI&isSeriesDramaRcmd="
    url = "http://www.iqiyi.com/v_19rrercswg.html"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse_index)
        # for url in self.start_urls:
        # yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        result = response.text.strip("var tvInfoJs=")
        # print(result)
        jj = json.loads(result)
        print(jj.get("albumQipuId"))
        # print(jj.get("keyword"))
        # print(jj.get("qiyiPlayStrategy"))
        # print(jj.get("tg"))
        # print(jj.get("info"))
        # print(jj.get("d"))
        # print(jj.get("ma"))
        # print(jj.get("nurl"))
        print(jj.get("videoQipuId"))
        # yield scrapy.Request(url=self.urls, callback=self.parse_index)

    def parse_index(self, response):
        result = response.text.strip("var tvInfoJs=")
        jj = json.loads(result)
        for tt in jj.get("mixinVideos"):
            url = tt.get("url")
            print(tt.get("description"))
            print(tt.get("tvId"))
            print(tt.get("albumId"))
            print(tt.get("crumbList")[1].get("title"))
            print(tt.get("crumbList")[2].get("title"))

            yield scrapy.Request(url=url, callback=self.parse_index)

    def parse_index(self, response):
        sel = scrapy.Selector(response)
        result = response.text
        # print(result)
        albumid = re.findall("param\['albumid']\s=\s(.*?);", result)
        tvid = re.findall("param\['tvid']\s=\s(.*?);", result)
        vid = re.findall("param\['vid']\s=\s(.*?);", result)
        print(albumid, tvid, vid)
        print(sel.xpath('//div[@class="playList-update-tip "]/p/text()')).extract_first(default="")
        titles = sel.xpath('//div[@data-tab-page="body"]/ul/li/a/@title').extract()
        print(len(titles))
