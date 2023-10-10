import requests
import base64
import json

def ocr_google_cloud(api_key, image_path):
    if image_path.startswith("http"):
        image = {
            "source": {
                "imageUri": image_path
            }
        }
    else:
        with open(image_path, 'rb') as image_file:
            img = image_file.read()
            content = base64.b64encode(img).decode()

        image = {
            "content": content
        }

    body = {
        "requests": [
            {
                "image": image,
                "features": [
                    {
                        "type": "TEXT_DETECTION"
                    }
                ]
            }
        ]
    }
    body = json.dumps(body)

    try:
        response = requests.post("https://vision.googleapis.com/v1/images:annotate?key={key}".format(key=api_key),
                                 data=body)
        json_resp = response.json()

        if "error" in json_resp:
            return json_resp["error"]["message"]
        if "responses" in json_resp:
            return json.dumps(json_resp["responses"])

    except Exception as e:
        return str(e)
