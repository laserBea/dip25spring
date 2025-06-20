import numpy as np
import cv2

def detect_plate_corners(cropped_img):
    # 检测图像中的四个角点（近似矩形）
    gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            return approx.reshape(4, 2)
    return None

def four_point_transform(image, pts):
    # 获取输入坐标点并进行透视变换
    rect = np.array(pts, dtype=np.float32)
    (tl, tr, br, bl) = rect

    # 计算变换后的宽度和高度
    width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(width_a), int(width_b))

    height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(height_a), int(height_b))

    # 定义目标图像的四个顶点
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")

    # 计算变换矩阵并应用透视变换
    m = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, m, (max_width, max_height))
    return warped

def plate_recognize(img, box, ocr):
    try:
        # 获取边界框坐标
        x1, y1, x2, y2 = map(int, box[:4])
        padding = 10
        # 确保坐标在有效范围内
        x1, y1 = max(x1 - padding, 0), max(y1 - padding, 0)
        x2, y2 = min(x2 + padding, img.shape[1] - 1), min(y2 + padding, img.shape[0] - 1)
        
        # 检查裁剪区域是否有效
        if x2 <= x1 or y2 <= y1 or x1 >= img.shape[1] or y1 >= img.shape[0]:
            return ""
            
        cropped_image = img[y1:y2, x1:x2]
        if cropped_image.size == 0:
            return ""

        # 图像增强
        try:
            gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
            gray = cv2.bilateralFilter(gray, 11, 17, 17)
            thresh = cv2.adaptiveThreshold(gray, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
            processed_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        except cv2.error:
            processed_img = cropped_image   # 如果图像处理失败，使用原始裁剪图像

        # 尝试检测四角点
        corners = detect_plate_corners(processed_img)
        if corners is not None:
            # 将角点坐标映射回原图
            corners[:, 0] += x1
            corners[:, 1] += y1
            warped_img = four_point_transform(processed_img, corners)
        else:
            warped_img = processed_img  # 如果检测不到角点，就用原始裁剪图像

        # OCR识别
        result = ocr.predict(warped_img)
        print(result)
        if not result or not result[0]:
            return ""

        # 提取文本
        if result and len(result) > 0:
            try:
                item = result[0]
                if 'rec_text' in item:
                    return item['rec_text']
                else:
                    return ""
            except (IndexError, KeyError, TypeError):
                return ""
        return ""


    except Exception as e:
        print(f"Error in plate recognition: {str(e)}")
        return ""

