import nltk
import string
import heapq
from nltk.tokenize import TweetTokenizer, sent_tokenize, word_tokenize
from nltk.corpus import stopwords 
import requests
from bs4 import BeautifulSoup
from collections import Counter

r = requests.get("https://at.indeed.com/Zeige-Job?jk=3b145aed3018e9a1&tk=1cnosbha69ngics0&from=serp&alid=3&advn=521719209789768")
soup = BeautifulSoup(r.content, features="lxml")
for hit in soup.findAll(attrs={'class' : 'jobsearch-jobDescriptionText'}):      #retrives text from the given url
    hit = hit.text.strip()

sentence_list = nltk.sent_tokenize(hit)         #sentence tokenization

tokens = word_tokenize(hit)         #preprocesing of retrived text
tokens = [w.lower() for w in tokens]       # convert to lower case
table = str.maketrans('', '', string.punctuation)      # remove punctuation from each word
stripped = [w.translate(table) for w in tokens]
words = [word for word in stripped if word.isalpha()]       # remove remaining tokens that are not alphabetic

stop_words = set(stopwords.words('english','german'))       # filter out stop words
words = [w for w in words if not w in stop_words]
    
word_counts = Counter(words)        #counting frequancy of each word   

maximum_frequncy = max(word_counts.values())

for word in word_counts.keys():
    word_counts[word] = (word_counts[word]/maximum_frequncy)

sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_counts.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_counts[word]
                else:
                    sentence_scores[sent] += word_counts[word]
                    

summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)
print(summary)



