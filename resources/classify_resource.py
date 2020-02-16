import pickle
import json
from flask_restful import Resource, reqparse

from models.classify_model import ClassifyModel
from utils.utils import remove_stopwords

# loading the saved model [model_tfidf_logreg]
model = pickle.load(open("model_tfidf_logreg.sav", "rb"))


class Classify(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('comment', required=True, help='This field cannot be empty')

    def get(self, comment_id):
        comment_list = []
        comment_text = ClassifyModel.find_by_comment_id(comment_id)
        if comment_text:
            obj = ClassifyModel(comment_id, comment_text.comment)
            comment = obj.comment
            comment_pre_processed = remove_stopwords(comment)
            comment_string = ' '.join([str(elem) for elem in comment_pre_processed])
            print(comment_string)
            print(type(comment_string))
            comment_list.append(comment_string)  # model takes list.

            # result = model.predict_proba(comment_list)
            result = model.predict(comment_list)

            final_result = result.tolist()  # numpy ndarray cannot be directly sent to json as json object does not \
            # understand how to convert a numpy array so we convert it into list

            # return json.dumps({"prediction": final_result})
            return {'prediction [toxic, severe_toxic, obscene, threat, insult, identity_hate]': json.dumps(final_result)}

    def post(self, comment_id):
        if ClassifyModel.find_by_comment_id(comment_id):
            return {'message': f'The comment with comment_id {comment_id} already exist'}, 400
        request_data = Classify.parser.parse_args()
        comment = ClassifyModel(comment_id, request_data['comment'])
        try:
            comment.save_to_db()
        except Exception:
            return {'message': 'An error occurred while inserting the comment'}, 500

        return comment.json(), 201

    def put(self, comment_id):
        request_data = Classify.parser.parse_args()

        comment_text = ClassifyModel.find_by_comment_id(comment_id)

        if comment_text is None:
            comment_text = ClassifyModel(comment_id, request_data['comment'])
        else:
            comment_text.comment = request_data['comment']

        comment_text.save_to_db()

        return comment_text.json()

    def delete(self, comment_id):
        comment_text = ClassifyModel.find_by_comment_id(comment_id)
        if comment_text:
            comment_text.delete_from_db()

        return {'message': f'comment with comment_id {comment_id} deleted'}


class AllData(Resource):
    def get(self):
        return {'all comments': [comment.json() for comment in ClassifyModel.query.all()]}

