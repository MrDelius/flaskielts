from flask_restful import Resource, reqparse, abort, fields, marshal_with
from models import db, Token, SpeakingTest

import random


# Create request parser for Token model
def create_token_args():
    token_args = reqparse.RequestParser()
    token_args.add_argument('token', type=str, help='Token value, required', required=True)
    token_args.add_argument('is_premium', type=bool, help='Is Premium, required', required=True)
    token_args.add_argument('chat_id', type=int, help='Chat ID, required', required=True)
    token_args.add_argument('is_used', type=bool, help='Is Used, required', required=True)
    token_args.add_argument('limit', type=int, help='Limit', required=False)  # Adjust based on your requirements
    token_args.add_argument('aimed', type=str, help='Aimed', required=False)
    token_args.add_argument('question_id', type=int, help='Question ID', required=False)
    return token_args


def update_token_args():
    token_args = reqparse.RequestParser()
    token_args.add_argument('token', type=str, help='Token value, required', required=False)
    token_args.add_argument('is_premium', type=bool, help='Is Premium, required', required=False)
    token_args.add_argument('chat_id', type=int, help='Chat ID, required', required=False)
    token_args.add_argument('is_used', type=bool, help='Is Used, required', required=False)
    token_args.add_argument('limit', type=int, help='Limit', required=False)  # Adjust based on your requirements
    token_args.add_argument('aimed', type=str, help='Aimed', required=False)
    token_args.add_argument('question_id', type=int, help='Question ID', required=False)
    return token_args


# Define resource fields for marshalling
token_resource_fields = {
    'id': fields.Integer,
    'token': fields.String,
    'is_premium': fields.Boolean,
    'chat_id': fields.Integer,
    'is_used': fields.Boolean,
    'created_at': fields.DateTime(dt_format='iso8601'),
    'limit': fields.Integer,
    'used_time': fields.Integer,
    'aimed': fields.String,
    'question_id': fields.Integer,
}


class TokenQueries(Resource):
    @marshal_with(token_resource_fields)
    def get(self, token):
        # Get the Token instance by ID
        token = Token.query.filter_by(token=token).first()
        # Check if the Token exists
        if not token:
            abort(404, message="Token not found")

        total_records = SpeakingTest.query.all()
        # get 1 out of all
        result = random.choice(total_records)
        return result

    @marshal_with(token_resource_fields)
    def post(self):
        args = create_token_args().parse_args()


        # Create a Token object
        token = Token(
            token=args['token'],
            is_premium=args['is_premium'],
            chat_id=args['chat_id'],
            is_used=args['is_used'],
            limit=args.get('limit'),
            aimed=args.get('aimed'),
            question_id=args.get('question_id'),
        )

        # Add the token object to the database
        db.session.add(token)
        db.session.commit()

        return token, 201

    @marshal_with(token_resource_fields)
    def put(self, token):
        # Parse the arguments from the request
        args = update_token_args().parse_args()

        # Get the existing Token instance from the database
        token = Token.query.filter_by(token=token).first()

        # Check if the instance exists
        if not token:
            abort(404, message="Token not found")

        # Update the instance with the provided arguments
        for key, value in args.items():
            if value is not None:
                setattr(token, key, value)

        # Commit the changes to the database
        db.session.commit()

        return token

    def delete(self, token):
        t = Token.query.filter_by(token=token).first()
        if t:
            db.session.delete(t)
            db.session.commit()
