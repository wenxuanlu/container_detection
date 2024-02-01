import os
import random
import shutil

def split_dataset(image_dir, label_dir, output_dir, train_ratio, val_ratio, test_ratio):
    assert train_ratio + val_ratio + test_ratio == 1.0, "The sum of ratios should be 1.0"

    # 创建输出文件夹和子文件夹
    os.makedirs(output_dir, exist_ok=True)
    train_dir = os.path.join(output_dir, 'images', 'train')
    val_dir = os.path.join(output_dir, 'images', 'val')
    test_dir = os.path.join(output_dir, 'images', 'test')
    train_label_dir = os.path.join(output_dir, 'labels', 'train')
    val_label_dir = os.path.join(output_dir, 'labels', 'val')
    test_label_dir = os.path.join(output_dir, 'labels', 'test')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(train_label_dir, exist_ok=True)
    os.makedirs(val_label_dir, exist_ok=True)
    os.makedirs(test_label_dir, exist_ok=True)

    # 获取图像文件列表
    image_files = os.listdir(image_dir)
    random.shuffle(image_files)

    # 计算数据集划分的索引位置
    num_samples = len(image_files)
    num_train = int(train_ratio * num_samples)
    num_val = int(val_ratio * num_samples)

    # 将图像和标签文件按比例划分到训练集、验证集和测试集
    train_files = image_files[:num_train]
    val_files = image_files[num_train:num_train + num_val]
    test_files = image_files[num_train + num_val:]

    for file in train_files:
        src_image_path = os.path.join(image_dir, file)
        src_label_path = os.path.join(label_dir, file.replace('.jpg', '.txt'))
        dst_image_path = os.path.join(train_dir, file)
        dst_label_path = os.path.join(train_label_dir, file.replace('.jpg', '.txt'))
        shutil.copy(src_image_path, dst_image_path)
        shutil.copy(src_label_path, dst_label_path)

    for file in val_files:
        src_image_path = os.path.join(image_dir, file)
        src_label_path = os.path.join(label_dir, file.replace('.jpg', '.txt'))
        dst_image_path = os.path.join(val_dir, file)
        dst_label_path = os.path.join(val_label_dir, file.replace('.jpg', '.txt'))
        shutil.copy(src_image_path, dst_image_path)
        shutil.copy(src_label_path, dst_label_path)

    for file in test_files:
        src_image_path = os.path.join(image_dir, file)
        src_label_path = os.path.join(label_dir, file.replace('.jpg', '.txt'))
        dst_image_path = os.path.join(test_dir, file)
        dst_label_path = os.path.join(test_label_dir, file.replace('.jpg', '.txt'))
        shutil.copy(src_image_path, dst_image_path)
        shutil.copy(src_label_path, dst_label_path)

# 使用示例
image_directory = '/Users/lwx/Desktop/voc/images'
label_directory = '/Users/lwx/Desktop/voc/labels'
output_directory = '/Users/lwx/Desktop'
train_ratio = 0.6    # 60% 划分为训练集
val_ratio = 0.2      # 20% 划分为验证集
test_ratio = 0.2     # 20% 划分为测试集
split_dataset(image_directory, label_directory, output_directory, train_ratio, val_ratio, test_ratio)

