import fileinput
import re

# Function phase1 reads a text file from stdin of tweets in
# XML format and creates 3 files, terms.txt, dates.txt, and
# tweets.txt where each line in terms.txt is of the form
# term:tweet_id, each line in dates.txt is of the form
# tweet_date:tweet_id, and each line in tweets.txt is of the
# form tweet_id:tweet, where tweet is the full tweet record

def phase1():
	termsFile = open('terms.txt', 'w')
	datesFile = open('dates.txt', 'w')
	tweetsFile = open('tweets.txt', 'w')
	for record in fileinput.input():
		word = record.split()
		# Skip the first 2 lines
		if word[0] == '<status>':
			# write the tweets and dates dates
			id = word[1][4:13]
			tweetsFile.write(id + ':' + record)
			date = word[2][12:22]
			datesFile.write(date + ':' + id + '\n')
			
			# remove the <text> tag
			word[3] = word[3][6:]
			
			# Go over the tweet text
			lastWord = False
			nameIndex = 5
			for word2 in word[3:]:
				nameIndex += 1

				# Check if special characters are included in the word
				beginSpCharIndex = word2.find('&#')
				while beginSpCharIndex >= 0:
					# Check for the ; 
					endSpCharIndex = word2.find(';', beginSpCharIndex)
					if endSpCharIndex >= 0:
						# Check if there is a number between &# and ;
						try:
							int(word2[beginSpCharIndex+2:endSpCharIndex])
							# Found a special character, remove it and check the rest of the word
							word2 = word2.replace(word2[beginSpCharIndex:endSpCharIndex+1], '')
							beginSpCharIndex = word2.find('&#', beginSpCharIndex)
						except ValueError:
							# Not a special character, skip it and check the rest of the word
							beginSpCharIndex = word2.find('&#', endSpCharIndex+1)
					else:
						# Didn't find a ; so skip the &# and check the rest of the word
						beginSpCharIndex = word2.find('&#', beginSpCharIndex + 2)
				
				# Check for </text> tag
				if len(word2) >= 7 and word2[-7:] == '</text>':
					word2 = word2[:-7]
					lastWord = True

				# The words that have reached here are will be terms if length
				# is still greater than 2 once splitting on non [a-zA-Z0-9_]
				for word3 in re.split('[^a-zA-Z0-9_]', word2):
					if len(word3) > 2:
						# Found a term
						termsFile.write('t-' + word3.lower() + ':' + id + '\n')
				if lastWord:
					break
			
			# remove the <name> tag
			word[nameIndex] = word[nameIndex][6:]
			
			# Go over the name text
			lastWord = False
			locationIndex = nameIndex
			for word2 in word[nameIndex:]:
				locationIndex += 1
				
				# Check if special characters are included in the word
				beginSpCharIndex = word2.find('&#')
				while beginSpCharIndex >= 0:
					# Check for the ; 
					endSpCharIndex = word2.find(';', beginSpCharIndex)
					if endSpCharIndex >= 0:
						# Check if there is a number between &# and ;
						try:
							int(word2[beginSpCharIndex+2:endSpCharIndex])
							# Found a special character, remove it and check the rest of the word
							word2 = word2.replace(word2[beginSpCharIndex:endSpCharIndex+1], '')
							beginSpCharIndex = word2.find('&#', beginSpCharIndex)
						except ValueError:
							# Not a special character, skip it and check the rest of the word
							beginSpCharIndex = word2.find('&#', endSpCharIndex+1)
					else:
						# Didn't find a ; so skip the &# and check the rest of the word
						beginSpCharIndex = word2.find('&#', beginSpCharIndex + 2)
				
				# Check for </text> tag
				if len(word2) >= 7 and word2[-7:] == '</name>':
					word2 = word2[:-7]
					lastWord = True

				# The words that have reached here are will be terms if length
				# is still greater than 2 once splitting on non [a-zA-Z0-9_]
				for word3 in re.split('[^a-zA-Z0-9_]', word2):
					if len(word3) > 2:
						# Found a term
						termsFile.write('n-' + word3.lower() + ':' + id + '\n')
				if lastWord:
					break
			
			# remove the <location> tag
			word[locationIndex] = word[locationIndex][10:]
			
			# Go over the location text
			lastWord = False
			for word2 in word[locationIndex:]:
				# Check if special characters are included in the word
				beginSpCharIndex = word2.find('&#')
				while beginSpCharIndex >= 0:
					# Check for the ; 
					endSpCharIndex = word2.find(';', beginSpCharIndex)
					if endSpCharIndex >= 0:
						# Check if there is a number between &# and ;
						try:
							int(word2[beginSpCharIndex+2:endSpCharIndex])
							# Found a special character, remove it and check the rest of the word
							word2 = word2.replace(word2[beginSpCharIndex:endSpCharIndex+1], '')
							beginSpCharIndex = word2.find('&#', beginSpCharIndex)
						except ValueError:
							# Not a special character, skip it and check the rest of the word
							beginSpCharIndex = word2.find('&#', endSpCharIndex+1)
					else:
						# Didn't find a ; so skip the &# and check the rest of the word
						beginSpCharIndex = word2.find('&#', beginSpCharIndex + 2)
				
				# Check for </text> tag
				if len(word2) >= 11 and word2[-11:] == '</location>':
					word2 = word2[:-11]
					lastWord = True

				# The words that have reached here are will be terms if length
				# is still greater than 2 once splitting on non [a-zA-Z0-9_]
				for word3 in re.split('[^a-zA-Z0-9_]', word2):
					if len(word3) > 2:
						# Found a term
						termsFile.write('l-' + word3.lower() + ':' + id + '\n')
				if lastWord:
					break
					
if __name__ == "__main__":
	phase1()
