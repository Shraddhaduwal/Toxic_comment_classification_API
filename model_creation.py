import pickle
import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from lime.lime_text import LimeTextExplainer
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

stop_words = set(stopwords.words("english"))


def remove_stopwords(text):
    text_clean = text.replace("\n", "").replace("\t", "").replace("?", "").replace(".", "").replace("#", "").replace("$", "").replace("!", "").replace("^", "").replace("\s", "").replace("\'", "").replace('\"', "").replace("@", "").replace("$", "").strip(" ").replace(",", "").lower()
    without_punctuations = RegexpTokenizer(r'\w+')
    tokens = without_punctuations.tokenize(text_clean)
    words = [w for w in tokens if w not in stop_words]
    return words


def create_pipeline(p1, p2):
    pipe = Pipeline([
        ("vec", p1),
        ('clf', OneVsRestClassifier(p2))
    ])
    return pipe


if __name__ == '__main__':
    df_train = pd.read_csv("data/train.csv")
    df_test = pd.read_csv("data/test.csv")
    df_sub = pd.read_csv("data/sample_submission.csv")

    # Data cleaning and replacing into the dataFrame
    df_train["comment_text"] = pd.DataFrame(df_train["comment_text"].map(lambda com: remove_stopwords(com)))
    df_test["comment_text"] = pd.DataFrame(df_test["comment_text"].map(lambda com: remove_stopwords(com)))

    # converting list into string for pipe2 and pipe3
    train_string = df_train["comment_text"].map(lambda x: " ".join(x))
    test_string = df_test["comment_text"].map(lambda x: " ".join(x))

    # for ytrain, we collect all the data from each label columns from df_train dataframe except column id and comment_text
    # categories is the list of names of labels
    ytrain = df_train[[i for i in df_train.columns if i not in ["comment_text", "id"]]]
    categories = [i for i in df_train.columns if i not in ['id', 'comment_text']]

    # using TFIDF and LogisticRegression
    pipe3 = create_pipeline(TfidfVectorizer(), LogisticRegression())
    pipe3.fit(train_string, ytrain)
    prediction3 = pipe3.predict(test_string)

    # using TFIDF and LinearSVC
    pipe2 = create_pipeline(TfidfVectorizer(), LinearSVC())
    pipe2.fit(train_string, ytrain)
    prediction2 = pipe2.predict(test_string)

    # save the model to disk
    pickle.dump(pipe3, open('model_tfidf_logreg.sav', 'wb'))
    pickle.dump(pipe2, open('model_tfidf_linearsvc.sav', 'wb'))

