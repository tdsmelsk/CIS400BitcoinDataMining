# CIS400BitcoinDataMining
Final Project that utilizes a Mongo DB database and an API to perform sentiment analysis on Tweets related to Bitcoin

CIS 400 README

1. Install python 3.7 or higher.
2. Install pip and run the following commands in the prompt to download necessary packages.
		a. pip install twitter
		b. pip install pymongo 
		c. pip install PrettyTable
		d. pip install -U textblob
		c. pip install matplotlib
		e. pip install google
		f. pip install requests
		g. pip install dnspython
3. Open FinalProjectPt1.py and FinalProjectPt2.py in idle.
4. Run FinalPorjectPt1.py for x amount of time (program is hard coded to run for 8 hours, a few more hours 
than the stock market is open for daily, but the user can choose how long to run the program by 
altering the fullTime variable in the code. The fullTime variable is approximately the amount of seconds
the program will collect tweets for.)
5. Wait for FinalProjectPt1.py to complete. This will be denoted by the following in output:
	done. 
	xXx
6. Run FinalProjectPt2.py to see table for percent of positive negative and neutral tweets for the
day as well as graphs that show TSS scores for the total amount of days the program has been run. 
		-**Note**: FinalProjectPt2.py is a separate file so that it can be run before 
		FinalProjectPt1.py is finished running if the user desires. If this is the case it will analyze 
		all data in the datbase to give percents and a score but will allow FinalProjectPt1.py to keep 
		collecting tweet data without resetting the database.  
