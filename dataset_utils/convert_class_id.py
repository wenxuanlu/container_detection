import os

def convert_labels(label_dir):
    classes = ['numberarea', 'specialarea', 'ding', 'carcode', 'heng_1', 'heng_2', 'heng_3', 'shu', 'type_heng', 'type_shu', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_0', '_1', '_2', '_3', '_4', '_5', '_6', '_7', '_8', '_9', 'closed', 'opened']

    label_files = os.listdir(label_dir)
    for label_file in label_files:
        if label_file.endswith('.txt'):
            label_path = os.path.join(label_dir, label_file)
            with open(label_path, 'r+') as f:
                lines = f.readlines()
                f.seek(0)
                for line in lines:
                    line = line.strip()
                    class_name, *coords = line.split(' ')
                    if class_name in classes:
                        class_index = classes.index(class_name)
                        new_line = str(class_index) + ' ' + ' '.join(coords)
                        f.write(new_line + '\n')
                    else:
                        f.write(line + '\n')
                f.truncate()

# 使用示例
label_directory = '/Users/lwx/Desktop/voc/label'
convert_labels(label_directory)

