import pandas as pd
import json

TOPICS=['efficacy', 'mandate', 'political', 'children', 'side_effect', 'information', 'unvax', 'spread']
SENTIMENTS=['positive', 'negative', 'neutral']

def get_posts():
    with open("../data/no_duplicates_1000.tsv", 'r') as file:
        posts=pd.read_csv(file, sep='\t')
        posts=posts.head(1000)
        return posts

def freq(codings, code):
    counter=0
    for row in codings.iteritems():
        if row[1].__eq__(code):
            counter+=1
    percent="{:.1%}".format(counter/len(codings))  #one decimal place
    return percent
        
def main():
    posts=get_posts()
    topics_freq_dict={}
    sent_freq_dict={}
    output_dict={}
    for topic in TOPICS:
        categories=posts['category']
        percent=freq(categories, topic)
        topics_freq_dict[topic]=percent
    for code in SENTIMENTS:
        sentiments=posts['sentiment']
        percent=freq(sentiments, code)
        sent_freq_dict[code]=percent
    for topic in TOPICS:
        output_dict[topic]={}
        topic_df=posts[posts['category'].str.contains(f'^{topic}$', case=False, regex=True)]
        sentiments=topic_df['sentiment']
        for sentiment in SENTIMENTS:
            percent=freq(sentiments, sentiment)
            output_dict[topic][sentiment]=percent
    with open("../data/more_analysis.json", "w") as file:
        json.dump(topics_freq_dict, file, indent=2)
        json.dump(sent_freq_dict, file)
        json.dump(output_dict, file, indent=2)
            
if __name__=='__main__':
    main()
