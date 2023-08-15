import base64
from io import BytesIO
import json
import os
import numpy as np
from PIL import Image, ImageFile
import torch

ImageFile.LOAD_TRUNCATED_IMAGES = True


class Model:
    def __init__(self, model_dir):
        self.device = os.getenv('DEVICE')
        model_name = os.getenv('MODEL_NAME', 'yolov5s.pt')
        self.model = torch.hub.load(
            './yolov5',
            'custom',
            source='local',
            path=os.path.join(model_dir, model_name),
            force_reload=True
        ).to(self.device)

    def inference(self, img):
        output = self.model(img)
        return output

    def preprocess(self, data):
        data = json.loads(data)
        img = Image.open(
            BytesIO(base64.b64decode(data['image']))
        )
        img = np.array(img)
        return img
    
    def postprocess(self, output):
        n, c, im_h, im_w = output.s
        spent_ms = sum(output.t)
        xywh, confidence, names = (
            output.xywhn[0][:, :-2],
            output.xywhn[0][:, -2],
            output.xywhn[0][:, -1]
        )
        names = [self.model.names[int(x)] for x in names]
        total = len(names)
        return {
            'ok': 1,
            'total': total,
            'spent_ms': spent_ms,
            'objects': [
                {
                    'name': on,
                    'x': int(x * im_w),
                    'y': int(y * im_h),
                    'w': int(w * im_w),
                    'h': int(h * im_h),
                    'p': p
                }
                for on, (x, y, w, h), p in zip(
                    names,
                    xywh,
                    confidence
                )
            ]
        }
    
    def handle(self, data):
        img = self.preprocess(data)
        output = self.inference(img)
        try:
            response = self.postprocess(output)
        except Exception as e:
            response = {'ok': 0, 'details': str(e)}
        return json.dumps(response)
