import asyncio
import random
from asyncio import queues
import logging

from flask import Flask, request, Response, jsonify, redirect, make_response
from flask_restful import Api, marshal
from models import db, User, Token, SpeakingTest
from speaking import SpeakingQueries
from user import UserQueries, user_resource_fields
from speaking_token import TokenQueries
from cookies import authentication_required, create_token

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

api.add_resource(SpeakingQueries, '/api/premium/speaking/questions/<int:task_id>', endpoint='speaking_delete_put')
api.add_resource(SpeakingQueries, '/api/premium/speaking/questions/', endpoint='speaking_post_get')

api.add_resource(UserQueries, '/api/premium/user/profile', endpoint='user_queries')

api.add_resource(TokenQueries, '/api/premium/speaking/token/', endpoint='token_get_post')
api.add_resource(TokenQueries, '/api/premium/speaking/token/id', endpoint='token_put_delete')

@app.route('/api/token/<string:token>', methods=['GET'])
def speaking_test(token):
    # Check if the token exists in the Token model
    token_obj = Token.query.filter_by(token=token).first()
    if not token_obj:
        # If the token is not found, return a 404 response
        return jsonify({'error': 'Token not found'}), 404
    # Check if the token is associated with a premium user
    if token_obj.is_premium == 3:
        # If it's a premium user, retrieve speaking tests for the associated chat_id
        speaking_tests = SpeakingTest.query.filter_by(chat_id=token_obj.chat_id).all()
        # Filter speaking tests for public ones
        public_speaking_tests = [test.to_dict() for test in speaking_tests if test.is_public]
        public_random_test = random.choice(public_speaking_tests)
        token_obj.question_id = public_random_test.id
        db.session.commit()
        # Return the public speaking tests in the response
        return jsonify(public_random_test)
    else:
        # If the user is not premium, select a random speaking test
        all_speaking_tests = SpeakingTest.query.all()
        random_test = random.choice(all_speaking_tests)
        # Increase the 'used_time' field by 1
        random_test.used_time += 1
        # Commit the changes to the database
        token_obj.question_id = random_test.id
        db.session.commit()
        # Return the selected speaking test in the response
        return jsonify(random_test.to_dict())

@app.route('/api/premuim/user/logout', methods=['GET'])
def logout():
    # Delete the auth_token cookie and redirect to the login page
    response = make_response(redirect('/login'))
    response.delete_cookie('auth_token')
    return response

def handle_verification():
    # Get the verification code from the request JSON data
    verification_code = request.json.get('verification')
    if not verification_code:
        return jsonify({'error': 'No verification code'}), 404
    user = User.query.filter_by(verification=verification_code).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if request.method == 'PUT':
        user.education_center = request.json.get('education_center')
        db.session.commit()
    max_age = 36000
    # Create a new token for cookies with the updated user ID
    new_token = create_token(user.chat_id)
    print(new_token)
    # Set the new auth_token cookie in the response
    response_data = marshal(user, user_resource_fields)
    response = jsonify(response_data)
    response.set_cookie('auth_token', new_token, max_age=max_age)
    return response, 200

# Register the same logic for two different URLs
@app.route('/api/premium/user/register', methods=['PUT'])
def sign_up_premium():
    return handle_verification()

@app.route('/api/regular/user/login', methods=['GET'])
def sign_up_regular():
    return handle_verification()


if __name__ == "__main__":
    with app.app_context():
       db.create_all()
    app.run(debug=True)
