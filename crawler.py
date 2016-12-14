from bs4 import BeautifulSoup
import urllib
import urllib.parse
import urllib.request as ur
import os
import time
import csv
import time

def fetchLinks(sitecontent):
	linklist = [a.attrs.get('href') for a in sitecontent.select('a[href]')]
	print("{} links found".format(len(linklist)))
	return linklist

def fetchInfo(sitecontent):
	infoDiv = sitecontent.find_all('div', {'class':"page product-details-page"})
	if len(infoDiv) > 0:
		name = getNames(infoDiv)
		price = getPrice(sitecontent)
	else:
		return "Null"
	return [name, price]

def getNames(productInfo):
	productName = str(productInfo[0].find_all('h1')[0]).split(">")[1].split("<")[0]
	productName = productName.strip()
	if "&amp;" in productName:
		productName = productName.replace("&amp;","&")
	print(productName)
	return productName
	
	
def getPrice(soup):
	scriptList = soup.find_all('script', {'type':"text/javascript"})
	for i in range(len(scriptList)):
		scriptList[i] = str(scriptList[i])
		if "] = new Array(" in scriptList[i]:
			pos = scriptList[i].index("] = new Array(")
			price = scriptList[i][pos + 14:].split(",")[0]
			return price

	
	
def defragURLs(alist, url):
	for i in range(len(alist)):
		alist[i] =  urllib.parse.urldefrag(alist[i])[0]
		
	for i in range(len(alist)):
		if bool(urllib.parse.urlparse(alist[i]).netloc) != True:
			alist[i] = urllib.parse.urljoin(url, alist[i])
	return alist
	
def mergeLinks(newList, oldList, url):
	for link in newList:
		if "." not in link[-5:]:
			if link not in oldList:
				if url in link:
					oldList.append(link)	
	return oldList
	
url = "https://vic.estore.thirstycamel.com.au/"	
linkList = [url]
urlsSearched = 0

timestr = time.strftime("%Y%m%d-%H%M%S")

while len(linkList) > urlsSearched:
	try:
		searchingURL = linkList[urlsSearched]
		
		print()
		print("Searching {}".format(searchingURL))
		r = ur.urlopen(searchingURL).read()
		sitecontent = BeautifulSoup(r, "html.parser")
		newLinks = fetchLinks(sitecontent)
		newLinks = defragURLs(newLinks, url)
		mergeLinks(newLinks, linkList, url)
		information = fetchInfo(sitecontent)
		print(information)
		if information != "Null":
			with open(timestr + '_TC.csv', "a", newline='') as csvfile:
				writer = csv.writer(csvfile, delimiter=',')
				writer.writerow(information)
		urlsSearched += 1
		print("{} links have been searched out of {}".format(urlsSearched, len(linkList)))
	except:
		print("Error")
		print(err)
		continue
print()
print()
print(linkList[-1])