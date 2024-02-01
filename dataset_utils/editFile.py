import re
import xml.etree.ElementTree as ET
import os
import time
25  # !/usr/bin/python
# -*- coding:utf-8 -*-
# 批量替换txt中部分文字

inner_path = r'/Users/lwx/Desktop/voc'
# inner_path = r'E:\imgProcessing\commonPlate\area\Annotations'
filelist = os.listdir(inner_path)


def update_txt_general(path):
    # classes = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    classes = ["P", "S"]
    for number in classes:
        for root, dirs, files in os.walk(inner_path):
            old_str = r"<name>%s</name>" % number.lower()
            new_str = r"<name>%s</name>" % number.upper()
            for file in files:
                file_data = ""
                src = os.path.join(root, file)
                with open(src, "r", encoding="utf-8") as f:
                    for line in f:
                        if old_str in line:
                            line = line.replace(old_str, new_str)
                        file_data += line
                with open(src, "w", encoding="utf-8") as f:
                    f.write(file_data)


def update_txt(path):
    for root, dirs, files in os.walk(inner_path):
        old_str = r"unusual"
        new_str = r"normal"
        for file in files:
            file_data = ""
            src = os.path.join(root, file)
            with open(src, "r", encoding="utf-8") as f:
                for line in f:
                    if old_str in line:
                        print(file)
                        line = line.replace(old_str, new_str)
                    file_data += line
            with open(src, "w", encoding="utf-8") as f:
                f.write(file_data)


# 删除xml中部分节点
def delete_node(path):
    for root, dirs, files in os.walk(inner_path):
        for file in files:
            file_dir = os.path.join(inner_path, file)
            tree = ET.parse(file_dir)
            root = tree.getroot()
            for child in root.findall('object'):
                name = child.find('name').text
                if name == "normal" or name == "unusual":
                    root.remove(child)
            tree.write(
                r'C:\AWork\python\workspace\carbonBrush\Annotations\%s' % file)
            
# 根据xml节点删除xml文件和jpg
def delete_file():
    xml_path = r'E:\imgProcessing\carbonBrush\Annotations'
    jpg_path = r'E:\imgProcessing\carbonBrush\JPEGImages'
    for root, dirs, files in os.walk(xml_path):
        for file in files:
            file_dir = os.path.join(xml_path, file)
            tree = ET.parse(file_dir)
            root = tree.getroot()
            tag = False
            for child in root.findall('object'):
                name = child.find('name').text
                if name == "unusual":
                    tag = True
            if tag != True:
                os.remove(file_dir)
                os.remove(os.path.join(jpg_path, file.replace("xml","jpg")))

# 查找xml中名称大于5231且显示异常的节点


def check_node_2(path):
    for root, dirs, files in os.walk(inner_path):
        for file in files:
            file_dir = os.path.join(inner_path, file)
            tree = ET.parse(file_dir)
            root = tree.getroot()
            num = 0
            for child in root.findall('object'):
                name = child.find('name').text
                # if int(file.split('.')[0])>5231 and name == "unusual":
                # if name == "unusual":
                if name == "plate" or name == "customplate":
                    # print(file)
                    num += 1
            if num > 1:
                print(file)


# 检测xml标注类别不在names文件中的异常节点


def check_node(path):
    num = 0
    classes = ['numberarea', 'specialarea', 'ding', 'carcode', 'heng_1', 'heng_2', 'heng_3', 'shu', 'type_heng', 'type_shu', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
               'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_0', '_1', '_2', '_3', '_4', '_5', '_6', '_7', '_8', '_9', 'closed', 'opened']
    # classes = ['plate', 'unk', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'jing_beijing', 'jin_tianjin', 'ji_hebei', 'jin_shanxi', 'liao', 'ji_jilin', 'hei', 'hu', 'su', 'zhe', 'wan', 'min', 'gan_jiangxi', 'lu', 'yu_henan', 'e', 'xiang', 'yue', 'gui_guangxi', 'qiong', 'yu_chongqing', 'chuan', 'gui_guizhou', 'yun', 'zang', 'shan', 'gan_gansu', 'qing', 'ning', 'xin', 'meng', 'gang', 'ao', 'jing_jingcha']
    for root, dirs, files in os.walk(inner_path):
        for file in files:
            file_dir = os.path.join(inner_path, file)
            tree = ET.parse(file_dir)
            root = tree.getroot()
            for child in root.findall('object'):
                name = child.find('name').text
                if name not in classes:
                    print(file, name)
                    num += 1
            # tree.write(r'C:\AWork\python\workspace\carbonBrush\Annotations\%s' % file)
    print(num)


def update_node(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_dir = os.path.join(path, file)
            tree = ET.parse(file_dir)
            root = tree.getroot()

            folderName = root.find("folder")
            folderName.text = "JPEGImages"

            pathname = root.find("path")
            newPath = r"E:\imgProcessing\caseTop\JPEGImages\%s.jpg" % file[:-4]
            pathname.text = newPath

            filename = root.find("filename")
            newName = r"%s.jpg" % file[:-4]
            filename.text = newName

            # print("filename", filename.text)
            # print("realname", newPath)
            # print("filename", filename.tag)
            # print("filename", filename.attrib)
            tree.write(r'E:\imgProcessing\caseTop\Annotations\%s' % file)


def readTxt():
    data = ''
    with open(r"/Users/lwx/Desktop/voc/voc.names", "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = "\'" + line.strip() + "\', "
            data += line
    print(data)


if __name__ == '__main__':
    readTxt()
    # check_node(inner_path)
    #update_txt(inner_path)
    #  delete_node(inner_path)
    # check_node_2(inner_path)
    # update_node(inner_path)
    # update_txt_general(inner_path)
    # delete_file()
