from bsddb3 import db

def phase3():
	# Open the databases
	tweetsDB = db.DB()
	termsDB = db.DB()
	datesDB = db.DB()
	tweetsDB.open('tw.idx',None,db.DB_HASH,db.DB_CREATE)
	termsDB.open('te.idx',None,db.DB_BTREE,db.DB_CREATE)
	datesDB.open('da.idx',None,db.DB_BTREE,db.DB_CREATE)

	while (True):
		inp = input("Please enter a query or 'exit' to exit the program: ")
		if inp == 'exit':
			break

		results = parseAndSearch(inp, termsDB, datesDB)
		tweets = getTweets(results, tweetsDB)
		displayResults(tweets)

def parseAndSearch(query, termsDB, datesDB):
	results = []
	finalResults = []
	for expression in query.split():
		if len(expression) >= 4 and expression[:4] == 'date':
			results.append(searchDates(expression[4:], datesDB))
		else:
			results.append(searchTerms(expression, termsDB))

	# Compound expression, need to aggregate the results
	if len(query.split()) > 1:
		# Keep only the ids that occur in each result set
		# Go through each result in the first result set and check if it is in all the others
		# If it is then add it to the final result set
		finalResultsTemp = []
		for result in results[0]:
			foundAll = True
			for resultSet in results[1:]:
				found = False
				for rslt in resultSet:
					if result[1] == rslt[1]:
						found = True
						break
				if not found:
					foundAll = False
					break
			if foundAll:
				finalResultsTemp.append(result)
		for index1 in range(len(finalResultsTemp)):
			foundDuplicate = False
			for index2 in range(index1+1, len(finalResultsTemp)):
				if finalResultsTemp[index1][1] == finalResultsTemp[index2][1]:
				   foundDuplicate = True
			if not foundDuplicate:
			   finalResults.append(finalResultsTemp[index1])
	else:
		for index1 in range(len(results[0])):
			foundDuplicate = False
			print("DEBUG: ", results[0][index1])
			for index2 in range(index1+1, len(results[0])):
				if results[0][index1][1] == results[0][index2][1]:
				   foundDuplicate = True
			if not foundDuplicate:
			   finalResults.append(results[0][index1])
	return finalResults

def searchTerms(query, termsDB):
	partialMatch = False
	keys = []
	results = []
	curs = termsDB.cursor()
	if query[-1] == '%':
		partialMatch = True

	if len(query) >= 5 and query[:5] == 'text:':
		keys.append('t-' + query[5:].lower())
	elif len(query) >= 5 and query[:5] == 'name:':
		keys.append('n-' + query[5:].lower())
	elif len(query) >= 9 and query[:9] == 'location:':
		keys.append('l-' + query[9:].lower())
	else:
		keys.append('t-' + query.lower())
		keys.append('n-' + query.lower())
		keys.append('l-' + query.lower())

	if partialMatch:
		for key in keys:
			skey = key[:-1]
			key = key[:-1].encode('ascii','ignore')
			result = curs.set_range(key)
			if result:
				resultKey = result[0].decode('utf-8')
				while len(resultKey) >= len(skey) and resultKey[:len(key)] == skey:
					results.append(result)
					result = curs.next()
					resultKey = result[0].decode('utf-8')
	else:
		for key in keys:
			key = key.encode('ascii','ignore')
			result = curs.set(key)
			while result:
				results.append(result)
				result = curs.next_dup()

	curs.close()
	return results

def searchDates(query, datesDB):

	keys = []
	results = []
	curs = datesDB.cursor()

	if query[0] == ':':
		keys.append( query[1:])
		for key in keys:

			#key = bytes(key, 'utf-8')
			key = key.encode('ascii','ignore')

			result = curs.set_range(key)
			#print(result)
			while result:
				results.append(result)
				result = curs.next_dup()
	elif query[0] == '<':
		keys.append(query[1:])
		for key in keys:
			key = key.encode('ascii','ignore')

			result = curs.set_range(key)

			result = curs.prev()
			if  result is None:
				return results
			else:

				while result is not None:
					results.append(result)
					result = curs.prev()
	else:
		keys.append(query[1:])
		for key in keys:
			key = key.encode('ascii','ignore')
			result = curs.set_range(key)
			result = curs.next()
			if  result is None:
				return results
			else:

				while result is not None:
					results.append(result)
					result = curs.next()
	curs.close()
	print(results)
	return results

def getTweets(results, tweetsDB):
	tweets = []
	curs = tweetsDB.cursor()
	for result in results:
		tw = curs.set(result[1])
		if tw:
			tweets.append(tw)
	curs.close()
	return tweets

def displayResults(results):
	for result in results:
		print(result)

if __name__ == "__main__":
	phase3()
