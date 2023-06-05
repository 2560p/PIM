import urequests

# URL of the web server endpoint
url = 'http://webserver-endpoint'

# Data to send in the POST request
data = {'text': 'Hello, world!'}

# Send the POST request
response = urequests.post(url, json=data)

# Process the response, if needed
if response.status_code == 200:
    # Handle the response from the web server
    response_data = response.json()
    # Process the response data

# Close the connection
response.close()