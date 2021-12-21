import pandas as pd
import numpy as np
import json

PUNCTS=["(", ")","[", "]", ",", "-", ".", "?", "!", ":", ";", "&", "%"]
TOPICS=['efficacy', 'mandate', 'political', 'children', 'side_effect', 'information', 'unvax', 'spread']
MIN_COUNT=5

def make_tweets_df():
    with open("../data/no_duplicates_1000.tsv", 'r') as file:
        tweets_df=pd.read_csv(file, sep='\t')
        tweets_df=tweets_df.head(1000)
        return tweets_df

def collect_stopwords():
    stopwords=[]
    with open("../data/stopwords.txt", 'r') as file:
        lines=file.readlines()[6:]
        for word in lines:
            stopwords.append(word.strip())
    return stopwords

def get_topic(tweets_df, regex):
    topic_df=tweets_df[tweets_df['category'].str.contains(regex, case=False, regex=True)]
    return topic_df

def remove_punct(tweet):
    for punct in PUNCTS:
        tweet=tweet.replace(punct, ' ')
    return tweet

def get_word_counts(tweets_df, stopwords):
    all_counts={}
    counts={}
    for topic in TOPICS:
        counts[topic]={}
        topic_df=get_topic(tweets_df, f'^{topic}$')
        tweets=topic_df['text']
        for tweet in tweets:
            tweet=tweet.lower()
            tweet=remove_punct(tweet)
            for word in tweet.split():
                if word not in stopwords and word.isalpha():
                    if word not in counts[topic]:
                        counts[topic][word]=0
                    counts[topic][word]+=1
                if word not in all_counts:
                    all_counts[word]=0
                all_counts[word]+=1
    for topic in TOPICS:
        for word in list(counts[topic]):
            if all_counts[word]<MIN_COUNT:
                del counts[topic][word]
    counts_df=pd.DataFrame.from_dict(counts)
    counts_df=counts_df.fillna(0)
    return counts_df

def tf_count(counts_df, topic, word):
    return counts_df[topic][word]

def idf_count(counts_df, word):
    topics_count=0
    all_topics=len(counts_df.columns)
    topics_data=counts_df.loc[word,:]
    for category, word_count in topics_data.iteritems():
        if not word_count==0:
            topics_count+=1
    idf=np.log10(all_topics/topics_count)
    return idf

def make_tf_idf_df(counts_df):
    tf_idf_df=pd.DataFrame(index=counts_df.index, columns=counts_df.columns)
    columns=counts_df.columns
    index=counts_df.index
    for topic,word in ((topic, word) for word in index for topic in columns):
        tf_idf_df[topic][word]=tf_count(counts_df, topic, word)*idf_count(counts_df, word)
    return tf_idf_df

def main():
    tweets_df=make_tweets_df()
    stopwords=collect_stopwords()
    counts_df=get_word_counts(tweets_df, stopwords)
    tf_idf_df=make_tf_idf_df(counts_df)
    output_dict={}
    for category, score in tf_idf_df.iteritems():
        topic=score.sort_values(ascending=False)
        output_dict[category]=list(topic.index[:10])
    with open("../data/word_analysis.json", 'w') as file:
        json.dump(output_dict, file, indent=2)

if __name__=='__main__':
    main()