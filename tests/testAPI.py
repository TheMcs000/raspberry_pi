import requests
import json

url = 'http://localhost:3000/effect'
my_obj = {
    "name": "tisch",
    "priority": 99,
    "effects": json.dumps([
        {
            "effectType": "static",
            "color": "rgb",
            "duration": 3000,
            "rgb": [0, 222, 111],
        },
        {
            "effectType": "static",
            "color": "rgb",
            "duration": 500,
            "rgb": [222, 222, 222],
        },
        {
            "effectType": "static",
            "color": "rgb",
            "duration": 1000,
            "rgb": [222, 0, 0],
        },
        {
            "effectType": "sweep",
            "color": "rgb",
            "duration": 1000,
            "rgb": [0, 255, 0],
        }
    ])
}

x = requests.post(url, data=my_obj)

print(x.text)
