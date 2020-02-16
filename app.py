from flask import Flask
from flask_restful import Api

from resources.classify_resource import Classify, AllData

# initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize api
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Classify, '/classify/<string:comment_id>')
api.add_resource(AllData, '/all_data')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    app.run(debug=True)
