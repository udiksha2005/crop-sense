from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("yolov8n.pt")

def detect_leaf(image_bytes):

    file_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    results = model(img)

    boxes = results[0].boxes.xyxy

    if len(boxes) == 0:
        return image_bytes

    x1, y1, x2, y2 = map(int, boxes[0])

    cropped = img[y1:y2, x1:x2]

    success, encoded_image = cv2.imencode('.jpg', cropped)
    if success:
        return encoded_image.tobytes()
    else:
        return image_bytes