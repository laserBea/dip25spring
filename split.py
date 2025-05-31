import os
import random
from shutil import copyfile

def select_data(src_path, dst_train_path, dst_val_path, dst_test_path, num):
    # 创建目标目录
    os.makedirs(dst_train_path, exist_ok=True)
    os.makedirs(dst_val_path, exist_ok=True)
    os.makedirs(dst_test_path, exist_ok=True)

    # 获取图片列表
    images = [img for img in os.listdir(src_path) if img.endswith(".jpg")]
    if len(images) < num:
        print(f"[警告] {src_path} 中图片不足 {num} 张，仅使用 {len(images)} 张")
        num = len(images)

    # 随机抽样
    random.seed(0)
    selected = random.sample(images, num)

    # 8:1:1 划分
    train_num = int(num * 0.8)
    val_num = int(num * 0.1)
    test_num = num - train_num - val_num

    train_imgs = selected[:train_num]
    val_imgs = selected[train_num:train_num + val_num]
    test_imgs = selected[train_num + val_num:]

    # 拷贝文件
    for img in train_imgs:
        copyfile(os.path.join(src_path, img), os.path.join(dst_train_path, img))

    for img in val_imgs:
        copyfile(os.path.join(src_path, img), os.path.join(dst_val_path, img))

    for img in test_imgs:
        copyfile(os.path.join(src_path, img), os.path.join(dst_test_path, img))

    print(f"{os.path.basename(src_path)}  训练: {len(train_imgs)} 验证: {len(val_imgs)} 测试: {len(test_imgs)}")

if __name__ == "__main__":
    # CCPD19原始数据路径
    root = "E:/BaiduNetdiskDownload/CCPD2019"
    dataset_info = {
        "ccpd_base": 0,
        "ccpd_challenge": 200,
        "ccpd_db": 200,
        "ccpd_fn": 200,
        "ccpd_rotate": 200,
        "ccpd_tilt": 200,
        "ccpd_weather": 200
    }

    # 输出路径
    output_root = "D:/documents/code/py/dip/ccpd_blue"
    train_path = os.path.join(output_root, "train")
    val_path = os.path.join(output_root, "val")
    test_path = os.path.join(output_root, "test")

    # 执行划分
    for subfolder, num in dataset_info.items():
        src_path = os.path.join(root, subfolder)
        select_data(
            src_path=src_path,
            dst_train_path=train_path,
            dst_val_path=val_path,
            dst_test_path=test_path,
            num=num
        )

    # # CCPD20原始数据路径
    # root = "E:/BaiduNetdiskDownload/CCPD2020/CCPD2020/ccpd_green"
    # dataset_info = {
    #     "img": 5300
    # }
    #
    # # 输出路径
    # output_root = "D:/documents/code/py/dip/ccpd_green"
    # train_path = os.path.join(output_root, "train")
    # val_path = os.path.join(output_root, "val")
    # test_path = os.path.join(output_root, "test")
    #
    # # 执行划分
    # for subfolder, num in dataset_info.items():
    #     src_path = os.path.join(root, subfolder)
    #     select_data(
    #         src_path=src_path,
    #         dst_train_path=train_path,
    #         dst_val_path=val_path,
    #         dst_test_path=test_path,
    #         num=num
    #     )
