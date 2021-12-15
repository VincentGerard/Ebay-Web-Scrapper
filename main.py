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
		userAgent ="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
		headers = { 'User-Agent' : userAgent}

		#HtmlSearchTags
		htmlItem = "ad-listitem lazyload-item"
		htmlDescription = "aditem-main--middle--description"
		htmlPrice = "aditem-main--middle--price"
		htmlEllipsis = "ellipsis"
		htmlImage = "imagebox"

		
		
		#Search all 50 pages
		while pageNumber <= 50:
			url = "https://www.ebay-kleinanzeigen.de/s-preis:" + str(minPrice) + ":/seite:" + str(pageNumber) +"/marklin/k0"
			result = requests.get(url,headers=headers, cookies=cookies)
			myPrint("URL = " + url)
			myPrint("StatusCode = " + str(result.status_code))

			html_text = result.text

			# Manual Testing when the website does not repond(to much spam?)
			#html_text = open("test.html", 'r').read()
			
			soup = BeautifulSoup(html_text, 'lxml')
			myPrint("Item Number = " + str(html_text.count(htmlItem)))
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
			pageNumber = pageNumber + 1
			sleep(5)
	except Exception as e:
			myPrint("Error exception caught!")
			myPrint(e)

if __name__ == "__main__":
	main()
