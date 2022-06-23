import re
import requests
from time import sleep
from urllib.parse import unquote_plus
from bs4 import BeautifulSoup


def getUrls(content, url):
	soup = BeautifulSoup(content, "html.parser")
	urls = []
	for link in soup.find_all("a"):
		relativeUrl = str(link.get("href"))
		if not relativeUrl.startswith("//"):
			resultingUrl = requests.compat.urljoin(url, relativeUrl)
			if resultingUrl.startswith("http://172.17.0.2/wikipedia_el_all_maxi_2022-05/"):
				urls.append(unquote_plus(resultingUrl).split("#")[0])
	return list(set(urls))


def getPage(url):
	response = ""
	attempter = 0

	while response == "" and attempter < 5:
		try:
			response = requests.get(url)
		except requests.exceptions.TooManyRedirects:
			print(f"Received too many redirects for {url}")
			attempter += 1
			sleep(10)

	if response:
		return response.text
	else:
		return "Keno"


def main():
	sites = []
	urlList = []
	url = "http://172.17.0.2/wikipedia_el_all_maxi_2022-05/A/%CE%A0%CF%8D%CE%BB%CE%B7:%CE%9A%CF%8D%CF%81%CE%B9%CE%B1"
	
	sites.append(url)

	while sites:
		sleep(0.1)
		toProcess = sites[0]
		urlList.append(toProcess)

		pageContent = getPage(toProcess)

		if pageContent != "Keno":
			newUrls = getUrls(pageContent, url)
		else:
			newUrls = []
		
		for aurl in newUrls:
			if aurl not in urlList:
				sites.append(aurl)

		sites.remove(toProcess)
		sites = list(set(sites))

		print(f"Sites to visit: {len(sites)} - My URLs so far: {len(urlList)}")

	print(len(urlList))
	with open("out-urls.txt", "w") as outfile:
		for url in urlList:
			outfile.write(f"{url}\n")


if __name__ == "__main__":
	main()










# docker run -v '/root/Desktop/wikitest:/data' -p 8888:80 kiwix/kiwix-serve 'wikipedia_el_all_maxi_2022-05.zim'