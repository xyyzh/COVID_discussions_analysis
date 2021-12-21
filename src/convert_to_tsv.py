import csv
import json

def already_exists(text):
    '''Checks that it's not a duplicate    
    '''
    with open('tweets.tsv', 'r', encoding="utf-8", newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if row[3] == text:
                return True
    return False

def get_tweet_text(tweet):
    '''Normal tweets have the entire string given inside "tweet.full_text",
    However to get the entire string of a retweet we need to get it from:
    tweet._json['retweeted_status']['full_text']. This method gives the full
    text regardless of what kind of tweet it is.
    Note: the text of a retweet lose the 'RE' prefix that they usually contain. 
    '''
    if 'retweeted_status' in tweet:
        text = tweet['retweeted_status']['full_text']
    else:
        text = tweet['full_text']
    return text.replace('\n', '\\n')

def save_to_tsv(json_filename, tsv_file):
    with open(json_filename, 'r') as fjson:
        while True:
            line = fjson.readline()
            if not line:
                break
            tweet = json.loads(line)
            text_to_save = get_tweet_text(tweet)
            if not already_exists(text_to_save):
                writer = csv.writer(tsv_file, delimiter='\t')
                writer.writerow([tweet['id_str'], f"https://twitter.com/twitter/statuses/{tweet['id_str']}", tweet['created_at'], text_to_save])
    
with open('tweets.tsv', 'a+', encoding="utf-8", newline='') as ftweets:
    save_to_tsv('tweets-11-12.json', ftweets)
    save_to_tsv('tweets-11-13.json', ftweets)
    save_to_tsv('tweets-11-14.json', ftweets)