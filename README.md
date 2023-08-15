# detector-api
## Start server
1. Clone repo
```
git clone https://github.com/ra-led/detector-api.git && cd detector-api
```
2. Create `model_dir` in root of repo and
```
mkdir model_dir
```
3. Save there `yolov5{size}.pt` (ex, `/model_dir/yolov5s.pt`)
```
wget https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt
mv ./yolov5s.pt ./model_dir/yolov5s.pt
```
3. Run doker compos
```
docker compose up --build -d
```

## Endpoints

### GET 127.0.0.1/health
Response JSON:
```
{"result": 1}
```

### POST 127.0.0.1/
Request JSON:
```
{
    'image': 'img_in_base64',
}
```
Response JSON:
```
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