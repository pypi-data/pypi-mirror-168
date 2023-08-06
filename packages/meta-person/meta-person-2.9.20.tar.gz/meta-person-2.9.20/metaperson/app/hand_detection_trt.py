import cv2
from ..model_zoo import TrtPredictor


class HandDetectionTrt:
    def __init__(self,
                 trt_file="models/hand.trt",
                 input_shape=(640, 640),
                 conf=0.01,
                 iou=0.45,
                 end2end=False):
        self.conf = conf
        self.iou = iou
        self.end2end = end2end
        self.model = TrtPredictor(engine_path=trt_file, imgsz=input_shape)

    def predict(self, image):
        dets = self.model.inference(image, conf=self.conf, iou=self.iou, end2end=self.end2end)
        return dets[:, :-1] if dets is not None else None

    def show(self, image, results):
        index = 1
        for (box, score) in zip(list(results[:, :-1].astype(int)), list(results[:, -1])):
            cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (255, 0, 255), 2)
            cv2.putText(image, 'id: %d, score: %.2f' % (index, score),
                        (box[0], box[1] - 4), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), thickness=2)
            index += 1
        return image
