#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filename:         project2.py
# Name(s):          Alex Kerzner, Stuart Badger, Jonathan Hunt
# Class:            Cosc 480 (Data Science for Social Good)
# Assignment:       miniproject2 - Twitter Scrapulatirintegrating
# Date:             2017-March-03
# Description:      Scrapes twitter and parses data before presenting it in text and visualization

"""  Library Imports  """

# Python API library for Twitter
import tweepy

# Date and time functions
import datetime

# Dictionary
from collections import defaultdict,OrderedDict


# Graphing and math imports
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

"""  Program Settings  """

# Maximum is 48000
MAXIMUM_NUMBER_OF_TWEETS = 32 * 15 * 100

# How many tweets to print out, maximum, per statistic (where applicable)
MAX_TWEETS_TO_DISPLAY = 5

# How many users to print out, maximum, per statistic (where applicable)
MAX_USERS_TO_DISPLAY = 10

"""  Utility Functions  """

# Sort dictionary by values from greatest to least, then by key (alphabetically)
def sort_dictionary(dictionary):
	return OrderedDict(sorted(dictionary.items(), key=lambda item : (-item[1], item[0]),reverse=False))

# Prints sorted dictionary
def print_dictionary(dictionary):
	for key, value in dictionary.iteritems():
		print("%4i: %s" % (value, str(key)))

"""  Variable Initialization  """

# List of hashtags
LIST_OF_HASHTAGS = ["STEM","CSFORALL","EQUALITY","EQUITY","YOLO"]

# Data initialization
users = {}
user_followers = {}
tweets = {}
for tag in LIST_OF_HASHTAGS:
	tweets[tag] = []
	user_followers[tag] = {}
	users[tag] = defaultdict(int)

# Time range definition
before_time = datetime.datetime(2017,2,25,5,0,0)
after_time = datetime.datetime(2017,3,1,5,0,0)

"""  Credentials Loading  """

# Load credentials for authentication from ./tokens.txt
file = open("./tokens.txt", "r")
consumer_key = file.readline().strip()
consumer_secret = file.readline().strip()
app_key = file.readline().strip()
app_secret = file.readline().strip()

"""  Tweepy API Initialization  """

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(app_key, app_secret)

# Load credentials and command tweepy to wait after maxing out the rate limit
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

"""  Twitter Search Declaration  """


"""  Twitter Search Process  """

print "Beginning search. Press CTRL-C to finalize search without finishing."
print "After finalizing, results will be displayed."
print "This process may take a while"
print "For future reference, the start time is: " + str(datetime.datetime.now())
print "Estimated time to complete: 2-2.5 hours"
try:
	# Search for any of the five hashtags in the time range specified
	# Call it quits at 15*100*32=48000 tweets
	jtweets = tweepy.Cursor(api.search,q="#csforall OR #equality OR #equity OR #stem OR #yolo", count=100, since='2017-02-25',until='2017-03-02').items(MAXIMUM_NUMBER_OF_TWEETS)
	
	for jtweet in jtweets:
		# Drilldown to proper time range
		if (jtweet.created_at < before_time or jtweet.created_at >= after_time):
			# Skip if not in time range
			continue
		#
		# Obtain tweet data, only store useful data
		tweet = {}
		tweet["text"] = jtweet._json["text"]
		tweet["retweet_count"] = jtweet._json["retweet_count"]
		tweet["user"] = jtweet._json["user"]["screen_name"]
		tweet["created_at"] = jtweet.created_at
		tweet["hashtags"] = [hashtag["text"].upper() for hashtag in jtweet._json["entities"]["hashtags"]]
		tweet["favorite_count"] = jtweet._json["favorite_count"]
		tweet["followers_count"] = jtweet._json["user"]["followers_count"]
		#
		# Handle truncation because a tweet is a retweet
		tweet["is_retweet"] = "retweeted_status" in jtweet._json
		if tweet["is_retweet"]:
			# Get original tweet text and hashtags
			tweet["text"] = jtweet._json["retweeted_status"]["text"]
			tweet["hashtags"] = [hashtag["text"].upper() for hashtag in jtweet._json["retweeted_status"]["entities"]["hashtags"]]
		#
		# Classify tweets according to hashtag
		for tag in LIST_OF_HASHTAGS:
			if tag in tweet["hashtags"]:
				# Add tweet to list of tweets with specific tag
				tweets[tag].append(tweet)
				# Add another instance of the user who tweeted
				users[tag][tweet["user"]] += 1
				# Record the number of followers of the user
				user_followers[tag][tweet["user"]] = tweet["followers_count"]
