from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

stop_words = set(stopwords.words("english"))


def remove_stopwords(text):
    text_clean = text.replace("\n", "").replace("\t", "").replace("?", "").replace(".", "").replace("#", "").replace("$", "").replace("!", "").replace("^", "").replace("\s", "").replace("\'", "").replace('\"', "").replace("@", "").replace("$", "").strip(" ").replace(",", "").lower()
    without_punctuations = RegexpTokenizer(r'\w+')
    tokens = without_punctuations.tokenize(text_clean)
    words = [w for w in tokens if w not in stop_words]
    return words
