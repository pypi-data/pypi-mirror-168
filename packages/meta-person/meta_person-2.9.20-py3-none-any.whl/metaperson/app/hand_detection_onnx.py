import cv2
from ..model_zoo import OnnxPredictor


class HandDetectionOnnx:
    def __init__(self,
                 onnx_file="models/hand.onnx",
                 input_shape=(640, 640),
                 conf=0.01,
                 iou=0.45,
                 end2end=False,
                 use_gpu=False):
        self.model = OnnxPredictor(onnx_file=onnx_file,
                                   input_shape=input_shape,
                                   conf=conf,
                                   iou=iou,
                                   end2end=end2end,
                                   use_gpu=use_gpu)

    def predict(self, image):
        dets = self.model.inference(image)
        return dets[:, :-1] if dets is not None else None

    def show(self, image, results):
        index = 1
        for (box, score) in zip(list(results[:, :-1].astype(int)), list(results[:, -1])):
            cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (255, 0, 255), 2)
            cv2.putText(image, 'id: %d, score: %.2f' % (index, score),
                        (box[0], box[1] - 4), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), thickness=2)
            index += 1
        return image
