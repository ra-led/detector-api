# detector-api
## Start server
```
docker compose up --build -d
```
## Intracte with server
Process image from `image_pth`
```python
import base64
import json
from io import BytesIO
import requests

image_path = ''

tmp = BytesIO()
Image.open(image_pth).save(tmp, format="PNG")
img64 = base64.b64encode(tmp.getvalue())

request_content = json.dumps({
    'image': img64.decode('utf-8'),
})

files = {
    'data': (None, request_content),
}

response = requests.post('http://127.0.0.1:5000/', files=files).json()

print(response)

```