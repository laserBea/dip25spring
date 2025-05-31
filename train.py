
from ultralytics import YOLO

def main():
    model = YOLO('runs/detect/train2/weights/last.pt')
    model.train(
        data='data.yaml',
        epochs=50,
        imgsz=640,
        batch=16,
        device=0
    )

if __name__ == '__main__':
    main()
