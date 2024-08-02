import requests
from bs4 import BeautifulSoup
import csv
import pandas


def scrapePage(user):
	allPagesScraped = False
	page = 0
	filmsWatched = 0
	filmList = []
	yearList = []
	ratingList = []

	while not allPagesScraped:
		if page == 0:
			page += 1
			response = requests.get("https://letterboxd.com/" + user + "/films/diary/")
			soup = BeautifulSoup(response.text, 'html.parser')
			titleData = soup.find_all('h3', class_="headline-3 prettify")
			for title in titleData:
				filmsWatched += 1
				title = str(title.text)
				filmList.append(title)

			ratingData = soup.find_all('span', class_="rating")
			for rating in ratingData:
				rating = str(rating.encode("UTF-8")[26:28])
				rating = rating.replace("b'", "")
				rating = rating.replace("'", "")
				rating = rating.replace('"', "")
				if rating == "an":
					rating = 0
				rating = int(rating) / 2
				ratingList.append(rating)

			yearData = soup.find_all('td', class_="td-released")
			for year in yearData:
				year = str(year.text)
				yearList.append(year)

		if page > 0:
			page += 1
			response = requests.get("https://letterboxd.com/" + user + "/films/diary/page/" + str(page) + "/")
			soup = BeautifulSoup(response.text, 'html.parser')
			titleData = soup.find_all('h3', class_="headline-3 prettify")
			for title in titleData:
				filmsWatched += 1
				title = str(title.text)
				filmList.append(title)

			ratingData = soup.find_all('span', class_="rating")
			for rating in ratingData:
				rating = str(rating.encode("UTF-8")[26:28])
				rating = rating.replace("b'", "")
				rating = rating.replace("'", "")
				rating = rating.replace('"', "")
				rating = int(rating) / 2
				ratingList.append(str(rating))

			yearData = soup.find_all('td', class_="td-released")
			for year in yearData:
				year = str(year.text)
				yearList.append(year)

		if filmsWatched % 50 != 0:
			break

	readDataSet()
	writeToDataBase(filmList, yearList, ratingList)


def readDataSet():
	with open("imdbData.csv", "r") as dataSet:
		reader = csv.DictReader(dataSet)
		for row in reader:
			print(row["Series_Title"])


def writeToDataBase(filmList, yearList, ratingList):
	diary = zip(filmList, yearList, ratingList)
	headers = ("Film Name", "Year Released", "Rating", "Genre")

	with open("filmDB.csv", "w", newline="") as file:
		writer = csv.writer(file)
		writer.writerow(headers)
		writer.writerows(diary)


scrapePage("fcribb7")
