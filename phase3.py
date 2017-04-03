from bsddb3 import db

# Function phase3 gives an interface for the user to query the database
# created in phase2.
def phase3():
	# Open the databases
	tweetsDB = db.DB()
	termsDB = db.DB()
	datesDB = db.DB()
	tweetsDB.open('tw.idx',None,db.DB_HASH,db.DB_CREATE)
	termsDB.open('te.idx',None,db.DB_BTREE,db.DB_CREATE)
	datesDB.open('da.idx',None,db.DB_BTREE,db.DB_CREATE)

	# Get the query from the user
	while (True):
		inp = input("Please enter a query or 'exit' to exit the program: ")
		if inp == 'exit':
			break

		# Parse the query and display the results
		results = parseAndSearch(inp, termsDB, datesDB)
		tweets = getTweets(results, tweetsDB)
		displayResults(tweets)

# Function parseAndSearch splits the query into individual expressions
# and gets the query results for each expression from the searchDates
# and searchTerms functions. Those results are then aggregated and
# duplicates removed. 
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
		# Remove duplicate tweets
		for index1 in range(len(finalResultsTemp)):
			foundDuplicate = False
			for index2 in range(index1+1, len(finalResultsTemp)):
				if finalResultsTemp[index1][1] == finalResultsTemp[index2][1]:
				   foundDuplicate = True
			if not foundDuplicate:
			   finalResults.append(finalResultsTemp[index1])
	else:
		# Remove duplicate tweets
		for index1 in range(len(results[0])):
			foundDuplicate = False
			for index2 in range(index1+1, len(results[0])):
				if results[0][index1][1] == results[0][index2][1]:
				   foundDuplicate = True
			if not foundDuplicate:
			   finalResults.append(results[0][index1])
	return finalResults

# Function searchTerms searches the termsDB database using query query
# and returns the results.
def searchTerms(query, termsDB):
	partialMatch = False
	keys = []
	results = []
	curs = termsDB.cursor()
	if query[-1] == '%':
		partialMatch = True

	# Create the keys
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
				# Scan and add results until the prefix is no longer found
				while len(resultKey) >= len(skey) and resultKey[:len(key)] == skey:
					results.append(result)
					result = curs.next()
					resultKey = result[0].decode('utf-8')
	else:
		for key in keys:
			key = key.encode('ascii','ignore')
			result = curs.set(key)
			# Add all the duplicates aswell
			while result:
				results.append(result)
				result = curs.next_dup()

	curs.close()
	return results

# Function searchDates searches the datesDB database using query query
# and returns the results.
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
	return results

# Function getTweets searches the tweetsDB database for the tweets
# with the ids in results and returns them.
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
		words = result[1].decode('utf-8').split()
		id = words[1][4:-5]
		date = words[2][12:-13]
		
		words[3] = words[3][6:]
		index_text = 3
		for word in words[3:]:
			if len(word) >= 7 and word[-7:] == '</text>':
				words[index_text] = words[index_text][:-7]
				break
			index_text = index_text + 1
		text = " ".join(words[3:index_text+1])
		retweet_count = words[index_text+1][15:-16]
		
		index_name_start = 0
		index_name_end = 0
		index = index_text + 2
		for word in words[index:]:
			if len(word) >= 6 and word[:6] == '<name>':
				index_name_start = index
				words[index] = words[index][6:]
			if len(word) >= 7 and word[-7:] == '</name>':
				index_name_end = index
				words[index] = words[index][:-7]
				break
			index = index + 1
		name = " ".join(words[index_name_start:index_name_end+1])

		index_location_start = 0
		index_location_end = 0
		index = index_name_end + 1
		for word in words[index:]:
			if len(word) >= 10 and word[:10] == '<location>':
				index_location_start = index
				words[index] = words[index][10:]
			if len(word) >= 11 and word[-11:] == '</location>':
				index_location_end = index
				words[index] = words[index][:-11]
				break
			index = index + 1
		location = " ".join(words[index_location_start:index_location_end+1])
		
		index_description_start = 0
		index_description_end = 0
		index = index_location_end + 1
		for word in words[index:]:
			if len(word) >= 13 and word[:13] == '<description>':
				index_description_start = index
				words[index] = words[index][13:]
			if len(word) >= 14 and word[-14:] == '</description>':
				index_description_end = index
				words[index] = words[index][:-14]
				break
			index = index + 1
		description = " ".join(words[index_description_start:index_description_end+1])
		
		index_url_start = 0
		index_url_end = 0
		index = index_description_end + 1
		for word in words[index:]:
			if len(word) >= 5 and word[:5] == '<url>':
				index_url_start = index
				words[index] = words[index][5:]
			if len(word) >= 6 and word[-6:] == '</url>':
				index_url_end = index
				words[index] = words[index][:-6]
				break
			index = index + 1
		url = " ".join(words[index_url_start:index_url_end+1])
		
		print("##################################################################")
		print("id: ", id)
		print("date: ", date)
		print("text: ", text)
		print("retweet count: ", retweet_count)
		print("name: ", name)
		print("location: ", location)
		print("description: ", description)
		print("url: ", url)

if __name__ == "__main__":
	phase3()
