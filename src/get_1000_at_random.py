import pandas as pd

df1 = pd.read_csv('tweets-11-12.tsv', '\t', header=None, names=["id", "link", "date", "text"]).sample(333)
df2 = pd.read_csv('tweets-11-13.tsv', '\t', header=None, names=["id", "link", "date", "text"]).sample(334)
df3 = pd.read_csv('tweets-11-14.tsv', '\t', header=None, names=["id", "link", "date", "text"]).sample(333)

frames = [df1, df2, df3]
result = pd.concat(frames)

result.to_csv('1000_tweets.tsv', index=False, sep='\t')