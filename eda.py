import pandas as pd
train = pd.read_csv('cartalk_stemaway.csv', index_col='Unnamed: 0')

train.head()
train.keys()

train['Title Word Count'] = train['Topic Title'].apply(lambda x: len(str(x).split()))
train[['Topic Title', "Title Word Count"]].head()

train['Title Characters'] = train['Topic Title'].str.len()
train[['Topic Title', 'Title Characters']].head()

train['Title Average Word Length'] = train['Title Characters']/train['Title Word Count']
train[['Topic Title', 'Title Average Word Length']].head()

# pip install nltk

import nltk
nltk.download('stopwords')
stop = nltk.corpus.stopwords.words('english')

train['Title Stopwords'] = train['Topic Title'].apply(lambda x: len([x for x in x.split() if x in stop]))
train[['Topic Title', 'Title Stopwords']].head()

train['Discussion'] = train['Topic Title'] + ' ' + train['Leading Comment'] + ' ' + ' '.join(str(a) for a in train['Other Comments'])

train['Discussion Word Count'] = train['Discussion'].apply(lambda x: len(str(x).split()))
train[['Discussion', "Discussion Word Count"]].head()

train['Discussion Characters'] = train['Discussion'].str.len()
train[['Discussion', 'Discussion Characters']].head()

train['Title Average Word Length'] = train['Title Characters']/train['Title Word Count']
train[['Discussion', 'Discussion Average Word Length']].head()

train['Title Stopwords'] = train['Discussion'].apply(lambda x: len([x for x in x.split() if x in stop]))
train[['Discussion', 'Discussion Stopwords']].head()

# Cleanup Time

train['Discussion'] = train['Discussion'].apply(lambda x: " ".join(x.lower() for x in x.split()))
train['Discussion'].head()

train['Discussion'] = train['Discussion'].str.replace('[^\w\s]','')
train['Discussion'].head()

train['Discussion'] = train['Discussion'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
train['Discussion'].head()

frequent_words = pd.Series(' '.join(train['Discussion']).split()).value_counts()[:5]
frequent_words = list(frequent_words.index)

# pip install textblob

import textblob
tb = textblob.TextBlob
train['Discussion'][:10].apply(lambda x: str(tb(x).correct()))
train['Discussion'].head()

st = nltk.stem.PortStremmer
train['Discussion'].apply(lambda x: " ".join([st.stem(word) for word in x.split()]))
train['Discussion'].head()

nltk.download('wordnet')
train['Discussion'] = train['Discussion'].apply(lambda x: " ".join([textblob.Word(word).lemmatize() for word in x.split()]))

train["N-grams"] = list(tb(train['Discussion']).ngrams(3))
train['Discussion'].head()

import numpy as np

