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
		displayResults(results)
	
def parseAndSearch(query, termsDB, datesDB):
	if len(query) >= 4 and query[:4] == 'date':
		return searchDates(query[4:], datesDB)
	else:
		return searchTerms(query, termsDB)

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
			key = key[:-1].encode('ascii','ignore')
			results.append(curs.get(key, db.DB_DBT_PARTIAL, dlen=length(key), doff=0))
			result = curs.next()
			resultKey = result[0].decode('utf-8')
			while len(resultKey) >= len(key) and resultKey[:len(key)] == key:
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
def displayResults(results):
	for result in results:
		print(result)
	
if __name__ == "__main__":
	phase3()