import requests
import json

BASE_URL = "http://127.0.0.1:5000/"

# Example data for the POST request
post_data = {
    "is_private": True,
}

# Add data for each part and question using loops
for part_suffix in [1, 2, 3]:
    # Add thinking and speaking time, and questions for each part
    for i in range(1, 31):
        post_data[f'thinking{i}_part{part_suffix}'] = 10  # Example thinking time
        post_data[f'speaking{i}_part{part_suffix}'] = 15  # Example speaking time
        post_data[f'question{i}_part{part_suffix}'] = f'Question {i} for Part {part_suffix}'  # Example question

# Add thinking and speaking time for part 2 (as you mentioned 2 parts for part 2)
post_data['thinking_part2'] = 20  # Example thinking time for part 2
post_data['speaking_part2'] = 25  # Example speaking time for part 2

# Make a POST request to your API endpoint
response = requests.post(f'{BASE_URL}/api/premium/speaking/questions/', json=data)
# Print the response
print(response.status_code)
print(response.json())  # Assuming your API returns JSON

# response = requests.get(BASE_URL+'/speaking')
# if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type', ''):
#     json_response = response.json()
#     formatted_json = json.dumps(json_response, indent=4)
#     print(formatted_json)
# else:
#     print(f"Failed to retrieve JSON. Status Code: {response.status_code}")
#     print(f"Response Content: {response.text}")

response = requests.put(BASE_URL+'/user/12345', json=user_data)
# Check the response status and content
print(f"Response Status Code: {response.status_code}")

if response.status_code == 200:
    updated_speaking_test = response.json()
    formatted_json = json.dumps(updated_speaking_test, indent=4)
    print(formatted_json)
else:
    print(f'Failed to update SpeakingTest. Status code: {response.status_code}, Content: {response.text}')