# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class JpNeedsSpider(scrapy.Spider):
    name = 'jp_needs'
    allowed_domains = ['RGF.com']
    start_urls = []
    for i in range(1, 1340):
        url_i = 'https://cn.japanese-jobs.com/jobs?page=' + str(i)
        start_urls.append(url_i)


    def parse(self, response):
        if response.url in self.start_urls:
            for href in response.xpath('//p[@class="jj-cassette__heading is-pc"]/a/@href').extract():
                yield Request(href, dont_filter=True)
        else:
            url = response.url
            title = response.xpath('//h1/text()').extract_first()
            release_time = response.xpath('//span[@class="jj-pageHeader__date"]/text()').extract_first().split("：")[1].split("～")[0]
            status = response.xpath('//li[@class="jj-pageHeader__btn"]//span[@class="jj-btn__text"]/text()').extract_first()
            if response.xpath('//p[@class="jj-pageHeader__price"]/span/text()').extract_first()=="需要确认/非公开":
                price_highest = "需要确认/非公开"
                price_lowest = "需要确认/非公开"
            else:
                price_lowest = int(float(response.xpath('//p[@class="jj-pageHeader__price"]/span/text()').extract_first().split("K")[0])*1000)
                price_highest = int(float(response.xpath('//p[@class="jj-pageHeader__price"]/span/text()').extract_first().split(" 〜 ")[1].split("K")[0])*1000)
            company = response.xpath('//li[@class="jj-pageHeader__company"]/text()').extract_first()
            location_city = response.xpath('//li[@class="jj-pageHeader__place"]/text()').extract()[1].split("\n")[2].split(" ")[18]
            experience = response.xpath('//li[@class="jj-pageHeader__level"]/text()').extract()[1].split("\n")[2].split("：")[1]
            career_type = response.xpath('//td[@class="jj-table__contents"]/text()').extract()[0]
            field_big = response.xpath('//td[@class="jj-table__contents"]/text()').extract()[1].split("\n")[0]
            field_small = response.xpath('//td[@class="jj-table__contents"]/text()').extract()[1].split("\n")[1].strip(" ")
            position_level = response.xpath('//td[@class="jj-table__contents"]/text()').extract()[3]
            needs = response.xpath('//td[@class="jj-table__contents"]/text()').extract()[4]
            time_wanted = response.xpath('//td[@class="jj-table__contents"]/text()').extract()[5]
            language_must = response.xpath('//td[@class="jj-table__contents"]/p/text()').extract_first()
            language_hope = response.xpath('//td[@class="jj-table__contents"]/text()').extract()[7].strip("\n").strip(" ")
            location_detail = response.xpath('//div[@class="jj-detail__contents"]//a[contains(@class,"jj-detail__map")]/../text()').extract_first().strip("\n").strip(" ")
            wellfare = response.xpath('//td[@class="jj-table__contents"]/text()').extract()[9:]
            job_detail = response.xpath('//div[@class="jj-detail__contents"]/p/text()').extract()

            yield {
                "职位链接": url,
                "职位名": title,
                "发布时间": release_time,
                "招聘状态": status,
                "最低薪资": price_lowest,
                "最高薪资": price_highest,
                "公司名": company,
                "工作地": location_city,
                "经验要求": experience,
                "职位种类": career_type,
                "行业大类别": field_big,
                "行业小类别": field_small,
                "岗位级别": position_level,
                "招聘人数": needs,
                "希望入职时间": time_wanted,
                "必须语言能力": language_must,
                "希望语言能力": language_hope,
                "详细地址": location_detail,
                "福利待遇": wellfare,
                "职位详述": job_detail
            }