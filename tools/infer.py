import argparse
import os
import sys
import os.path as osp
import re
import torch

ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))


from yolov6.utils.events import LOGGER
from yolov6.core.inferer import Inferer


def get_args_parser(add_help=True):
    parser = argparse.ArgumentParser(description='YOLOv6 PyTorch Inference.', add_help=add_help)
    parser.add_argument('--weights', type=str, default='weights/yolov6s.pt', help='model path(s) for inference.')
    parser.add_argument('--source', type=str, default='data/images', help='the source path, e.g. image-file/dir.')
    parser.add_argument('--webcam', action='store_true', help='whether to use webcam.')
    parser.add_argument('--webcam-addr', type=str, default='0', help='the web camera address, local camera or rtsp address.')
    parser.add_argument('--yaml', type=str, default='data/coco.yaml', help='data yaml file.')
    parser.add_argument('--img-size', nargs='+', type=int, default=[640, 640], help='the image-size(h,w) in inference size.')
    parser.add_argument('--conf-thres', type=float, default=0.8, help='confidence threshold for inference.')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold for inference.')
    parser.add_argument('--max-det', type=int, default=1000, help='maximal inferences per image.')
    parser.add_argument('--device', default='0', help='device to run our model i.e. 0 or 0,1,2,3 or cpu.')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt.')
    parser.add_argument('--not-save-img', action='store_true', help='do not save visuallized inference results.')
    parser.add_argument('--save-dir', type=str, help='directory to save predictions in. See --save-txt.')
    parser.add_argument('--view-img', action='store_true', help='show inference results')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by classes, e.g. --classes 0, or --classes 0 2 3.')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS.')
    parser.add_argument('--project', default='runs/inference', help='save inference results to project/name.')
    parser.add_argument('--name', default='exp', help='save inference results to project/name.')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels.')
    parser.add_argument('--hide-conf', default=True, action='store_true', help='hide confidences.')
    parser.add_argument('--half', action='store_true', help='whether to use FP16 half-precision inference.')

    args = parser.parse_args()
    LOGGER.info(args)
    return args


@torch.no_grad()
def run(weights,
        source,
        webcam=False,
        webcam_addr=0,
        yaml=None,
        img_size=640,
        conf_thres=0.8,
        iou_thres=0.45,
        max_det=1000,
        device='',
        save_txt=False,
        not_save_img=False,
        save_dir=None,
        view_img=False,
        classes=None,
        agnostic_nms=False,
        project=osp.join(ROOT, 'runs/inference'),
        name='exp',
        hide_labels=True,
        hide_conf=True,
        half=False,
        ):
    """ Inference process, supporting inference on one image file or directory which containing images.
    Args:
        weights: The path of model.pt, e.g. yolov6s.pt
        source: Source path, supporting image files or dirs containing images.
        yaml: Data yaml file, .
        img_size: Inference image-size, e.g. 640
        conf_thres: Confidence threshold in inference, e.g. 0.25
        iou_thres: NMS IOU threshold in inference, e.g. 0.45
        max_det: Maximal detections per image, e.g. 1000
        device: Cuda device, e.e. 0, or 0,1,2,3 or cpu
        save_txt: Save results to *.txt
        not_save_img: Do not save visualized inference results
        classes: Filter by class: --class 0, or --class 0 2 3
        agnostic_nms: Class-agnostic NMS
        project: Save results to project/name
        name: Save results to project/name, e.g. 'exp'
        line_thickness: Bounding box thickness (pixels), e.g. 3
        hide_labels: Hide labels, e.g. False
        hide_conf: Hide confidences
        half: Use FP16 half-precision inference, e.g. False
    """
    # create save dir
    if save_dir is None:
        save_dir = osp.join(project, name)
        save_txt_path = osp.join(save_dir, 'labels')
    else:
        save_txt_path = save_dir
    if (not not_save_img or save_txt) and not osp.exists(save_dir):
        os.makedirs(save_dir)
    else:
        LOGGER.warning('Save directory already existed')
    if save_txt:
        save_txt_path = osp.join(save_dir, 'labels')
        if not osp.exists(save_txt_path):
            os.makedirs(save_txt_path)

    # Inference
    inferer = Inferer(source, webcam, webcam_addr, weights, device, yaml, img_size, half)#参数来自**vars(args)和run()函数的默认参数
   

    #从source里取出图片并改为txt
    last_slash_index = source.rfind("/")
    file_name_with_extension = source[last_slash_index + 1:]
    txt_gen = file_name_with_extension.rsplit(".", 1)[0] + ".txt"
    img_gen = file_name_with_extension.rsplit(".", 1)[0] + ".jpg"
    #要生成的对应的txt和图片的路径
    txt_path_gen = osp.join(ROOT, 'runs/inference/exp/labels', txt_gen)
    img_path_gen = osp.join(ROOT, 'runs/inference/exp', img_gen)

    #判断txt文件是否存在
    if not os.path.exists(img_path_gen) and not os.path.exists(txt_path_gen):
        inferer.infer(conf_thres, iou_thres, classes, agnostic_nms, max_det, save_dir, save_txt, not not_save_img, hide_labels, hide_conf, view_img)
        LOGGER.info(f"Results saved to {save_dir}")

    judge = yaml.split('/')[-1].split('.')[0]
    if judge == 'dataset':
        ans = convert_yanzhengma(txt_path_gen)
    elif judge == 'xiangzi_data':
        ans = convert_xiangzi(txt_path_gen)
    else:
        print('yaml文件名不对')
     
    return ans

