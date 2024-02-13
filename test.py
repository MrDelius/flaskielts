import requests
import json

BASE_URL = "http://127.0.0.1:5000/"

# Generate sample data
data = {
    'chat_id': 123,
    'is_private': True,
    'created_at': '2022-01-01T00:00:00',  # Replace with the actual date and time
    'updated_at': '2022-01-01T00:00:00',  # Replace with the actual date and time
}

# Add sample data for questions, thinking, and speaking parts
for i in range(1, 3):
    data[f'question{i}_part1'] = f'The Question {i} for Part 1'
    data[f'thinking{i}_part1'] = i * 10
    data[f'speaking{i}_part1'] = i * 5

    data[f'question{i}_part2'] = f'The Question {i} for Part 2'
    data[f'thinking{i}_part2'] = i * 8
    data[f'speaking{i}_part2'] = i * 4

    data[f'question{i}_part3'] = f'The Question {i} for Part 3'
    data[f'thinking{i}_part3'] = i * 6
    data[f'speaking{i}_part3'] = i * 3

# # Make a POST request to your API endpoint
# response = requests.put(f'{BASE_URL}/speaking', json=data)
# # Print the response
# print(response.status_code)
# print(response.json())  # Assuming your API returns JSON

# response = requests.get(BASE_URL+'/speaking')
# if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type', ''):
#     json_response = response.json()
#     formatted_json = json.dumps(json_response, indent=4)
#     print(formatted_json)
# else:
#     print(f"Failed to retrieve JSON. Status Code: {response.status_code}")
#     print(f"Response Content: {response.text}")
print(data)
response = requests.put(BASE_URL+'/speaking/1', json=data)
# Check the response status and content
print(f"Response Status Code: {response.status_code}")

if response.status_code == 200:
    updated_speaking_test = response.json()
    formatted_json = json.dumps(updated_speaking_test, indent=4)
    print(formatted_json)
else:
    print(f'Failed to update SpeakingTest. Status code: {response.status_code}, Content: {response.text}')


"""{
        'speaking_test': {'chat_id':'...',
                        'is_private': '...', ......,
                        'part1': {'question1': '...',
                                  'thinking1_part1': '...',
                                  'speaking1_part1': '...',
                                  until 10},
                        'part2': {'question1_part2': '...',
                                  'thinking1_part2': '...',
                                  'speaking1_part2': '...',
                                  until 10},
                        'part3': {'question1_part3': '...',
                                  'thinking1_part3': '...',
                                  'speaking1_part3': '...',
                                  until 10}
}
"""