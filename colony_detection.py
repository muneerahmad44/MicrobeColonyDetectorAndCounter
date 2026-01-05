from ultralytics import YOLO
from collections import defaultdict
import cv2
model = YOLO('best_model/best_45.pt')

class DetectColony:
    def __init__(self):
        self.classes = [
            'B.subtilis',
            'P.aeruginosa',
            'E.coli',
            'S.aureus',
            'C.albicans',
            'Contamination',
            'Defect'
        ]
        self.count = defaultdict(int)
        self.results = None

    def detect_colonies(self, img):
        self.results = model(img, conf=0.3)
        return self.results

    def count_per_class(self):
        # reset counts
        if self.results==None:
            return "No Detections"
        self.count = defaultdict(int)

        for result in self.results:          # results is a list
            for box in result.boxes:
                class_id = int(box.cls.item())
                class_name = self.classes[class_id]
                self.count[class_name] += 1

        return dict(self.count)

    def post_process(self,img):
        if self.results==None:
            return "No Detections"
        for box in self.results[0].boxes:
            bbox=box.xyxy[0].cpu().numpy()
            cls=int(box.cls[0].cpu().numpy())
            cls_label=self.classes[cls]
            bbox=map(int,bbox)
            x1,y1,x2,y2=bbox

            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),5)
            cv2.putText(img,cls_label,(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255),4)

        return img