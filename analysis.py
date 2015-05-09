import csv
from scipy import stats
import numpy as np
import re

babyCSV = 'BabyNames.csv'
forbesCSV = 'ForbesRankings.csv'
googleCSV = 'GoogleTrends.csv'

class Analysis:
	def __init__(self, babyCSV, forbesCSV, googleCSV):
		self.babyNamesListRaw = None
		self.forbesRankingsListRaw = None
		self.googleTrendsListRaw = None
		with open(babyCSV, 'rb') as f:
		    reader = csv.reader(f)
		    self.babyNamesListRaw = list(reader)

		# year, rank, boy_name, % of boys, girl_name, % of girls
		# print babyNamesList

		with open(forbesCSV, 'rU') as g:
		    reader = csv.reader(g)
		    self.forbesRankingsListRaw = list(reader)

		# year, rank, name
		# print forbesRankingsList

		with open(googleCSV, 'rU') as h:
		    reader = csv.reader(h)
		    self.googleTrendsListRaw = list(reader)


	def formatBabyRankDicts(self):
		retDict = {}
		# Create a list of lists for each year (2002-2014)
		for year in list(range(1999, 2014)):
			retDict[year] = {}

		for x in range(1, len(self.babyNamesListRaw)):
			itemYear = int(self.babyNamesListRaw[x][0])
			itemRank = self.babyNamesListRaw[x][1]
			itemBoyName = self.babyNamesListRaw[x][2]
			itemGirlName = self.babyNamesListRaw[x][4]
			if itemYear in retDict.keys():
				retDict.get(itemYear)[itemBoyName] = itemRank
				retDict.get(itemYear)[itemGirlName] = itemRank
		return retDict

	def formatBabyPercentageDicts(self):
		retDict = {}
		# Create a list of lists for each year (2002-2014)
		for year in list(range(1999, 2014)):
			retDict[year] = {}

		for x in range(1, len(self.babyNamesListRaw)):
			itemYear = int(self.babyNamesListRaw[x][0])
			itemBoyPercentage = self.babyNamesListRaw[x][3]
			itemBoyPercentage = re.sub('[^0-9\.]+', '', itemBoyPercentage)
			itemBoyPercentage = float(itemBoyPercentage)
			itemBoyName = self.babyNamesListRaw[x][2]
			itemGirlPercentage = self.babyNamesListRaw[x][5]
			itemGirlPercentage = re.sub('[^0-9\.]+', '', itemGirlPercentage)
			itemGirlPercentage = float(itemGirlPercentage)
			itemGirlName = self.babyNamesListRaw[x][4]
			if itemYear in retDict.keys():
				retDict.get(itemYear)[itemBoyName] = itemBoyPercentage
				retDict.get(itemYear)[itemGirlName] = itemGirlPercentage
		return retDict

	def formatForbesDicts(self):
		retDict = {}
		# Create a list of lists for each year (2002-2014)
		for year in list(range(1999, 2014)):
			retDict[year] = {}

		for x in range(1, len(self.forbesRankingsListRaw)):
			itemYear = int(self.forbesRankingsListRaw[x][0])
			itemRank = -1 * int(self.forbesRankingsListRaw[x][1])
			itemName = self.forbesRankingsListRaw[x][2]
			itemName = re.sub('[^a-zA-Z]+', ' ', itemName)
			itemName = itemName.split()[0]
			if itemYear in retDict.keys():
				retDict.get(itemYear)[itemName] = itemRank
		return retDict
	
	def formatForbesDiffDicts(self):
		retDict = {}
		forbesDict = formatForbesDict()
		for year in list(range(2000, 2014)):
			retDict[year] = {}
			for x in forbesDict.keys():
				oldYear = year - 1
				rankChange = (forbesDict.get(year)).get(x) - (forbesDict.get(oldYear)).get(x)
		return retDict

	def formatBabyPercentageDiffDicts(self):
		retDict = {}
		return retDict

	def listAnalysis(self, year, aForbesDict, aBabyDict):
		forbesRank = []
		babyPercentage = []
		nameList = []
		forbesDict = aForbesDict
		babyDict = aBabyDict
		for name in forbesDict.get(year).keys():
			if name in babyDict.get(year).keys():
				nameList.append(name)
				forbesRank.append((forbesDict.get(year)).get(name))
				babyPercentage.append((babyDict.get(year)).get(name))
		return (nameList, np.array(forbesRank), np.array(babyPercentage))

	# def diffListAnalysis(self, year):

# year, rank, name category
# print googleTrendsList

def main():
	x = Analysis(babyCSV, forbesCSV, googleCSV)
	rawBaby = x.formatBabyPercentageDicts()
	rawForbes = x.formatForbesDicts()
	for year in range(2002, 2014):
		nameList, forbesRank, babyPercentage = x.listAnalysis(year, rawForbes, rawBaby)
		slope, intercept, r_value, p_value, std_err = stats.linregress(forbesRank, babyPercentage)
		print(str(year) + ": " + str(r_value))
	# print(x.rawListAnalysis(2002))
	# for i in range(len(babyList)):
	# 	slope, intercept, r_value, p_value, std_err = stats.linregress(forbesList[i], babyList[i])

if __name__ == "__main__":
	main()
	