except tweepy.TweepError:
	# If a TweepError occurs, stop. Most often due to the rate limit exceeded.
	# The rate limit is 15 api calls (approximately 15 pages, or 1500 tweets)
	# in a 15-minute window.
	print "Stopping - too many requests (TweepError)"
except StopIteration:
	# No more tweets. The search is finished!
	print "Finished"
except KeyboardInterrupt:
	# The user pressed CTRL-C, or maybe Delete
	print "Cancelling operation..."

"""  Statistics Functions  """

# Finds the most frequent user in the frequency list of users
def get_most_frequent_user(tag):
	top_users = []
	if users[tag].values() == []:
		# No results
		return (0, top_users)
	# Get maximum, and get all users with that maximum
	max_count = max(users[tag].values())
	for name, number in users[tag].iteritems():
		if number == max_count:
			top_users.append(name)
	return (max_count, top_users)

# Get user with the most followers
def get_most_followed_user(tag):
	top_users = []
	if user_followers[tag].values() == []:
		# No results
		return (0, top_users)
	# Get maximum, and get all users with that maximum
	max_followers = max(user_followers[tag].values())
	for name, number in user_followers[tag].iteritems():
		if number == max_followers:
			top_users.append(name)
	return (max_followers, top_users)

# Get tweet with most retweets
def get_most_retweeted_tweet(tag):
	top_tweets = []
	if tweets[tag] == []:
		# No results
		return (0, top_tweets)
	# Get maximum, and get all users with that maximum
	max_retweets = max([tweet["retweet_count"] for tweet in tweets[tag]])
	for tweet in tweets[tag]:
		if tweet["retweet_count"] == max_retweets:
			top_tweets.append(tweet)
	return (max_retweets, top_tweets)

# Get tweet with most favorites
def get_most_favorited_tweet(tag):
	top_tweets = []
	if tweets[tag] == []:
		return (0, top_tweets)
	# Get maximum, and get all users with that maximum
	max_favorites = max([tweet["favorite_count"] for tweet in tweets[tag]])
	for tweet in tweets[tag]:
		if tweet["favorite_count"] == max_favorites:
			top_tweets.append(tweet)
	return (max_favorites, top_tweets)

"""  Statistics Output  """

for tag in LIST_OF_HASHTAGS:
	print "   Results for the hashtag '#%s'" % tag
	#
	# Print most frequent user
	(count, top_users) = get_most_frequent_user(tag)
	print " Most frequent user (%i appearances)" % count
	counter = 0
	for user in top_users:
		counter += 1
		if counter >= MAX_USERS_TO_DISPLAY:
			print "~ %i results hidden~" % (len(top_users) - MAX_USERS_TO_DISPLAY)
			break
		print(user.encode("utf-8"))
	#
	# Print most followed user
	(count, top_followed) = get_most_followed_user(tag)
	print " Most followed user (%i followers)" % count
	counter = 0
	for user in top_followed:
		counter += 1
		if counter >= MAX_USERS_TO_DISPLAY:
			print "~ %i results hidden~" % (len(top_followed) - MAX_USERS_TO_DISPLAY)
			break
		print(user.encode("utf-8"))
	#
	# Print most retweeted tweet
	(count, top_retweeted) = get_most_retweeted_tweet(tag)
	print " Most retweeted tweet (%i retweets)" % count
	counter = 0
	for tweet in top_retweeted:
		counter += 1
		if counter >= MAX_TWEETS_TO_DISPLAY:
			print "~ %i results hidden~" % (len(top_retweeted) - MAX_TWEETS_TO_DISPLAY)
			break
		print (tweet["text"].encode("utf-8"))
	#
	# Print most favorited tweet
	(count, top_favorited) = get_most_favorited_tweet(tag)
	print " Most favorited tweet (%i favorites)" % count
	counter = 0
	for tweet in top_favorited:
		counter += 1
		if counter >= MAX_TWEETS_TO_DISPLAY:
			print "~ %i results hidden~" % (len(top_favorited) - MAX_TWEETS_TO_DISPLAY)
			break
		print (tweet["text"].encode("utf-8"))