def convert_yanzhengma(txt_path_gen):
    # 定义数字到字符的映射关系
    print(txt_path_gen)
    char_mapping = {
    0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
    10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g', 17: 'h', 18: 'i', 19: 'j',
    20: 'k', 21: 'l', 22: 'm', 23: 'n', 24: 'o', 25: 'p', 26: 'q', 27: 'r', 28: 's', 29: 't',
    30: 'u', 31: 'v', 32: 'w', 33: 'x', 34: 'y', 35: 'z', 36: 'A', 37: 'B', 38: 'C', 39: 'D',
    40: 'E', 41: 'F', 42: 'G', 43: 'H', 44: 'I', 45: 'J', 46: 'K', 47: 'L', 48: 'M', 49: 'N',
    50: 'O', 51: 'P', 52: 'Q', 53: 'R', 54: 'S', 55: 'T', 56: 'U', 57: 'V', 58: 'W', 59: 'X',
    60: 'Y', 61: 'Z'}

    # 读取标签文件内容
    with open(txt_path_gen, "r") as file:
        labels = file.readlines()

    # 提取标签中的数字和坐标信息
    label_data = []
    for label in labels:
        #切分标签
        label_ = label.split(" ")
        if True:
            class_id = int(label_[0])
            center_x = float(label_[1])
            center_y = float(label_[2])
            width = float(label_[3])
            height = float(label_[4])
            confidence = float(label_[5])
            label_data.append((class_id, center_x, center_y, width, height, confidence))

    # 按照 center_x 从小到大排序
    label_data.sort(key=lambda x: x[1])

    # 将数字转换为字符，并按列输出
    output_txt = ""
    for item in label_data:
        class_id = char_mapping[item[0]]
        output_txt += class_id

    # 输出结果
    print(output_txt)
    return output_txt



