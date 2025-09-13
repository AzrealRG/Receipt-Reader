import json
import requests
import os

folder_path = "/ReciptReader/Receipts"
for filename in os.listdir("recipts"):
    if filename.lower().endswith(".jpg", ".jpeg", ".png"):
        file_path = os.path.join(folder_path, filename)
    else:
        continue
    url = "https://ocr.asprise.com/api/v1/receipt"
    image = file_path

    res = requests.post(url,
                        data = {
                            'api-key': 'TEST',
                            'recognizer': 'auto',
                            'ref_no': 'ocr_python_123'
                        },
                        files = {
                            'file': open(image, 'rb')
                        })

    with open(f"results/{filename}.json", "w") as f:
        json.dump(json.loads(res.text), f)

