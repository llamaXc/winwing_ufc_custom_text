from ufc import UFCSimAppProHelper
import socket
import json

def send_json_udp_message(json_data, host='localhost', port=16536):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(json_data).encode('utf-8'), (host, port))

simapp_pro_start_messages = [
    {"func": "net", "msg": "ready"},
    {"func": "mission", "msg": "ready"},
    {"func": "mission", "msg": "start"},
    {"func": "mod", "msg": "FA-18C_hornet"}
]

# Connect to SimApp Pro and prepare to start receiving data
for payload in simapp_pro_start_messages:
    send_json_udp_message(payload)

# Create a UFC payload
ufc_payload = {
    "option1": "DCS", 
    "option2": "F18",
    "option3": "F15",
    "option4": "WW",
    "option5": "AIM9",
    "com1": "10",
    "com2": "4",
    "scratchPadNumbers": "115.800",
    "scratchPadString1": "X",
    "scratchPadString2": "Y",
    "selectedWindows": ["1"]
}
ufcHelper = UFCSimAppProHelper(ufc_payload)

# Create the SimApp Pro messaged it needs to update the UFC
simapp_pro_ufc_payload = {
    "args": {
        "FA-18C_hornet": ufcHelper.get_ufc_payload_string(),
    },
    "func": "addCommon",
    "timestamp": 0.00
}

simapp_pro_set_brightness = {
    "args": {
        "0": {
            "109": "0.95"
        }
    },
    "func": "addOutput",
    "timestamp": 0
}

# Send message to SimApp Pro
send_json_udp_message(simapp_pro_ufc_payload)
send_json_udp_message(simapp_pro_set_brightness)
