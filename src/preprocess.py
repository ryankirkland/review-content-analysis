import re
import sys
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

wordnet = WordNetLemmatizer()
nltk.download('stopwords')

def cleaned_reviews_dataframe(filename):
    print('loading customer reviews dataframe')
    reviews_df = pd.read_csv(f'data/reviews/{filename}')
    print('cleaning customer reviews dataframe')
    reviews_df['title'] = reviews_df['title'].str.replace('\n', '')
    reviews_df['desc'] = reviews_df['desc'].str.replace('\n','')
    reviews_df['title_desc'] = reviews_df['title'] + reviews_df['desc']
    if 'Unnamed: 0' in set(reviews_df.columns):
        reviews_df = reviews_df.drop('Unnamed: 0', axis=1)
    print('cleaning complete, moving to nlp preprocessing')
    return reviews_df

def remove_punc(string:str) -> str:
    '''Given a string, removes all punctuation and returned punctuation-less string'''
    return re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", string)

def tokenize(str):
    '''
    Tokenize a str and return a tokenized list.
    '''
    return [word for word in word_tokenize(str)]

def lemmatize(doc):
    '''Takes in a doc and lemmatizes tokens in doc
    Parameters
    ----------
    doc: list of tokens
    
    Returns
    -------
    lemmatized tokens
    '''
    return [wordnet.lemmatize(tkn) for tkn in doc]

def rm_stop_words(doc, stops=set(stopwords.words('english'))):
    '''Takes in a doc and removes stop words
    Parameters
    ----------
    doc: list of tokens
    
    Returns
    -------
    Tokens with stop words removed
    '''
    return([w for w in doc if w not in stops])

def preprocess_corpus(content):
    '''
    Add docstring. Make flexible to allow for doing, or not doing, preprocessing functions. 
    Parameters
    ----------
    content (str): a collection of strings
    Returns
    -------
    A list of lists: each list contains a tokenized version of the original string
    '''
    preprocessed = []
    for i in range(len(content)):
        print('removing punctuation')
        step_1 = remove_punc(content[i].lower())
        print('tokenizing')
        step_2 = tokenize(step_1)
        print('lemmatizing')
        step_3 = lemmatize(step_2)
        print('removing stop words')
        step_4 = rm_stop_words(step_3)
        preprocessed.append(step_4)
    return preprocessed

def create_str_desc(cleaned_desc, filename):
    print('creating preprocessed column for nlp and review classification')
    str_desc = [" ".join(x) for x in cleaned_desc]
    df['str_desc'] = str_desc
    df.to_csv(f'data/preprocessed_reviews/preprocessed_{filename}')
    return df

if __name__ == '__main__':
    df = cleaned_reviews_dataframe(*sys.argv[1:])
    cleaned_desc = preprocess_corpus(df['title_desc'])
    create_str_desc(cleaned_desc, *sys.argv[1:])