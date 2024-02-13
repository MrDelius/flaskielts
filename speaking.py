from flask_restful import Resource, reqparse, abort, fields, marshal_with
from flask import request

import random

# check if posted data is true
from models import SpeakingTest, db


# check if post data of client side is true
def create_test_args(request_method):
    test_args = reqparse.RequestParser()

    # Add arguments for Questions
    for i in range(1, 11):
        # Determine if the question is required based on i
        is_required = i < 5 if request_method == 'POST' else False

        test_args.add_argument(f'question{i}_part1', type=str, help=f'Question {i} for Part 1', required=is_required)
        test_args.add_argument(f'question{i}_part2', type=str, help=f'Question {i} for Part 2', required=is_required)
        test_args.add_argument(f'question{i}_part3', type=str, help=f'Question {i} for Part 3', required=is_required)

    # Add arguments for Thinking and Speaking Times
    for i in range(1, 11):
        test_args.add_argument(f'thinking{i}_part1', type=int, help=f'Thinking Time {i} for Part 1')
        test_args.add_argument(f'speaking{i}_part1', type=int, help=f'Speaking Time {i} for Part 1')

        test_args.add_argument(f'thinking{i}_part2', type=int, help=f'Thinking Time {i} for Part 2')
        test_args.add_argument(f'speaking{i}_part2', type=int, help=f'Speaking Time {i} for Part 2')

        test_args.add_argument(f'thinking{i}_part3', type=int, help=f'Thinking Time {i} for Part 3')
        test_args.add_argument(f'speaking{i}_part3', type=int, help=f'Speaking Time {i} for Part 3')

    # Add arguments for other fields in SpeakingTest
    test_args.add_argument('chat_id', type=int, help='Chat ID, required', required=True)
    test_args.add_argument('is_private', type=bool, help='Is Private, required')

    return test_args


# used for post and put
# used to make returned instance of model, be like json format
speaking_resource_fields = {'id': fields.Integer, 'chat_id': fields.Integer, 'is_private': fields.Boolean,
                            'created_at': fields.DateTime(dt_format='iso8601'),
                            'updated_at': fields.DateTime(dt_format='iso8601')}

# Loop for Questions, Thinking, and Speaking Times
for part in ['part1', 'part2', 'part3']:
    for i in range(1, 11):
        # Fields for Questions
        speaking_resource_fields[f'question{i}_{part}'] = fields.String

        # Fields for Thinking and Speaking Times
        speaking_resource_fields[f'thinking{i}_{part}'] = fields.Integer
        speaking_resource_fields[f'speaking{i}_{part}'] = fields.Integer


# getting speaking json data:
question_fields = {
    'question': fields.String,
    'thinking_time': fields.Integer,
    'speaking_time': fields.Integer,
}


def get_part_data(result, part_suffix):
    return [
        {
            'question': getattr(result, f'question{i}_part{part_suffix}'),
            'thinking_time': getattr(result, f'thinking{i}_part{part_suffix}'),
            'speaking_time': getattr(result, f'speaking{i}_part{part_suffix}'),
        } for i in range(1, 11) if getattr(result, f'question{i}_part{part_suffix}') is not None
    ]


class SpeakingQueries(Resource):
    def get(self):
        # Get all the records
        total_records = SpeakingTest.query.all()
        # get 1 out of all
        result = random.choice(total_records)

        # Organize the data in the desired format
        response_data = {
            'chat_id': result.chat_id,
            'is_private': result.is_private,

            'part1': get_part_data(result, 1),
            'part2': get_part_data(result, 2),
            'part3': get_part_data(result, 3),
        }

        return response_data

    @marshal_with(speaking_resource_fields)
    def post(self):
        args = create_test_args(request.method).parse_args()

        # Create a SpeakingTest object
        speaking = SpeakingTest(
            chat_id=args['chat_id'],
            is_private=args['is_private'],
        )

        # Loop through parts and field prefixes to populate the SpeakingTest object
        for i in range(1, 11):
            for part in ['part1', 'part2', 'part3']:
                for prefix in ['question', 'thinking', 'speaking']:
                    field_name = f'{prefix}{i}_{part}'
                    if field_name in args:
                        setattr(speaking, field_name, args[field_name])

        # Add the speaking object to the database
        db.session.add(speaking)
        db.session.commit()

        return speaking, 201

    @marshal_with(speaking_resource_fields)
    def put(self, task_id):
        # Parse the arguments from the request
        args = create_test_args(request.method).parse_args()
        print(f"Received PUT request with data: {args}")
        # Get the existing SpeakingTest instance from the database
        speaking_test = SpeakingTest.query.get(task_id)
        # Check if the instance exists
        if not speaking_test:
            abort(404, message="SpeakingTest not found")
        # Update the instance with the provided arguments
        for key, value in args.items():
            if value is not None:
                setattr(speaking_test, key, value)

        print(f"Successfully updated SpeakingTest with ID {task_id}")

        # Commit the changes to the database
        db.session.commit()

        return speaking_test

    def delete(self, task_id):
        task = SpeakingTest.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()