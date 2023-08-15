# detector-api
## Start server
```
docker compose up --build -d
```

## Endpoints

### GET 127.0.0.1/health
Response JSON:
```json
{"result": 1}
```

### POST 127.0.0.1/
Request JSON:
```json
{
    'image': 'img_in_base64',
}
```
Response JSON:
```json
{
    'ok': 1 if image was processed succesfully else 0,
    'total': count of detected objects,
    'spent_ms': milliseconds spent for inference,
    'objects': [
        {
            'name': First object name,
            'x': X of ceneter,
            'y': Y of center,
            'w': width in pixels,
            'h': hight in pixels,
            'p': confidence of detection
        }
        ...
        {
            'name': Last object name,
            'x': X of ceneter,
            'y': Y of center,
            'w': width in pixels,
            'h': hight in pixels,
            'p': confidence of detection
        }

    ]
}
```
## Intracte with server
Process image from `image_pth`
```python
import base64
import json
from io import BytesIO
from PIL import Image
import requests

image_pth = ''

tmp = BytesIO()
Image.open(image_pth).save(tmp, format="PNG")
img64 = base64.b64encode(tmp.getvalue())

request_content = json.dumps({
    'image': img64.decode('utf-8'),
})

files = {
    'data': (None, request_content),
}

response = requests.post('http://127.0.0.1/', files=files).json()

print(response)

```