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
            "speed": 100,
            "rgb": [0, 222, 111],
        }
    ])
}

x = requests.post(url, data=my_obj)

print(x.text)
