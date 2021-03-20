import requests
import json

url = 'http://localhost:3000/effect'
myobj = {
    "name": "tisch",
    "effects": json.dumps([
        {
            "effectType": "static",
            "priority": 99,
            "color": "rgb",
            "duration": 3000,
            "rgb": [0, 222, 111],
        },
        {
            "effectType": "static",
            "priority": 99,
            "color": "rgb",
            "duration": 44,
            "rgb": [222, 222, 222],
        }
    ])
}

x = requests.post(url, data=myobj)

print(x.text)
