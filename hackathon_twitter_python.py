#!/usr/bin/env python
# coding: utf-8

# In[1]:


import twitter
import re
import pandas as pd
consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''
 
print("sajan")
api=twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)

trender={}
trending =[]
count=[]
timestamp=[]
url=[]

trending_topics = api.GetTrendsWoeid(23424848)
for topic in trending_topics:
    if topic.name[0]!='#':
       new_name ="#" + topic.name
       trending.append(new_name)
    else:
        trending.append(topic.name)
    count.append(topic.volume)
    timestamp.append(topic.timestamp)
    url.append(topic.url)

trender['Trending']=trending
trender['count']=count
trender['timestamp']=timestamp
trender['url']=url
#print(trender)
df=pd.DataFrame(trender)

tweets = dict()
users = dict()

def find_tweets_and_users_using_hashtag_sajan(hashtag="#MSI2018"):
    tweet_data=""
    for tweet in api.GetSearch(hashtag, count=50, lang="en", return_json=False):
        tweet_data+=tweet.text
    return tweet_data

def classify(x):
    #print("X value is {}".format(x))
    saj=find_tweets_and_users_using_hashtag_sajan(x)
    
    Sports = re.compile(r'(ball|bat|cricket|run|spin|stump|football|club|balls|runs|match|matches|bowling|innings|tournament|six|four|world cup|ODI|century|catch|bowl|lbw|captain|coach|team|wickets|stump|runs|goal|messi|ground)')
    News = re.compile(r'(breaking news|politics|minister|CM|BJP|congress|threaten|MP|goons|Opposition|parties|Modi|Gandhi|Arnab|Mantri|election|ndtv|republic|cnbc|new18|timesnow|cnn|aaj|mla)')
    Movie = re.compile(r'(Actor|ajith|actress|bollywood|trailer|movie|trp|hero|box|box office|gross|btown|sandalwood|beautiful|handsome|couple|pair|romance|kiss|comedy|kollywood|tollywood|sandlewood|drama|thriller|gorgeous)')

    matches = Sports.finditer(saj,re.IGNORECASE)
    sports_count=0
    sports_match=set()
    for match in matches:
        sports_count=sports_count+1
        sports_match.add(match.group(1))
        #print(match.group(1))
    #print("SPORTS COUNT is  {}".format(sports_count))

    matches = News.finditer(saj,re.IGNORECASE)
    news_count=0
    news_match=set()
    for match in matches:
        news_count=news_count+1
        news_match.add(match.group(1))
        #print(match)
    #print("NEWS COUNT is  {}".format(news_count))

    matches = Movie.finditer(saj,re.IGNORECASE)
    movie_count=0
    movie_match=set()
    for match in matches:
        movie_count=movie_count+1
        movie_match.add(match.group(1))
        #print(match)
    #print("MOVIE COUNT is  {}".format(movie_count))

    maximus=max(sports_count,news_count,movie_count)
    none=0

    if maximus==0 or maximus==1:
        value="OTHERS"
        return value,maximus,none
    keywds=[]
    if maximus==sports_count:
        value="SPORTS"
        keywds=sports_match
    elif maximus==news_count:
        value="NEWS"
        keywds=news_match
    else:
        value="MOVIE"
        keywds=movie_match
    return value,maximus,keywds

def keywords(category):
    sports="ball|bat|cricket|run|spin|stump|balls|runs|match|matches|bowling|innings|tournament|six|four|world cup|ODI|century|catch|bowl|lbw|captain|coach|team|wickets|stump|runs|goal|messi|ground"
    sports=sports.split("|")
    news="breaking news|politics|minister|CM|BJP|congress|threaten|MP|goons|Opposition|parties|Modi|Gandhi|Arnab|Mantri|election|ndtv|republic|cnbc|new18|timesnow|cnn|aaj|mla"
    news=news.split("|")
    movies="Actor|ajith|actress|bollywood|trailer|movie|trp|hero|box|box office|gross|btown|sandalwood|beautiful|handsome|couple|pair|romance|kiss|comedy|kollywood|tollywood|sandlewood|drama|thriller|gorgeous"
    movies=movies.split("|")
    if category=='SPORTS':
        return sports
    elif category=='NEWS':
        return news
    elif category=='MOVIE':
        return movies
    else:
        return 0

if __name__ == "__main__": 
    print ("Executed when invoked directly")
    #df['category']=df['Trending'].apply(lambda x: classify(x))
    tup=df['Trending'].apply(lambda x: classify(x))
    df['category']=tup.apply(lambda x:x[0])
    df['matching_counts']=tup.apply(lambda x:x[1])
    df['keywords']=tup.apply(lambda x:x[2])
    #df['keywords']=df['category'].apply(lambda x:keywords(x))
    #df['matching_counts']=tup[1]
    #df['matching_counts']=df['Trending'].apply(lambda x: classify_count(x))
    #df['matching_counts']=df['Trending'].apply(lam)
else: 
    print ("Executed when imported")


