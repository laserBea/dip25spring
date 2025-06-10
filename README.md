# 车牌检测与识别系统

## 项目简介

本项目基于数字图像处理技术，结合深度学习模型，实现了一个完整的车牌检测与识别系统。系统采用 YOLO 进行车牌定位，PaddleOCR 进行文字识别，并提供了基于 PyQt5 的可视化界面。

## 功能实现

### 基础图像处理功能
- 图像增强
  - 直方图均衡化
  - 图像锐化
  - 高斯模糊
  - 边缘增强
  - 图像降噪

### 高级功能
- 车牌检测与识别
  - 基于 YOLO 的车牌定位
  - 基于 PaddleOCR 的文字识别
  - 实时结果可视化

### 具体应用场景
- 智能交通管理
  - 车牌自动识别
  - 违章车辆检测
- 停车场管理
  - 车辆进出管理
  - 车位状态监控

## 技术实现

### 核心算法
- 车牌检测：YOLO (You Only Look Once)
  - 使用自定义数据集训练
  - 支持多车牌同时检测
- 文字识别：PaddleOCR
  - 使用 PP-OCRv5_server_rec 模型
  - 支持中英文车牌识别

### 图像处理
- 使用 OpenCV 进行图像预处理
- 实现了多种图像增强算法
- 支持实时图像处理

## 环境配置

### 系统要求
- Python >= 3.7

### 依赖安装
```bash
pip install -r requirements.txt
```

### 模型文件
- YOLO模型：`runs/detect/train5/weights/best.pt`
- PaddleOCR模型：自动下载

## 使用说明

1. 启动程序
```bash
python main.py
```

2. 基本操作
   - 打开图像：支持jpg、png、bmp格式
   - 图像增强：选择增强方式并应用
   - 车牌识别：自动检测并识别车牌
   - 保存结果：保存处理后的图像

## 项目结构
```
.
├── main.py             # 主程序入口
├── PTL.py              # 车牌识别核心算法
├── requirements.txt    # 依赖包列表
├── test.py             # 模型测试
├── runs/               # YOLO模型权重
│   └── detect/
│       └── train5/
│           └── weights/
│               └── best.pt    #车牌检测模型
├── utils/                  # 数据集工具
│   └── split.py            # CCPD数据集分割
│   └── convert2YOLO.py     # CCPD数据集转yolo格式
└── dataset/             # 训练数据集
```

## 引用说明

本项目使用了以下开源项目：
1. [YOLO](https://github.com/ultralytics/ultralytics)：用于车牌检测
2. [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)：用于文字识别
3. [OpenCV](https://opencv.org/)：用于图像处理
4. [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)：用于GUI界面
5. [CCPD](https://github.com/detectRecog/CCPD): 用于车牌检测模型训练

## 常见问题

1. 模型加载失败
   - 检查模型文件路径是否正确
   - 确认CUDA/anaconda环境配置

2. 识别效果不理想
   - 确保图像清晰度
   - 调整图像增强参数
   - 检查车牌是否完整可见

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。

## 许可证

本项目采用 MIT 许可证。 
