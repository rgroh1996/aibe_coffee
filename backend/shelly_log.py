import time
import requests
import threading
import json
import os
from datetime import datetime

INTERVAL = 0.9 # query interval 
SAVE_INTERVAL = 10  # save file every seconds

url = "http://192.168.33.1/rpc/Shelly.GetStatus"

# The JSON-RPC payload
payload = {
    "jsonrpc": "2.0",
    "method": "Shelly.GetStatus",
    "params": {
        "id": 0
    },
    "id": 1  # The ID of the request
}

# Headers to indicate that the payload is in JSON format
headers = {
    "Content-Type": "application/json"
}

def test_connection():
    try: 
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=5) 
        response_data = response.json()
        return True
    except requests.exceptions.RequestException: 
        print("Shelly not connected")
        return False


def log_voltage_main(stop_signal, verbose=False): 
    # The URL to which you're sending the request
    last_save = datetime.now()
    current_day = datetime.now().day

    save_path = "./shelly_log/" + last_save.strftime("%Y-%m-%d.log")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Now, we can write logs at different levels of severity
    fp = open(save_path, "a")


    while not stop_signal.is_set(): 
        dt = datetime.now()
        # check for date switch 
        # if new day -- save csv, remove data
        if current_day != dt.day: 
            fp.close()
            save_path = "./shelly_log/" + dt.strftime("%Y-%m-%d.log")
            current_day = dt.day 
            last_save = dt
            fp = open(save_path, "a")

        # Making the POST request
        try: 
            response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=5)
            response_data = response.json()

            # Print the response
            power = response_data["switch:0"]["apower"]
            current = response_data["switch:0"]["current"]
            fp.write(dt.strftime("%Y-%m-%d--%H-%M-%S.%f") + f",{current:2.3f},{power:2.3f}\n")
            if verbose: 
                fp.write(dt.strftime("%Y-%m-%d--%H-%M-%S.%f") + f",{current:2.3f},{power:2.3f}\n")

        except requests.exceptions.RequestException: 
            fp.write(dt.strftime("%Y-%m-%d--%H-%M-%S.%f") + f",{-1:2.3f},{-1:2.3f}\n")

        if (dt - last_save).seconds > SAVE_INTERVAL: 
            fp.flush()
            last_save = dt

        time.sleep(INTERVAL)

    print("stop")
    fp.close()