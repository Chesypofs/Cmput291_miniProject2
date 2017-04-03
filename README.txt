Cmput 291 Mini Project 2

William Hodgson
Irene Gao 
Shuaiqun Pan


This project includes 3 separate programs, phase1.py, phase2.py, and phase3.py.

Phase1 can be run using the phase1_script.sh script by the command:
	   phase1_script.sh <tweetsXML.txt>
where <tweetsXML.txt> is the name of a text file containing tweets in XML format.
Phase1 takes the <tweetsXML.txt> file, parses the included tweets and creates 3 files, tweets.txt, terms.txt, and dates.txt that are used in phase2.py to create the Berkeley DB databases.

Phase2 can be run using the phase2_script.sh script by the command:
	   phase2_script.sh
which first sorts and deletes duplicates in the tweets.txt, terms.txt, and dates.txt files created in phase1.py. It then creates 3 indexes, tw.idx on tweets with tweet ids as keys and the full tweet recod as data, te.idx on terms.txt with terms as keys and tweet ids as data, and da.idx on dates.txt with dates as keys and tweet ids as data.

Phase3 can be run on the command line using the command:
	   python3 phase3.py
Phase3 opens the databases created in phase2.py then allows the user to query the databases, returning the tweets that match the queries.

All 3 phases can be run using the command:
	allPhases_script.sh <tweetsXML.txt>
where <tweetsXML.txt> is the name of a text file containing tweets in XML format. This script will first run phase1.py, then phase2.py, and finally phase3.py.
