import re
import sys
import uuid
import requests
from tqdm import tqdm
from time import sleep
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed


def getPage(url):
	response = ""
	attempter = 0

	while response == "" and attempter < 5:
		try:
			response = requests.get(url)
		except requests.exceptions.TooManyRedirects:
			#print(f"Received too many redirects for {url}")
			attempter += 1
			sleep(10)

	if response:
		response.encoding = response.apparent_encoding
		content = response.text
		return content
	else:
		return "Keno"


def processUrl(url, length=2):
	content = getPage(url)
	
	if content == "Keno": 
		return []

	words = []
	textWithoutTags = BeautifulSoup(content, "lxml").text
	textWithoutSymbols = re.sub("[&\/\\#,+()$~%.'\":*?<>{}]+", " ", textWithoutTags)
	myWords = re.findall("[ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρσςτυφχψωΆΈΉΊΌΎΏάέήίόύώϊϋΐΰΪΫ]+", textWithoutSymbols)

	for word in myWords:
		wordparts = re.findall("[ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΆΈΉΊΌΎΏΪΫ][^ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΆΈΉΊΌΎΏΪΫ]*", word)
		if len(wordparts) > 1:
			myWords.remove(word)
			myWords.extend(wordparts)

	if myWords:
		words = [word for word in myWords if len(word) > length]

	return list(set(words))


def chunkify(original, numberOfItemsInChunk):
	for i in range(0, len(original), numberOfItemsInChunk):
		yield original[i:i + numberOfItemsInChunk]


def main():

	allwords = []
	urls = []
	numberOfChunks = 1
	leaveFlag = False

	with open("out-urls.txt") as myfile:
		for line in myfile:
			urls.append(line.strip())

	if len(urls) <= 10000:
		pass
	else:
		numberOfChunks = len(urls) // 10000 + 1

	urlChunks = chunkify(urls, 10000)
	iteration = 1

	for urlChunk in urlChunks:

		with ThreadPoolExecutor(max_workers=1) as executor:
			tasks = {executor.submit(processUrl, url): url for url in urlChunk}

			try:
				completed = as_completed(tasks)

				if iteration == numberOfChunks:
					leaveFlag = True

				if numberOfChunks == 1:
					completed = tqdm(completed, total=len(urlChunk), desc="{0}".format("Progress"), dynamic_ncols=True, leave=leaveFlag)

				else:
					completed = tqdm(completed, total=len(urlChunk), desc="{0}".format("Progress {0}/{1}".format(iteration, numberOfChunks)), dynamic_ncols=True, leave=leaveFlag)

				for task in completed:
					result = task.result()

					if result is not None:
						allwords.extend(result)

			except KeyboardInterrupt:
				completed.close()
				print("\n[*]-Received keyboard interrupt! Shutting down...\n")
				executor.shutdown(wait=False)
				exit(-1)

		with open(f"./tmp/{str(uuid.uuid4())}.txt", "w") as outfile:
			for word in list(set(allwords)):
				outfile.write(f"{word}\n")

		iteration += 1
		allwords = []


if __name__ == "__main__":
	main()