import tweepy as tw
import auth_keys as keys
import datetime 
import json
from os.path import exists


def generate_query_string(search_words, until):
    ''' Given a list of search_words and a since date it outputs a query string.
    The syntax is: 'keyword1 OR keyword2 OR keyword3... since:YYYY-MM-DD -filter:links'
    '''
    query = ""
    num_words = len(search_words)
    for i in range(num_words):
        if i < num_words - 1:
            query += search_words[i] + " OR "
        else:
            query += search_words[num_words - 1]
    
    #query += " since:" + since
    query += " until:" + until
    query += " -filter:links"
    return query

def get_date_n_days_ago(n):
    '''Calculates the date from n days ago, outputs a string in format YYYY-MM-DD
    '''
    today = datetime.datetime.now()
    n_days = datetime.timedelta(days = 3)
    return str(today- n_days)[:10]

def get_tweet_text(tweet):
    '''Normal tweets have the entire string given inside "tweet.full_text",
    However to get the entire string of a retweet we need to get it from:
    tweet._json['retweeted_status']['full_text']. This method gives the full
    text regardless of what kind of tweet it is.

    Note: the text of a retweet lose the 'RE' prefix that they usually contain. 
    '''
    if 'retweeted_status' in tweet._json:
        text = tweet._json['retweeted_status']['full_text']
    else:
        text = tweet.full_text
    return text

def check_text(tweet, search_words):
    '''It checks that the tweet indeed contains one of the search words
    This is not always the case, for example if a person's name has 'covid' 
    then the tweet is labeled as having the 'covid' keyword even if the text doesn't
    '''
    text = get_tweet_text(tweet)

    for word in search_words:
        no_quotes = word.replace('\"', '')
        if no_quotes in text:
            return True
    return False

#This is outside the method so it doesn't have to initialize an array everytime the function is called
canadian = ['alberta', 'british columbia', 'manitoba', 'new brunswick', 'newfoundland', 'labrador', 'nova scotia', 'ontario', 'prince edward', 'quebec', 'saskatchewan', 'canada']
def check_canadian(tweet):
    ''' about 1% of tweets have a "place" attribute, this is because most users don't have 
    geo location enabled (i.e. the tweet itself may not be directly have a location attached)
    However, users themselves can have a location. I used the heuristic that if they contained 
    a Canadian province in their description then we assume they are Canadian. (This seems to be
    a common solution people use).

    Note that this is manually written by the user so some people have imaginary places
    no places at all, etc
    '''
    user_location = str(tweet.user.location).lower()
    for province in canadian:
        if province in user_location:
            return True

    return (tweet.place is not None and tweet.place.country_code == "CA") 

def already_exists(s):
    '''Checks that it's not a duplicate    
    '''
    if not exists('tweets.json'):
        return False
    with open('tweets.json', 'r') as f:
        while True:
            line = f.readline()
    
            if not line:
                break
            tweet = json.loads(line)
            if 'retweeted_status' in tweet:
                text = tweet['retweeted_status']['full_text']
            else:
                text = tweet['full_text']
            if text == s:
                return True
        return False

def main():
    # For this part you need to create your own 'auth_keys.py' file
    # with your own credentials (see example in the github repo)
    auth = tw.OAuthHandler(keys.consumer_key, keys.consumer_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    # These are the keywords to search for
    search_words = ['covid', 'vaccination', 'vaccine', 'pfizer', 'BioNTech', 'j&j', '\"johnson & johnson\"', 'moderna', 'astrazeneca', '\"astra zeneca\"']
    # Date since limits how far back to go (currently set to 1 day).
    # Note that the search starts from "right now" and goes backwards in time
    # So the search is in the order: "now" -> date_since
    #date_since = get_date_n_days_ago(1)
    date_until = '2021-11-13'   
    # Gets the query string
    query  = generate_query_string(search_words, date_until)

    # This gives us an iterable set of tweets (lazy-loading)
    # The count gives us how many tweets we want per query (100 is max)
    # lang is the language
    # tweet_mode = 'extended' makes sure that the text is not truncated (and thus we get the full text)
    tweets = tw.Cursor(api.search_tweets,
                count=100,
                q= query,
                lang="en",
                tweet_mode='extended').items()

    count = 0
    # iterate through tweets
    for tweet in tweets:     
        # make sure the text contains a keyword (see check_text documentation above for more details as to why this is needed) 
        # also filter out all non-canadian tweets
        if check_text(tweet, search_words) and check_canadian(tweet):
            if not already_exists(get_tweet_text(tweet)):
                with open('tweets.json', 'a+') as f:
                    f.write(json.dumps(tweet._json)+'\n')
                count += 1
                print(count)
                
                
    

if __name__ == '__main__':
    main()