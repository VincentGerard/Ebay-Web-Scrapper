from bs4 import BeautifulSoup
import io
from bs4.dammit import html_meta
import requests
from functions import *

"""
Max page = 50
"seite:50" => Add page to search
"""

def main():
	minPrice = 500
	ebayUrl = "https://www.ebay-kleinanzeigen.de"
	baseUrl = "https://www.ebay-kleinanzeigen.de/s-preis:"
	endUrl = ":/marklin/k0"
	url = baseUrl + str(minPrice) + endUrl
	userAgent ="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
	headers = { 'User-Agent' : userAgent}

	htmlItem = "ad-listitem lazyload-item"
	htmlDescription = "aditem-main--middle--description"
	htmlPrice = "aditem-main--middle--price"
	htmlEllipsis = "ellipsis"
	htmlImage = "imagebox"

	try:
		print("URL = " + url)

		result = requests.get(url,headers=headers)
		print("Result = + " + str(result.status_code))

		html_text = result.text

		# Manual Testing when the website does not repond(to much spam?)
		#html_text = open("test.html", 'r').read()
		
		soup = BeautifulSoup(html_text, 'lxml')
		print(html_text.count(htmlItem))
		jobs = soup.find_all('li', class_ = htmlItem)

		for job in jobs:
			try:
				price = strToInt(job.find("p",htmlPrice).text)
				title = job.find("a", class_ = htmlEllipsis).text
				urlLink = ebayUrl + job.find("a", class_ = htmlEllipsis)['href']
				imageLink = job.find("div", class_ = htmlImage)['data-imgsrc']
			except KeyError as k:
				imageLink = ""
			

			print("\nTitle = " + title)
			print("Price = " + str(price))
			print("Url   = " + urlLink)
			#print(imageLink)
			print("Image = " + imageLink)
	except Exception as e:
		print("Error exception caught!")
		print(e)


if __name__ == "__main__":
	main()
