from flask import request
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from models import db, Token, SpeakingTest
from cookies import authentication_required

import random


# Create request parser for Token model
def create_token_args():
    token_args = reqparse.RequestParser()
    token_args.add_argument('token', type=str, help='Token value, required', required=True)
    token_args.add_argument('is_premium', type=int, help='Is Premium, required', required=True)
    token_args.add_argument('chat_id', type=int, help='Chat ID, required', required=True)
    token_args.add_argument('is_used', type=bool, help='Is Used, required', required=True)
    token_args.add_argument('limit', type=int, help='Limit', required=False)  # Adjust based on your requirements
    token_args.add_argument('name', type=str, help='name', required=False)
    token_args.add_argument('question_id', type=int, help='Question ID', required=False)
    return token_args


def update_token_args():
    token_args = reqparse.RequestParser()
    token_args.add_argument('token', type=str, help='Token value, required', required=False)
    token_args.add_argument('is_premium', type=int, help='Is Premium, required', required=False)
    token_args.add_argument('chat_id', type=int, help='Chat ID, required', required=False)
    token_args.add_argument('is_used', type=bool, help='Is Used, required', required=False)
    token_args.add_argument('limit', type=int, help='Limit', required=False)  # Adjust based on your requirements
    token_args.add_argument('name', type=str, help='name', required=False)
    token_args.add_argument('question_id', type=int, help='Question ID', required=False)
    return token_args


# Define resource fields for marshalling
token_resource_fields = {
    'id': fields.Integer,
    'token': fields.String,
    'is_premium': fields.Integer,
    'chat_id': fields.Integer,
    'is_used': fields.Boolean,
    'created_at': fields.DateTime(dt_format='iso8601'),
    'limit': fields.Integer,
    'used_time': fields.Integer,
    'name': fields.String,
    'question_id': fields.Integer,
}


class TokenQueries(Resource):
    @marshal_with(token_resource_fields)
    @authentication_required
    def get(self):
        # Access user chat_id from the request object
        chat_id = request.chat_id
        # Get the Token instance by ID
        token = Token.query.filter_by(chat_id=chat_id).all()
        # Check if the Token exists
        if not token:
            abort(404, message="Token not found")
        return token

    @marshal_with(token_resource_fields)
    @authentication_required
    def post(self):
        args = create_token_args().parse_args()
        chat_id = request.chat_id
        # Create a Token object
        token = Token(
            token=args['token'],
            is_premium=args['is_premium'],
            chat_id=chat_id,
            is_used=args['is_used'],
            limit=args['limit'],
            name=args['name'],
            question_id=args['question_id'],
        )

        # Add the token object to the database
        db.session.add(token)
        db.session.commit()
        return token, 201

    @marshal_with(token_resource_fields)
    @authentication_required
    def put(self, token_id):
        # Parse the arguments from the request
        args = update_token_args().parse_args()
        chat_id = request.chat_id
        # Get the existing Token instance from the database
        token = Token.query.filter_by(id=token_id).first()
        # Check if the instance exists
        if token and chat_id == token.chat_id:
            # Update the instance with the provided arguments
            for key, value in args.items():
                if value is not None:
                    setattr(token, key, value)
            # Commit the changes to the database
            db.session.commit()
            return token
        else:
            abort(404, message="Token not found")

    @authentication_required
    def delete(self, token_id):
        chat_id = request.chat_id
        t = Token.query.filter_by(id=token_id).first()
        if t and chat_id == t.chat_id:
            db.session.delete(t)
            db.session.commit()
        else:
            abort(404, message="You cannot delete this token")