"""  Data Visualization Data Initialization  """

# Lists for the frequencies of each hashtag with the first 4 values
# being the first day, then the next being the second day and so on.
csforall_frequency = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
equality_frequency = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
equity_frequency   = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
stem_frequency     = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
yolo_frequency     = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

"""  Data Visualization Data Initialization  """

for tag in LIST_OF_HASHTAGS:
	for tweet in tweets[tag]:
		# This section converts from UTC to EST,
		#  then determines what position in the array to assign tweet.
		day = tweet["created_at"].day
		hour = tweet["created_at"].hour
		# UTC to EST, rough conversion
		if hour - 5 < 0:
			if day == 1:
				day = 28
			else:
				day = day - 1
		# Position in array calculation
		hour = (24 + hour - 5) % 24
		position = (4 * (day - 25)) + int(hour / 6)
		# Code linking: adding to the correct frequency at a certain position.
		if tag == "CSFORALL":
			csforall_frequency[position] += 1
		elif tag == "EQUALITY":
			equality_frequency[position] += 1
		elif tag == "EQUITY":
			equity_frequency[position] += 1
		elif tag == "STEM":
			stem_frequency[position] += 1
		elif tag == "YOLO":
			yolo_frequency[position] += 1
		else:
			continue

"""  Data Visualization Data Preparation  """

# List containing the different hashtag's to be used to create a graph for each.
hashtag = ['#csforall', '#equality', '#equity', '#stem', '#yolo']


# Counter used to select the correct list for data.
y = 0

# List of all of the frequency lists, used to call the correct list for the
# correct graph during the loop.
hashtag_frequency = [csforall_frequency,
	equality_frequency,
	equity_frequency,
	stem_frequency,
	yolo_frequency]

"""  Data Visualization Generation  """

# Loop to create all five graphs for each hashtag.
for i in hashtag:
	
	# List that contains the proper data as called from the list of all frequency lists.
	frequency_list = hashtag_frequency[y]
	
	n_groups = 4
	
	# Sets values from the frequency list to separate lists for the different 
	# hour segments that we are measuring.
	first_hours = (frequency_list[0], frequency_list[5], frequency_list[8], frequency_list[12])
	second_hours = (frequency_list[1], frequency_list[5], frequency_list[9], frequency_list[13])
	third_hours = (frequency_list[2], frequency_list[6], frequency_list[10], frequency_list[14])
	fourth_hours = (frequency_list[3], frequency_list[7], frequency_list[11], frequency_list[15])
 
	# Creates the bar chart as well as the size of the bars and their color.
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.15
	opacity = 1.0
 
	# Uses the values from the newly created lists to create the bars in the
	# graph with proper spacing, different colors, and labels in the legend
	# for which group of bars represents which segment of time.
	
	# Colors are from "Show Me the Numbers" by Stephen Few
	# Also from http://www.mulinblog.com/a-color-palette-optimized-for-data-visualization/
	rects1 = plt.bar(index, first_hours, bar_width,
		alpha=opacity,
		color='#5da5da',
		label='00:00 - 05:59')
 
	rects2 = plt.bar(index + bar_width, second_hours, bar_width,
		alpha=opacity,
		color='#60bd68',
		label='06:00 - 11:59')

	rects3 = plt.bar(index + bar_width + bar_width, third_hours, bar_width,
		alpha=opacity,
		color='#f15854',
		label='12:00 - 17:59')

	rects4 = plt.bar(index + bar_width + bar_width + bar_width, fourth_hours, bar_width,
		alpha=opacity,
		color='#decf3f',
		label='18:00 - 23:59')
 
	# Sets the labels in the graphs.
	plt.xlabel('Day')   
	plt.ylabel('Frequency')  
	plt.title( i + ' Frequency over Days')
	plt.xticks(index + bar_width + bar_width, ('02/25/17', '02/26/17', '02/27/17', '02/28/17'))
	plt.legend()
	plt.tight_layout()
	plt.show()
	y += 1
 
	# Prints out the graphs and iterates y so that the next graph uses the next
	# data set from the next frequency list.
	
	