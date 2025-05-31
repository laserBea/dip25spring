from ultralytics import YOLO
import cv2

path = 'runs/detect/train/weights/best.pt'

img_path = "test.jpg"

model = YOLO(path, task='detect')

results = model(img_path)
res = results[0].plot()

cv2.imshow("YOLO Detection", res)
cv2.waitKey(0)

