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
            "duration": 1000,
            "speed": 100,
            "rgb": [255, 0, 0],
        },
        {
            "effectType": "static",
            "color": "rgb",
            "duration": 500,
            "speed": 100,
            "rgb": [50, 0, 0],
        },
        {
            "effectType": "static",
            "color": "rgb",
            "duration": 3000,
            "speed": 100,
            "rgb": [255, 0, 0],
        }
    ])
}

x = requests.post(url, data=my_obj)

print(x.text)
