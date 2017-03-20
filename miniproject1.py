# -- coding: utf-8 --
# Alex Kerzner, Stuart Badger
# 2017-02-10
# COSC480 - Data Science for the Public Good
# Professor Alan Jamieson

from bs4 import BeautifulSoup
import requests
import re
from collections import defaultdict,OrderedDict

# Notes

# Contractions are considered to be a single word
# Hyphenated words are also considered a single word
# All body text is included, including the state and city if applicable
# Words are case-insensitive





# Regular expression that matches one or more letters, numbers, underscores, hyphens, or apostrophes
REX = re.compile(r"[^A-Za-z0-9_\-']+")




# URL definitions
# Topic: Trump
# Reason: No shortage of articles on this topic

list_of_urls = []
# List that contains 20 urls
list_of_urls.append("http://www.theonion.com/article/eric-trump-scolds-father-he-mustnt-inquire-about-b-55218")
list_of_urls.append("http://www.theonion.com/article/secret-service-adds-emotional-protection-division--55263")
list_of_urls.append("http://www.theonion.com/article/fearful-americans-stockpiling-facts-federal-govern-55219")
list_of_urls.append("http://www.theonion.com/article/nations-stomach-ulcers-predict-trump-administratio-55208")
list_of_urls.append("http://www.theonion.com/article/trump-hails-gorsuch-fierce-protector-future-amendm-55201")
list_of_urls.append("http://www.theonion.com/article/trump-supporter-has-few-backup-scapegoats-ready-go-55186")
list_of_urls.append("http://www.theonion.com/article/trump-insists-now-more-ever-americans-must-stand-s-55181")
list_of_urls.append("http://www.theonion.com/article/nothing-would-surprise-me-point-says-man-who-will--55179")
list_of_urls.append("http://www.theonion.com/article/trump-claims-waterboarding-doesnt-come-close-excru-55158")
list_of_urls.append("http://www.theonion.com/article/collection-agency-holding-nation-collateral-until--55156")
list_of_urls.append("http://www.theonion.com/article/trump-deploys-national-guard-press-conference-stan-55134")
list_of_urls.append("http://www.theonion.com/article/i-promise-work-tirelessly-achieve-my-campaigns-goa-55094")
list_of_urls.append("http://www.theonion.com/article/trump-calms-nerves-inaugural-address-reminding-him-55095")
list_of_urls.append("http://www.theonion.com/article/trump-honors-sacrifices-civil-rights-activists-wil-55061")
list_of_urls.append("http://www.theonion.com/article/transition-team-assures-public-trump-has-too-many--55029")
list_of_urls.append("http://www.theonion.com/article/trump-unveils-exclusive-double-platinumlevel-press-55023")
list_of_urls.append("http://www.theonion.com/article/trump-gives-intelligence-agencies-their-daily-brie-54961")
list_of_urls.append("http://www.theonion.com/article/psychologists-advise-practicing-words-president-tr-54686")
list_of_urls.append("http://www.theonion.com/article/report-it-still-nowhere-near-okay-act-donald-trump-54679")
list_of_urls.append("http://www.theonion.com/article/report-things-finally-bad-trump-claims-54665")
# 20 urls added to list_of_urls

# Initialization of variables

# List of website objects, contains all of the data
websites = []

# Frequency list
global_words = defaultdict(int)

# List of top most frequent word(s)
most_frequent_words = []

# List of number of words per article
word_counts = []

# Median (middle number or average of two middle numbers)
median = 0

# Mean (average of all numbers - sum of all numbers divided by the number of)
mean = 0

# Sort dictionary by values from greatest to least, then by key (alphabetically)
def sort_dictionary(dictionary):
	return OrderedDict(sorted(dictionary.items(), key=lambda item : (-item[1], item[0]),reverse=False))

# Prints sorted dictionary
def print_dictionary(dictionary):
	for key, value in dictionary.iteritems():
		print("%4i: %s" % (value, str(key)))

# Prints the most frequently used word in the most_frequent_words list
def print_most_frequent_words():
	for key, value in most_frequent_words:
		print("%4i: %s" % (value, str(key)))

# Count words for a website
class Website:
	def __init__(self, url):
		self.url = url
		# Get website data
		response = requests.get(url)
		soup = BeautifulSoup(response.text, "html.parser")
		# Get title of article
		self.title = soup.title.text
		# Get body of article
		self.body = soup.find_all(class_="content-text")[0].get_text().strip()
		# Contractions are one word
		self.body = self.body.replace(u'\u2019', "'")
		# Split body into words
		self.words = REX.split(self.body)
		# Count unique words
		self.count_words()
		# Get word count, not including first null character
		self.word_count = len(self.words) - 1
	
	# Counts words for frequency list
	def count_words(self):
		for word in self.words:
			if (word != u''):
				global_words[word.lower()] += 1

# Creates a new website class object for each url
def webget():
	for url in list_of_urls:
		websites.append(Website(url))

def get_median_word_count():
	global median
	# Get median
	# Assume sorted
	if len(word_counts) % 2 == 0:
		# Average the middle two if even number of values
		median = float(word_counts[len(word_counts)/2] + word_counts[(len(word_counts)/2)-1]) / 2
	else:
		# Return the middle one if odd number of values
		median = float(word_counts[len(word_counts)/2])

# Get mean
def get_mean_word_count():
	global mean
	# Takes the sum of the contents of word_counts and divides it by the length of word_counts
	mean = float(sum(word_counts))/len(word_counts)

# Get word count from each article and sorts the combined list
def get_word_counts():
	global word_counts
	for website in websites:
		# Adds the word count from the article into the list word_counts
		word_counts.append(website.word_count)
	# Sorts the list for median calculation
	word_counts = sorted(word_counts)

# Finds the most frequently used word in the frequency list
def get_most_frequent_word():
	global most_frequent_words
	max_count = max(global_words.values())
	for word, number in global_words.iteritems():
		if number == max_count:
			most_frequent_words.append((word,number))

# Prints a numbered list of the urls
def print_urls():
	i = 0
	for website in websites:
		i = i + 1
		print("%2i: %s" % (i, website.url))

# Runs all of the methods and prints out the urls, median, mean, most frequent word, and frequency list of the article data
def run():
	# Defines "global_words" as a reference to a global variable (outside of function scope)
	global global_words
	
	# Get websites and prepare data
	webget()
	
	# Count the words in each article
	get_word_counts()
	
	# Get median number of (words per article)
	get_median_word_count()
	
	# Get mean number of (words per article)
	get_mean_word_count()
	
	# Get most frequent word
	get_most_frequent_word()
	
	# Sort list of words
	global_words = sort_dictionary(global_words)
	
	# Print topic
	print("Topic: Trump")
	
	# Print authors
	print("Code authors: Alex Kerzner, Stuart Badger")
	
	# Print sources
	print("Sources:")
	print_urls()
	
	# Print median and mean
	print("Median words/article = %3.2f words" % median)
	print("Mean words/article = %3.2f words" % mean)
	
	# Print most frequent word
	print("Most frequent word (count:word):")
	print_most_frequent_words()
	
	# Print word frequenc
	print("Frequency of words (count:word):")
	#print_dictionary(global_words)
	
	print("Warning - output may be truncated. Recommended console length is 4000 lines.")

run()

