from http import cookiejar
from time import sleep
from bs4 import BeautifulSoup
import io
from bs4.dammit import html_meta
import requests
from functions import *
import datetime
import configparser
import json
from http.cookies import SimpleCookie
import os.path

"""
Max page = 50
Cookies in congif files must be with ';' separator, juste copy paste google chrome cookies for best use
"""

def main():
	try:
		#Test for custom configs
		if os.path.isfile("config.json"):
			#Load Config
			with open('config.json', 'r') as f:
				config = json.load(f)
				myPrint("Loading custom config")
		else:
			#Load Default config
			with open('default.json', 'r') as f:
				config = json.load(f)
				myPrint("Loading default config")

		minPrice = config['minPrice']
		
		googleChromeCookie = config['googleChromeCookie']
		cookie = SimpleCookie()
		cookie.load(googleChromeCookie)
		#Create custom cookie dictionairy
		cookies = {}
		for key, morsel in cookie.items():
			cookies[key] = morsel.value

		#Variables
		pageNumber = 0
		ebayUrl = "https://www.ebay-kleinanzeigen.de"
		userAgent ="Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
		headers = { 'User-Agent' : userAgent,'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*'}

		#HtmlSearchTags
		htmlItem = "ad-listitem lazyload-item"
		htmlDescription = "aditem-main--middle--description"
		htmlPrice = "aditem-main--middle--price"
		htmlEllipsis = "ellipsis"
		htmlImage = "imagebox"

		#Search all 50 pages
		while True:
			url = "https://www.ebay-kleinanzeigen.de/s-preis:" + str(minPrice) + ":/seite:" + str(pageNumber) +"/marklin/k0"
			result = requests.Session().get(url,headers=headers, cookies=cookies)
			myPrint("URL = " + url)
			myPrint("StatusCode = " + str(result.status_code))

			html_text = result.text

			# Manual Testing when the website does not repond(to much spam?)
			#html_text = open("test.html", 'r').read()

			itemNumber = html_text.count(htmlItem)
			if itemNumber == 0:
				sleep(60)
			myPrint("Item Number = " + str(itemNumber))
			
			soup = BeautifulSoup(html_text, 'lxml')
			jobs = soup.find_all('li', class_ = htmlItem)

			for job in jobs:
				try:
					price = strToInt(job.find("p",htmlPrice).text)
					title = job.find("a", class_ = htmlEllipsis).text
					urlLink = ebayUrl + job.find("a", class_ = htmlEllipsis)['href']
					imageLink = job.find("div", class_ = htmlImage)['data-imgsrc']
				except KeyError as k:
					imageLink = ""
				
				myPrint("Page  = " + str(pageNumber))
				myPrint("Title = " + title)
				myPrint("Price = " + str(price))
				myPrint("Url   = " + urlLink)
				myPrint("Image = " + imageLink + "\n")
			sleep(60 * 5)
	except Exception as e:
			myPrint("Error exception caught!")
			myPrint(e)

if __name__ == "__main__":
	main()
