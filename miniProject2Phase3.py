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
	
	# Compound expression
	if len(query.split()) > 1:
		# Keep only the ids that occur in each result set
		# Go through each result in the first result set and check if it is in all the others
		# If it is then add it to the final result set
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
				finalResults.append(result)
		return finalResults
	else:
		return results[0]
		
def searchTerms(query, termsDB):
	partialMatch = False
	keys = []
	results = []
	curs = termsDB.cursor()
	if query[-1] == '%':
		partialMatch = True
	
	if len(query) >= 5 and query[:5] == 'text:':
		keys.append('t-' + query[5:])
	elif len(query) >= 5 and query[:5] == 'name:':
		keys.append('n-' + query[5:])
	elif len(query) >= 9 and query[:9] == 'location:':
		keys.append('l-' + query[9:])
	else:
		keys.append('t-' + query)
		keys.append('n-' + query)
		keys.append('l-' + query)
	
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
	if query[0] == ':':
		pass
	elif query[0] == '<':
		pass
	else:
		pass

def getTweets(results, tweetsDB):
	return(results)
	
def displayResults(results):
	for result in results:
		print(result)
	
if __name__ == "__main__":
	phase3()