def convert_xiangzi(txt_path_gen):
    #凡是type_开头的标签和被框在里边的标签都忽略掉
    #不考虑numberarea specialarea ding carcode和closed opened
    #之后，根据时heng还是shu来排序，分两类情况
    char_mapping = {
    0: 'numberarea', 1: 'specialarea', 2: 'ding', 3: 'carcode', 4: 'heng_1', 5: 'heng_2', 6: 'heng_3',
    7: 'shu', 8: 'type_heng', 9: 'type_shu', 10: '0', 11: '1', 12: '2', 13: '3', 14: '4', 15: '5',
    16: '6', 17: '7', 18: '8', 19: '9', 20: 'A', 21: 'B', 22: 'C', 23: 'D', 24: 'E', 25: 'F',
    26: 'G', 27: 'H', 28: 'I', 29: 'J', 30: 'K', 31: 'L', 32: 'M', 33: 'N', 34: 'O', 35: 'P',
    36: 'Q', 37: 'R', 38: 'S', 39: 'T', 40: 'U', 41: 'V', 42: 'W', 43: 'X', 44: 'Y', 45: 'Z',
    46: '_0', 47: '_1', 48: '_2', 49: '_3', 50: '_4', 51: '_5', 52: '_6', 53: '_7', 54: '_8',
    55: '_9', 56: 'closed', 57: 'opened'
}
    # 读取标签文件内容
    with open(txt_path_gen, "r") as file:
        labels = file.readlines()
        
    # 提取标签中的数字和坐标信息
    label_data = []
    label_data_1 = []#heng_1~heng_3分开
    label_data_2 = []
    label_data_3 = []
    type_id = 0

    X_limit_min = 0
    X_limit_max = 0
    Y_limit_min = 0
    Y_limit_max = 0

    limit_id = 0

    #找序号为8和9的框，确定边界,为了丢弃
    for label in labels:
        #切分标签
        label_tmp = label.split(" ")
        if True:
            class_id = int(label_tmp[0])
            center_x = float(label_tmp[1])
            center_y = float(label_tmp[2])
            width = float(label_tmp[3])
            height = float(label_tmp[4])
            if class_id == 8 or class_id == 9:
                X_limit_max = center_x + width / 2
                X_limit_min = center_x - width / 2
                Y_limit_max = center_y + height / 2
                Y_limit_min = center_y - height / 2
                type_id = class_id  
                break
            else:
                continue
    
    #找heng和shu的框，确定边界，确定输出格式
    for label in labels:
        #切分标签
        label_tmp = label.split(" ")
        
        class_id = int(label_tmp[0])
        center_x = float(label_tmp[1])
        center_y = float(label_tmp[2])
        width = float(label_tmp[3])
        height = float(label_tmp[4])
        confidence = float(label_tmp[5])
        if class_id == 4 or class_id == 5 or class_id == 6:
            limit_id = class_id
            break
        elif class_id == 7:
            limit_id = class_id
            break
        else:
            continue


    #遍历，选出序号
    for label in labels:
        #切分标签
        label_ = label.split(" ")
        if True:
            class_id = int(label_[0])
            center_x = float(label_[1])
            center_y = float(label_[2])
            width = float(label_[3])
            height = float(label_[4])
            confidence = float(label_[5])
            if not class_id == 8 and not class_id == 9 and not class_id == 4 and not class_id == 5 and not class_id == 6 and not class_id == 7:
                if type_id != 0:
                    if not (center_x > X_limit_min and center_x < X_limit_max and center_y > Y_limit_min and center_y < Y_limit_max):
                        label_data.append((class_id, center_x, center_y, width, height, confidence))
                else:
                    label_data.append((class_id, center_x, center_y, width, height, confidence))
            else:
                continue

    #先看type_id，再看limit_id，再看坐标，type_id和limit_id一致
    if type_id == 8:
        if limit_id == 4:#heng_1
            label_data.sort(key=lambda x: x[1])
        elif limit_id == 5:#heng_2
            label_data.sort(key=lambda x: x[2])
            threshold = (label_data[0][2] + label_data[-1][2]) / 2
            # 将框分配到对应的簇
            for box in label_data:
                if box[2] < threshold:
                    label_data_1.append(box)
                else:
                    label_data_2.append(box)
            label_data_1.sort(key=lambda x: x[1])
            label_data_2.sort(key=lambda x: x[1])
        elif limit_id == 6:#heng_3
            label_data.sort(key=lambda x: x[2])
            threshold1 = label_data[0][2] + (label_data[-1][2] - label_data[0][2]) / 3
            threshold2 = label_data[0][2] + 2 * (label_data[-1][2] - label_data[0][2]) / 3
            # 将框分配到对应的簇
            for box in label_data:
                if box[2] < threshold1:
                    label_data_1.append(box)
                elif box[2] < threshold2:
                    label_data_2.append(box)
                else:
                    label_data_3.append(box)
            label_data_1.sort(key=lambda x: x[1])
            label_data_2.sort(key=lambda x: x[1])
            label_data_3.sort(key=lambda x: x[1])
        else:
            print("error")
    elif type_id == 9:
        assert limit_id == 7
        label_data.sort(key=lambda x: x[2]) 
    else:
        print("error")

    #输出
    output_txt = ""
    if limit_id == 7:
        for item in label_data:
            class_id = char_mapping[item[0]]
            output_txt += class_id
            output_txt += "\n"
    elif limit_id == 4:
        for item in label_data:
            class_id = char_mapping[item[0]]
            output_txt += class_id
            output_txt += " "
    elif limit_id == 5:
        for item in label_data_1:
            class_id = char_mapping[item[0]]
            output_txt += class_id
            output_txt += " "
        output_txt += "\n"
        for item in label_data_2:
            class_id = char_mapping[item[0]]
            output_txt += class_id
            output_txt += " "
        output_txt += "\n"
    elif limit_id == 6:
        for item in label_data_1:
            class_id = char_mapping[item[0]]
            output_txt += class_id
            output_txt += " "
        output_txt += "\n"
        for item in label_data_2:
            class_id = char_mapping[item[0]]
            output_txt += class_id
            output_txt += " "
        output_txt += "\n"
        for item in label_data_3:
            class_id = char_mapping[item[0]]
            output_txt += class_id
            output_txt += " "
        output_txt += "\n"
    else:
        print("error")

    # 输出结果
    print(output_txt)
    return output_txt
# def main(args):
#     run(args) #vars() 函数返回对象object的属性和属性值的字典对象。#**kwargs表示将字典扩展为关键字参数,相当于run(weights=osp.join(ROOT, 'yolov6s.pt'),source=osp.join(ROOT, 'data/images'),webcam=False,webcam_addr=0,yaml=None,img_size=640,conf_thres=0.7,iou_thres=0.45,max_det=1000,device='',save_txt=False,not_save_img=False,save_dir=None,view_img=True,classes=None,agnostic_nms=False,project=osp.join(ROOT, 'runs/inference'),name='exp',hide_labels=True,hide_conf=True,half=False, )


# if __name__ == "__main__":
#     args = get_args_parser()
#     print(type(vars(args)))
#     print(vars(args))
#     main(args)
