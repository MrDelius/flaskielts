from flask import request
from flask_restful import Resource, fields, marshal_with, reqparse, abort

# check if posted data is true
from models import User, db
from cookies import authentication_required, create_token


# Create a request parser for dynamically generating arguments based on the desired structure
def create_user_args():
    user_args = reqparse.RequestParser()

    # Add arguments for User model
    user_args.add_argument('is_premium', type=int, help='Is Premium, required', required=False)
    user_args.add_argument('name', type=str, help='Name, required', required=True)
    user_args.add_argument('user_name', type=str, help='User Name, required', required=True)
    user_args.add_argument('chat_id', type=int, help='Chat ID, required', required=True)
    user_args.add_argument('education_center', type=str, help='Education Center, required', required=True)
    user_args.add_argument('verification', type=int, help='Verification, required', required=True)
    user_args.add_argument('payment', type=str, help='Payment Information, required', required=False)

    return user_args


def update_user_args():
    user_args = reqparse.RequestParser()

    # Add arguments for User model
    user_args.add_argument('is_premium', type=int, help='Is Premium', required=False)
    user_args.add_argument('name', type=str, help='Name', required=False)
    user_args.add_argument('user_name', type=str, help='User Name', required=False)
    user_args.add_argument('chat_id', type=int, help='Chat ID', required=False)
    user_args.add_argument('education_center', type=str, help='Education Center', required=False)
    user_args.add_argument('verification', type=int, help='Verification', required=False)
    user_args.add_argument('payment', type=str, help='Payment Information', required=False)

    return user_args


# Used to make the returned instance of the model be in JSON format
user_resource_fields = {
    'id': fields.Integer,
    'is_premium': fields.Integer,
    'name': fields.String,
    'user_name': fields.String,
    'chat_id': fields.Integer,
    'education_center': fields.String,
    'verification': fields.Integer,
    'payment': fields.String,
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601')
}


class UserQueries(Resource):
    @marshal_with(user_resource_fields)
    @authentication_required
    def get(self):
        # Access user details from the request object
        chat_id = request.chat_id
        # Get the User instance by ID
        user = User.query.filter_by(chat_id=chat_id).first()

        # Check if the User exists
        if not user:
            abort(404, message="User not found")
        return user

    @marshal_with(user_resource_fields)
    def post(self):
        # Parse the arguments from the request
        args = create_user_args().parse_args()

        # Check if the email is already in the database
        existing_user = User.query.filter_by(chat_id=args['chat_id']).first()
        if existing_user:
            abort(400, message="User with this chat_id already exists!")

        # Create a User object
        user = User(
            is_premium=args['is_premium'],
            name=args['name'],
            user_name=args['user_name'],
            chat_id=args['chat_id'],
            education_center=args['education_center'],
            verification=args['verification'],
            payment=args['payment'],
        )

        # Add the user object to the database
        db.session.add(user)
        db.session.commit()

        return user, 201

    @marshal_with(user_resource_fields)
    @authentication_required
    def put(self):
        # Parse the arguments from the request
        args = update_user_args().parse_args()
        chat_id = request.chat_id
        user = User.query.filter_by(chat_id=chat_id).first()
        # Check if the instance exists
        if not user:
            abort(404, message="User not found")

        # Update the instance with the provided arguments
        for key, value in args.items():
            if value is not None:
                setattr(user, key, value)

        print(f"Successfully updated User with chat_id {chat_id}")
        # Commit the changes to the database
        db.session.commit()
        return user

    @authentication_required
    def delete(self):
        chat_id = request.chat_id
        if chat_id is None:
            abort(400, message="Invalid user details")
        user = User.query.filter_by(chat_id=chat_id).first()

        if user:
            db.session.delete(user)
            db.session.commit()