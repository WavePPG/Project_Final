# app.py
import requests
import time
import dobot as dobot_module

# URL of the web server
SERVER_URL = 'http://10.80.83.192:5000/get_direction'

# Initialize Dobot connection
dobot = dobot_module.connect()

def get_direction():
    response = requests.get(SERVER_URL)
    if response.status_code == 200:
        data = response.json()
        return data['direction']
    return None

def control_dobot(direction):
    if direction == 'left':
        dobot_module.GoLeft()
    elif direction == 'right':
        dobot_module.GoRight()
    elif direction == 'up':
        dobot_module.GoUp()
    elif direction == 'down':
        dobot_module.GoDown()
    elif direction == 'stop':
        print("Stopping Dobot")
        # You might want to implement a stop function in dobot.py if needed

if __name__ == '__main__':
    while True:
        direction = get_direction()
        if direction:
            control_dobot(direction)
        time.sleep(1)  # Wait for 1 second before checking direction again
