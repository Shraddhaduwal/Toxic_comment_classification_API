# Toxic_comment_classification_API
This is the api that checks whether the given text is toxic or not. It also gives the measure of toxicity whether it is toxic, severely toxic, obscene, threat, insult or identity hate. The models were trained on the dataset from `kaggle toxic comment classification challenge`. 

## Data
The dataset can be found [here](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data)

## Models
- pipeline of tfidf vectorizer and linearSVC
- pipeline of tfidf vectorizer and logistic Regression

## Routes
1. GET /classify/<string:comment_id> : This route helps in getting all the text of a certain `comment_id` from the database.`comment_id` should be passed in the url. If `comment_id` doesn't exist then it will be informed.
2. POST /classify/<string:comment_id> : This route is for posting the data ie `comment` to the database.  If `comment_id` already exists or doesn't exist then it will be informed.
3. PUT /classify/<string:comment_id> : This route is for updating the `comment` of the particular `comment_id`. If `comment_id` doesnot exist, it will be informed.
4. DELETE /classify/<string:comment_id> : This route is for deleting the text of particular `comment_id`.  If `comment_id` doesnot exist, it will be informed.
5. GET /all_data : This route is for getting all the list of text/comment from the database.
