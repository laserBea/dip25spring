from PIL import Image
import pytesseract
import cv2
import os



def simple_ocr(image_path, preprocess='blur'):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"错误：无法读取图像 {image_path}")
        return

    # 仅保留原有预处理逻辑
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    elif preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    # 使用内存中的图像直接识别（避免临时文件）
    text = pytesseract.image_to_string(
        Image.fromarray(gray),  # 直接从numpy数组创建PIL图像
        lang='chi_sim+eng',  # 中英文混合识别
        config='--psm 3'  # 自动页面分割模式
    )

    print("=" * 30 + "\n识别结果：")
    print(text.strip())
    print("=" * 30)

    # 显示结果
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 使用示例
simple_ocr(r'D:\MC\license.png', preprocess='blur')
