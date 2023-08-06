import cv2
import numpy as np
import onnxruntime
from ..utils import multiclass_nms


def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, r, (dw, dh)


class OnnxPredictor:
    def __init__(self,
                 onnx_file='models/hand.onnx',
                 input_shape=(640, 640),
                 conf=0.1,
                 iou=0.45,
                 end2end=False,
                 use_gpu=False):
        self.input_shape = input_shape
        self.conf = conf
        self.iou = iou
        self.end2end = end2end
        self.n_classes = 1
        self.class_names = ['hand']
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if use_gpu else ['CPUExecutionProvider']
        self.session = onnxruntime.InferenceSession(onnx_file, providers=providers)
        self.input_names = [i.name for i in self.session.get_inputs()]
        self.output_names = [i.name for i in self.session.get_outputs()]

    def inference(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img, ratio, dwdh = letterbox(img, auto=False)
        img = img.transpose((2, 0, 1))
        img = np.expand_dims(img, 0)
        img = np.ascontiguousarray(img)
        img = img.astype(np.float32) / 255

        data = self.session.run(self.output_names, {self.input_names[0]: img})[0]

        predictions = np.reshape(data, (1, -1, int(5 + self.n_classes)))[0]
        dets = self.postprocess(predictions, ratio, dwdh, self.conf, self.iou)
        return dets

    @staticmethod
    def postprocess(predictions, ratio, dwdh, score_thr, nms_thr):
        boxes = predictions[:, :4]
        scores = predictions[:, 4:5] * predictions[:, 5:]
        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2.
        boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2.
        boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2.
        boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2.
        boxes_xyxy -= np.array(dwdh * 2)
        boxes_xyxy /= ratio
        dets = multiclass_nms(boxes_xyxy, scores, nms_thr=nms_thr, score_thr=score_thr)
        return dets
