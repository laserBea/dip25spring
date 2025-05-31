# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFileDialog, QMessageBox, QSizePolicy, QComboBox
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from paddleocr import TextRecognition
from ultralytics import YOLO
from PTL import *


class ImageEnhancer(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1600, 1000)
        self.original_cv = None
        self.processed_cv = None
        self.original_pixmap = None
        self.processed_pixmap = None
        self.model = YOLO('runs/detect/train4/weights/best.pt')
        self.ocr = TextRecognition(model_name="PP-OCRv5_server_rec")
        self.init_ui()

    def init_ui(self):
        self.label_original = QLabel("原图")
        self.label_result = QLabel("增强后")
        for label in [self.label_original, self.label_result]:
            label.setAlignment(Qt.AlignCenter)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            label.setScaledContents(False)  # 禁止自动拉伸，保持长宽比

        self.combo_enhance = QComboBox()
        self.combo_enhance.addItems([
            "直方图均衡化",
            "锐化",
            "高斯模糊",
            "边缘增强",
            "降噪"
        ])

        self.btn_open = QPushButton("打开图像")
        self.btn_open.clicked.connect(self.open_image)
        self.btn_enhance = QPushButton("增强图片")
        self.btn_enhance.clicked.connect(self.enhance_image)
        self.btn_save = QPushButton("保存结果")
        self.btn_save.clicked.connect(self.save_image)
        self.btn_detect = QPushButton("识别车牌")
        self.btn_detect.clicked.connect(self.detect_image)
        self.label_text = QLabel("识别结果：")
        self.label_text.setAlignment(Qt.AlignCenter)

        layout_main = QVBoxLayout()
        layout_imgs = QHBoxLayout()
        layout_imgs.addWidget(self.label_original)
        layout_imgs.addWidget(self.label_result)
        layout_main.addWidget(self.label_text)

        layout_controls = QHBoxLayout()
        layout_controls.addWidget(self.btn_open)
        layout_controls.addWidget(self.combo_enhance)
        layout_controls.addWidget(self.btn_enhance)
        layout_controls.addWidget(self.btn_detect)
        layout_controls.addWidget(self.btn_save)

        layout_main.addLayout(layout_imgs)
        layout_main.addLayout(layout_controls)

        self.setLayout(layout_main)
        self.setWindowTitle("图像增强工具")

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "打开图片", "", "Images (*.png *.jpg *.bmp)")
        if path:
            self.original_cv = cv2.imread(path)
            self.update_pixmaps()
            self.update_display()

    def enhance_image(self):
        if self.original_cv is None:
            QMessageBox.warning(self, "提示", "请先打开图片")
            return

        method = self.combo_enhance.currentText()
        img = self.original_cv.copy()

        if method == "直方图均衡化":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            enhanced = cv2.equalizeHist(gray)
            self.processed_cv = enhanced

        elif method == "锐化":
            kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
            sharpened = cv2.filter2D(img, -1, kernel)
            self.processed_cv = sharpened

        elif method == "高斯模糊":
            blurred = cv2.GaussianBlur(img, (7, 7), 0)
            self.processed_cv = blurred

        elif method == "边缘增强":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            self.processed_cv = edges

        elif method == "降噪":
            denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
            self.processed_cv = denoised

        else:
            QMessageBox.warning(self, "提示", "未知的增强类型")
            return

        self.update_pixmaps()
        self.update_display()

    def detect_image(self):
        if self.original_cv is None:
            QMessageBox.warning(self, "提示", "请先打开图片")
            return

        image = self.original_cv.copy()
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.model(image_rgb)
        annotated_frame = results[0].plot()

        plate_texts = []
        for box in results[0].boxes.xyxy:
            if hasattr(box, 'cpu'):
                box = box.cpu().numpy()
            plate = plate_recognize(image, box, self.ocr)
            plate_texts.append(plate)

        self.label_text.setText("识别结果：" + " | ".join(plate_texts))

        self.processed_cv = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
        self.update_pixmaps()
        self.update_display()

    def save_image(self):
        if self.processed_cv is None:
            QMessageBox.warning(self, "提示", "请先处理图片")
            return
        path, _ = QFileDialog.getSaveFileName(self, "保存图片", "", "PNG Files (*.png);;JPEG Files (*.jpg)")
        if path:
            cv2.imwrite(path, self.processed_cv)
            QMessageBox.information(self, "成功", f"保存成功: {path}")

    def update_pixmaps(self):
        if self.original_cv is not None:
            self.original_pixmap = self.cv2_to_pixmap(self.original_cv)

        if self.processed_cv is not None:
            self.processed_pixmap = self.cv2_to_pixmap(
                self.processed_cv, is_gray=(len(self.processed_cv.shape) == 2)
            )

    def update_display(self):
        if self.original_pixmap:
            self.label_original.setPixmap(self.original_pixmap.scaled(
                self.label_original.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        if self.processed_pixmap:
            self.label_result.setPixmap(self.processed_pixmap.scaled(
                self.label_result.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))

    def resizeEvent(self, event):
        self.update_display()

    def cv2_to_pixmap(self, img, is_gray=False):
        if is_gray:
            qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_Grayscale8)
        else:
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            qimg = QImage(rgb_img.data, rgb_img.shape[1], rgb_img.shape[0], rgb_img.strides[0], QImage.Format_RGB888)
        return QPixmap.fromImage(qimg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEnhancer()
    window.show()
    sys.exit(app.exec_())
