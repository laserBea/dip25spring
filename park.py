import time
from collections import defaultdict
import cv2
from main import ImageEnhancer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import sys

class ParkingLot:
    def __init__(self, hourly_rate=5):
        self.hourly_rate = hourly_rate  # 每小时收费
        self.active_vehicles = {}  # 车牌号: 入场时间戳
        self.history = defaultdict(list)  # 车牌号: [(入场时间, 出场时间, 费用)]
        self.image_enhancer = ImageEnhancer()

    def recognize_plate(self, image_path):
        """识别图片中的车牌号。"""
        self.image_enhancer.original_cv = cv2.imread(image_path)
        self.image_enhancer.detect_image()
        plate_texts = self.image_enhancer.label_text.text().replace("识别结果：", "").split(" | ")
        return plate_texts

    def enter(self, plate_number):
        """车辆入场，记录入场时间。"""
        if plate_number in self.active_vehicles:
            return f"车辆 {plate_number} 已在场内。"
        self.active_vehicles[plate_number] = time.time()
        return f"车辆 {plate_number} 入场成功。"

    def exit(self, plate_number):
        """车辆出场，计算费用。"""
        if plate_number not in self.active_vehicles:
            return f"车辆 {plate_number} 不在场内。"
        enter_time = self.active_vehicles.pop(plate_number)
        exit_time = time.time()
        hours = (exit_time - enter_time) / 3600
        fee = round(hours * self.hourly_rate, 2)
        self.history[plate_number].append((enter_time, exit_time, fee))
        return f"车辆 {plate_number} 出场，停车时长 {hours:.2f} 小时，应付 {fee} 元。"

    def get_status(self):
        """查询当前在场车辆。"""
        return list(self.active_vehicles.keys())

    def get_history(self, plate_number):
        """查询某车牌的历史记录。"""
        return self.history.get(plate_number, [])

class ParkingLotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1600, 1000)
        self.parking_lot = ParkingLot()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("停车场管理系统")
        layout = QVBoxLayout()

        self.btn_open = QPushButton("打开图片")
        self.btn_open.clicked.connect(self.open_image)
        layout.addWidget(self.btn_open)

        self.btn_enter = QPushButton("车辆入场")
        self.btn_enter.clicked.connect(self.enter_vehicle)
        layout.addWidget(self.btn_enter)

        self.btn_exit = QPushButton("车辆出场")
        self.btn_exit.clicked.connect(self.exit_vehicle)
        layout.addWidget(self.btn_exit)

        self.btn_status = QPushButton("查询在场车辆")
        self.btn_status.clicked.connect(self.show_status)
        layout.addWidget(self.btn_status)

        self.label_result = QLabel("识别结果：")
        layout.addWidget(self.label_result)

        # 添加图片展示区域
        self.label_image = QLabel("当前入场图片")
        self.label_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_image)

        self.setLayout(layout)

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "打开图片", "", "Images (*.png *.jpg *.bmp)")
        if path:
            plate_texts = self.parking_lot.recognize_plate(path)
            self.label_result.setText("识别结果：" + " | ".join(plate_texts))
            # 展示图片
            pixmap = QPixmap(path)
            self.label_image.setPixmap(pixmap.scaled(self.label_image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def enter_vehicle(self):
        plate_texts = self.label_result.text().replace("识别结果：", "").split(" | ")
        for plate in plate_texts:
            if plate:
                result = self.parking_lot.enter(plate)
                QMessageBox.information(self, "入场", result)

    def exit_vehicle(self):
        plate_texts = self.label_result.text().replace("识别结果：", "").split(" | ")
        for plate in plate_texts:
            if plate:
                result = self.parking_lot.exit(plate)
                QMessageBox.information(self, "出场", result)

    def show_status(self):
        status = self.parking_lot.get_status()
        QMessageBox.information(self, "在场车辆", "当前在场车辆：" + ", ".join(status))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParkingLotGUI()
    window.show()
    sys.exit(app.exec_()) 