from nltk.tokenize import WhitespaceTokenizer
from nltk.corpus import stopwords

from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer


ws_tokenizer = WhitespaceTokenizer()

lancaster = LancasterStemmer()
porter = PorterStemmer()
snowball = SnowballStemmer('english')


try:
    stopwords = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    stopwords = set(stopwords.words('english'))



def tokenize(review):

    ws_tokenized = ws_tokenizer.tokenize(review)

    cleaned_tokens = []

    for token in ws_tokenized:
        if token not in stopwords:
            cleaned_tokens.append(token)

    return cleaned_tokens

def stem_tokens(cleaned_tokens, *args):

    stemmed_tokens = []

    try:
        method = args[0]
    except:
        method = 'lancaster'

    if method == 'lancaster':
        for token in cleaned_tokens:
            stemmed_tokens.append(lancaster.stem(token))

    elif method == 'porter':
        for token in cleaned_tokens:
            stemmed_tokens.append(porter.stem(token))

    elif method == 'snowball':
        for token in cleaned_tokens:
            stemmed_tokens.append(snowball.stem(token))

    return stemmed_tokens

def full_review_stemmed(cleaned_tokens, *args):

    stemmed_tokens = []

    try:
        method = args[0]
    except:
        method = 'lancaster'

    if method == 'lancaster':
        for token in cleaned_tokens:
            stemmed_tokens.append(lancaster.stem(token))

    elif method == 'porter':
        for token in cleaned_tokens:
            stemmed_tokens.append(porter.stem(token))

    elif method == 'snowball':
        for token in cleaned_tokens:
            stemmed_tokens.append(snowball.stem(token))

    stemmed_text = ' '.join(stemmed_tokens)

    return stemmed_text
