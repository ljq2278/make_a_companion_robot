import requests
import queue
from lib.read_alound_and_show_text import read_alound_and_show_text
from lib.show_mood import show_mood
import time
import json

data_queue = queue.Queue()

server_url = "http://192.168.1.9:8001/expression/"

while True:
    json_data = {}
    response = requests.get(server_url)
    data = response.json()["data"]

    # Add the data to the queue
    if data != '':
        data_queue.put(data)

    # Remove the oldest item from the queue if it's full
    if data_queue.qsize() > 0:  # Adjust the queue size as needed
        json_data_str = data_queue.get()
        try:
            json_data = json.loads(json_data_str, encoding='utf-8')
        except Exception as e:
            print(e)
            pass

    # # Print the current queue contents
    # print(list(data_queue.queue))
    if 'mood' in json_data.keys():
        show_mood(json_data['mood'])
    if 'speech' in json_data.keys():
        read_alound_and_show_text(json_data['speech'])

    # # Wait for 1 second
    # time.sleep(1)
