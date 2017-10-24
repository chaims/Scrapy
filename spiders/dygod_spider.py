# -*- coding: UTF-8 -*-  
import scrapy
import urllib
from scrapyLess.items import ScrapylessItem

class DygodSpider(scrapy.Spider):
	
	name = "dygod"
	allowed_domains = ["dygod.net"]
	start_urls = ["http://www.dygod.net"]
    
    #一级列表解析
	def parse(self,response):
		# menu_list = ["/html/gndy/dyzz/index.html","/html/gndy/china/index.html","/html/gndy/rihan/index.html","/html/gndy/oumei/index.html"]
		menu_list = ["/html/gndy/dyzz/index.html"]
		for url in menu_list:
			yield scrapy.Request(self.start_urls[0]+url,callback=self.parse_list)
		# for sel in response.css('#menu .contain li a'):
		# 	if (sel.xpath('.//text()').extract_first()) not in exlist:
		# 		menu_url = self.start_urls[0]+sel.xpath('.//@href').extract_first()
		# 		yield scrapy.Request(menu_url,callback=self.parse_list)
	#二级列表解析	
	def parse_list(self,response):
		for sel in response.css('.co_content8 ul table a[title]'):
			full_url = self.start_urls[0] + sel.xpath('.//@href').extract_first()
			request = scrapy.Request(full_url,callback=self.parse_detail)
			request.meta['scrapy_url'] = full_url
			yield request
		for page in response.css('.co_content8 div[class="x"] select option'):
			print page.xpath('.//@value').extract_first()	
	#电影详情解析
	def parse_detail(self,response):
		obj = ScrapylessItem()
		preKey = ''
		obj['scrapy_url'] = response.meta['scrapy_url']
		tmpKey = ["starring","desc"]
		for sel in response.css('.co_area2 #Zoom p'):
			if sel.xpath('.//img').extract_first() is None:
				tmpText = sel.xpath('.//text()').extract_first()
				objKey = self.find_dict_name(tmpText)
				if objKey:
					preKey = objKey
					obj[objKey] = tmpText
				else:
					if preKey in tmpKey:
						obj[preKey] = obj[preKey] + tmpText
			else:
				obj["poster"] = sel.xpath('.//img/@src').extract_first()

		downloadurl = response.css('.co_area2 #Zoom table a::attr(href)').extract_first()
		obj["downloadurl"] = self.thunder_encode( urllib.quote( downloadurl.encode('utf-8') ) )
		yield obj
	#对应dict项
	def find_dict_name(self,content):
		objDict = {
		    "cname":"◎译　　名",
		    "ename":"◎片　　名",
		    "year":"◎年　　代",
		    "address":"◎产　　地",
		    "catogray":"◎类　　别",
		    "lan":"◎语　　言",
		    "subtitle":"◎字　　幕",
		    "showdate":"◎上映日期",
		    "db_score":"◎豆瓣评分",
		    "IMDb_score":"◎IMDb评分",
		    "file_type":"◎文件格式",
		    "movie_size":"◎视频尺寸",
		    "file_size":"◎文件大小",
		    "movie_mins":"◎片　　长",
		    "director":"◎导　　演",
		    "starring":"◎主　　演",
		    "desc":"◎简　　介",
		    "clipimgs":"◎影片截图"
		}
		for key in objDict:
			if objDict[key] in content.encode('UTF-8'):
				return key
		return ''
	#解析下载地址
	def utf16to8( self,st ):
		out = ''
		for letter in st:
			c = ord(letter)
			if (c >= 0x0001) and (c <= 0x007F):
				out += letter
			elif c > 0x07FF:
				out += chr(0xE0 | ((c >> 12) & 0x0F))
				out += chr(0x80 | ((c >>  6) & 0x3F))
				out += chr(0x80 | ((c >>  0) & 0x3F))
			else:
				out += chr(0xC0 | ((c >>  6) & 0x1F))
				out += chr(0x80 | ((c >>  0) & 0x3F))
		return out
	#解析下载地址	
	def base64_encode_chars(self,st):
		base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";	
		ln = len(st)
		n = 0
		out = ''
		while n < ln:
			c1 = ord(st[n]) & 0xff;
			n += 1
			if n == ln:
			    out += base64EncodeChars[(c1 >> 2)]
			    out += base64EncodeChars[((c1 & 0x3) << 4)]
			    out += "==";
			    break;
			c2 = ord(st[n])
			n += 1
			if n == ln:
			    out += base64EncodeChars[(c1 >> 2)]
			    out += base64EncodeChars[((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4)]
			    out += base64EncodeChars[((c2 & 0xF) << 2)]
			    out += "=";
			    break;
			c3 = ord(st[n])
			n += 1
			out += base64EncodeChars[(c1 >> 2)]
			out += base64EncodeChars[(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4))]
			out += base64EncodeChars[(((c2 & 0xF) << 2) | ((c3 & 0xC0) >>6))]
			out += base64EncodeChars[(c3 & 0x3F)]

		return out
	#解析下载地址
	def thunder_encode(self,url):
		thunderPrefix = "AA"
		thunderPosix = "ZZ"
		thunderTitle = "thunder://"
		thunderUrl = thunderTitle + self.base64_encode_chars(self.utf16to8(thunderPrefix + url + thunderPosix))
		return thunderUrl	