import json
import requests

ucl = "https://ocr.asprise.com/api/v1/receipt"
image = ".png"

res = requests.post(url,
                    data = {
                        'api-key': 'TEST',
                        'recognizer': 'auto',
                        'ref_no': 'ocr_python_123'
                    },
                    files = {
                        'file': open(image, 'rb')
                    })

with open("result1.json", "w") as f:
    json.dump(json.loads(res.text), f)