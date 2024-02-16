from flask_restful import Resource, reqparse, abort, fields, marshal_with
from flask import request

import random

# check if posted data is true
from cookies import authentication_required
from models import SpeakingTest, db


# check if post data of client side is true
def create_test_args():
    parser = reqparse.RequestParser()
    parser.add_argument('chat_id', type=int, required=True, help='Chat ID is required')
    parser.add_argument('is_private', type=bool, default=False, help='Is private should be a boolean')

    parser.add_argument('part1', type=list, location='json', required=True, help='Part1 is required')
    parser.add_argument('part2', type=list, location='json', required=True, help='Part2 is required')
    parser.add_argument('part3', type=list, location='json', required=True, help='Part3 is required')
    return parser


def parse_data(result, part_suffix):
    if part_suffix == 2:
        return [
            {
                'question': getattr(result, f'question{i}_part{part_suffix}', None)
            }
            for i in range(1, 11) if getattr(result, f'question{i}_part{part_suffix}') is not None
        ]
    else:
        return [
            {
                'question': getattr(result, f'question{i}_part{part_suffix}', None),
                'thinkingTime': getattr(result, f'thinking{i}_part{part_suffix}', None),
                'speakingTime': getattr(result, f'speaking{i}_part{part_suffix}', None),
            }
            for i in range(1, 11) if getattr(result, f'question{i}_part{part_suffix}') is not None
        ]
def create_single_response_data(record):
    return {
        'chat_id': record.chat_id,
        'is_private': record.is_private,
        'used_time': record.used_time,
        'part1': parse_data(record, 1),
        'part2': [{
            'ThinkingTime': getattr(record, 'thinking_part2', None),
            'SpeakingTime': getattr(record, 'speaking_part2', None),
        }],
        'part3': parse_data(record, 3),
    }

def create_response_data(records):
    # Handle list of records
    response_data_list = []
    for record in records:
        response_data = create_single_response_data(record)
        response_data_list.append(response_data)
    return response_data_list

def set_fields(speaking_test, args, part_key, question_key_prefix, thinking_key_prefix='', speaking_key_prefix=''):
    part_length = len(args[part_key])
    if not thinking_key_prefix:
        part_length -= 1
    for i in range(part_length):
        question_key = f'{question_key_prefix}{i+1}_{part_key}'
        thinking_key = f'{thinking_key_prefix}{i+1}_{part_key}' if thinking_key_prefix else None
        speaking_key = f'{speaking_key_prefix}{i+1}_{part_key}' if speaking_key_prefix else None

        setattr(speaking_test, question_key, args[part_key][i]['question'])
        if thinking_key:
            setattr(speaking_test, thinking_key, args[part_key][i]['thinkingTime'])
        if speaking_key:
            setattr(speaking_test, speaking_key, args[part_key][i]['speakingTime'])

class SpeakingQueries(Resource):
    @authentication_required
    def get(self):
        # Access user details from the request object
        chat_id = request.chat_id
        # Get all the records
        total_records = SpeakingTest.query.filter_by(chat_id=chat_id).all()
        if not total_records:
            abort(404, message="No data in db...")
        # Organize the data in the desired format
        response_data = create_response_data(total_records)

        return response_data

    @authentication_required
    def post(self):
        try:
            chat_id = request.chat_id
            args = create_test_args().parse_args()
            # Creating a new instance of SpeakingTest
            if chat_id != args['chat_id']:
                abort(404, message="You have no access...")
            speaking_test = SpeakingTest(
                chat_id=chat_id,
                is_private=args['is_private'],
            )
            # Set the fields for questions, thinking, and speaking times for each part
            set_fields(speaking_test, args, 'part1', 'question', 'thinking', 'speaking')
            # Set the fields for questions and thinking/speaking times for part2
            set_fields(speaking_test, args, 'part2', 'question')
            # Set the fields for questions, thinking, and speaking times for part3
            set_fields(speaking_test, args, 'part3', 'question', 'thinking', 'speaking')
            # Add the instance to the database session
            db.session.add(speaking_test)
            # Set the fields for thinking and speaking times for part2
            speaking_test.thinking_part2 = args['part2'][-1].get('thinkingTime')
            speaking_test.speaking_part2 = args['part2'][-1].get('speakingTime')
            # Commit the changes to the database
            db.session.commit()
            # Return a response
            response_data = create_single_response_data(speaking_test)
            return response_data, 201
        except Exception as e:
            return {'error': str(e)}, 500

    @authentication_required
    def put(self, task_id):
        try:
            chat_id = request.chat_id
            args = create_test_args().parse_args()
            # Retrieve the existing SpeakingTest record based on chat_id
            speaking_test = SpeakingTest.query.filter_by(id=task_id).first()
            if not speaking_test and speaking_test.chat_id != chat_id:
                abort(404, message="No data found for the given chat_id.")
            speaking_test.is_private = args['is_private']
            # Update the fields for questions, thinking, and speaking times for each part
            set_fields(speaking_test, args, 'part1', 'question', 'thinking', 'speaking')
            # Update the fields for questions and thinking/speaking times for part2
            set_fields(speaking_test, args, 'part2', 'question')
            # Update the fields for questions, thinking, and speaking times for part3
            set_fields(speaking_test, args, 'part3', 'question', 'thinking', 'speaking')
            # Update the fields for thinking and speaking times for part2
            speaking_test.thinking_part2 = args['part2'][-1].get('thinkingTime')
            speaking_test.speaking_part2 = args['part2'][-1].get('speakingTime')
            # Commit the changes to the database
            db.session.commit()
            # Return a response
            response_data = create_single_response_data(speaking_test)
            return response_data, 200
        except Exception as e:
            return {'error': str(e)}, 500

    @authentication_required
    def delete(self, task_id):
        chat_id = request.chat_id
        task = SpeakingTest.query.filter_by(id=task_id).first()
        if task and task.chat_id == chat_id:
            db.session.delete(task)
            db.session.commit()
        else:
            abort(400, message="Invalid test details")