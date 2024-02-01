import os
import xml.etree.ElementTree as ET

def convert_xml_to_txt(xml_file, txt_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(txt_file, 'w') as f:
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)
            width = int(root.find('size/width').text)
            height = int(root.find('size/height').text)

            # 计算中心点坐标和宽高的比例
            center_x = (xmin + xmax) / (2.0 * width)
            center_y = (ymin + ymax) / (2.0 * height)
            bbox_width = (xmax - xmin) / float(width)
            bbox_height = (ymax - ymin) / float(height)

            line = f"{class_name} {center_x} {center_y} {bbox_width} {bbox_height}\n"
            f.write(line)

def batch_convert_xml_to_txt(xml_dir, txt_dir):
    os.makedirs(txt_dir, exist_ok=True)
    xml_files = os.listdir(xml_dir)
    for xml_file in xml_files:
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(xml_dir, xml_file)
            txt_file = xml_file.replace('.xml', '.txt')
            txt_path = os.path.join(txt_dir, txt_file)
            convert_xml_to_txt(xml_path, txt_path)

# 使用示例
xml_directory = '/Users/lwx/Desktop/voc/Annotations'
txt_directory = '/Users/lwx/Desktop/voc/label'
batch_convert_xml_to_txt(xml_directory, txt_directory)

