import json
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
# import sys
# sys.path.append(current_dir)
import cv2
import shutil

import xml.dom.minidom
# parse the XML file
# xml_doc = xml.dom.minidom.parse('travel_pckgs.xml')
# get the root element
# root = xml_doc.documentElement
# print('Root is',root)

path = 'gbt_fish_dtset1.json'  # 100/100400
# path = 'gbt_fish_dtset2.json'  # 102/100400 but 100500
# path = 'gbt_fish_dtset3.json'  # 84/100400 but 100500
# path = 'gbt_fish_dtset4.json'  # 110/100400 but 100500
# path = 'gbt_fish_dtset.json'  # 60/50200 validation
i1 = 'U.S.-Coins-Dataset---A.Tatham-5/train/images/0e1f9578-20220629_181429_jpg.rf.3a8a6299af5d1677932c9b6defd32330.jpg'
l1 = 'U.S.-Coins-Dataset---A.Tatham-5/train/labels/0e1f9578-20220629_181429_jpg.rf.3a8a6299af5d1677932c9b6defd32330.txt'
l1voc = 'U.S. Coins Dataset - A.Tatham.v5i.voc/train/0e1f9578-20220629_181429_jpg.rf.3a8a6299af5d1677932c9b6defd32330.xml'
l1coco = 'U.S. Coins Dataset - A.Tatham.v5i.coco/train/_annotations.coco.json'


i2 = 'data/pascal_voc/images/VOCdevkit/VOC2007/JPEGImages/000001.jpg'
l2 = 'data/pascal_voc/images/VOCdevkit/VOC2007/Annotations/000001.xml'

img = cv2.imread(i1, cv2.COLOR_BGR2RGB)

f = open(l1)

# data = json.load(f)
yolo_labels = f.readlines()
f.close()
img_w = img.shape[1]
img_h = img.shape[0]


import xml.etree.ElementTree as ET

with open(l1voc) as f :
    tree = ET.parse(f)
    root = tree.getroot()


objs = root.findall('object')

voc_labels = []
for c in objs:
    name = c.find("name").text
    xmin = c.find("bndbox").find("xmin").text
    xmax = c.find("bndbox").find("xmax").text
    ymin = c.find("bndbox").find("ymin").text
    ymax = c.find("bndbox").find("ymax").text
    temp11 = [name, xmin, xmax, ymin, ymax]
    voc_labels.append(temp11)
    # print(c.tag, c.attrib)

f = open(l1coco)

data = json.load(f)
# yolo_labels = f.readlines()
f.close()
# print(voc_labels)
# xml_doc = xml.dom.minidom.parse(l1voc)
ii = data['images']
aa = data['annotations']
look_for = '3a8a6299af5d1677932c9b6defd32330'
for id, i in enumerate(ii):
    f_name = i['file_name']
    if look_for in f_name:
        # print(id)
        # print(i)
        the_id = id


coco_labels = []
for a in aa:
    iid = a['image_id']
    if iid == the_id:
        ca_id = a['category_id']
        bbox = a['bbox']
        temp11 = [ca_id]+bbox
        coco_labels.append(temp11)

print(yolo_labels)
print(voc_labels)
print(coco_labels)

# for coco in coco_labels:
#     cate = coco[0]
#     bbox = coco[1:]
#     [x, y, width, height] = bbox
#     x_width = x + width
#     y_height = y + height
#     cv2.rectangle(img, (x, y), (x_width, y_height), color=(255,0,0), thickness=2)
#     pass

# for voc in voc_labels:
#     cate = voc[0]
#     xmin = int(voc[1])
#     xmax = int(voc[2])
#     ymin = int(voc[3])
#     ymax = int(voc[4])
#     cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color=(255,0,0), thickness=2)

img_w
img_h
for yoo in yolo_labels:
    yolo = yoo.split()
    cate = int(yolo[0])
    x_center_norm = float(yolo[1])
    y_center_norm = float(yolo[2])
    width_norm = float(yolo[3])
    height_norm = float(yolo[4])
    x_center = int(x_center_norm * img_w)
    y_center = int(y_center_norm * img_h)
    width = int(width_norm * img_w)
    height = int(height_norm * img_h)

    half_w = width/2
    half_h = height/2

    xmin = int(x_center - half_w)
    xmax = int(x_center + half_w)
    ymin = int(y_center - half_h)
    ymax = int(y_center + half_h)
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color=(255,0,0), thickness=2)




# cv2.imshow("hello", img)
img = img
print()
cv2.rectangle(img, (x, y), (x_width, y_height), color=(255,0,0), thickness=2)
cv2.rectangle(img, (dx, dy), (dx_width, dy_height), color=(0,255,0), thickness=2)
# img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
cv2.imwrite(save_image_path, img)
shutil.copy2(image_path, save_folder)


# f = open(os.path.join(current_dir, path))

# data = json.load(f)
# f.close()


ii = data['images']
aa = data['annotations']

disease_idx = []

for i in range(len(aa)):
    if aa[i]['diseases_exist']:
        disease_idx.append(i)



save_root = 'temp-disease'
save_folder = os.path.join(current_dir, save_root)

if not os.path.exists(save_folder):
    os.makedirs(save_folder)
else:
    shutil.rmtree(save_folder)           # Removes all the subdirectories!
    os.makedirs(save_folder)


def showme(idx):
    
    image_name = ii[idx]['file_name']

    image_name = image_name[2:]
    image_bbox_name = image_name[:-4] + "_bbox" + image_name[-4:]
    bbox = aa[idx]['bbox']
    x,y = bbox[0], bbox[1]
    x_width, y_height = x + bbox[2], y + bbox[3]

    disease_bbox = aa[idx]['diseases_bbox']
    dx,dy = disease_bbox[0], disease_bbox[1]
    dx_width, dy_height = dx + disease_bbox[2], dy + disease_bbox[3]


    dataset_root = 'dtset1'
    image_path = os.path.join(current_dir, dataset_root, image_name)

    
    save_image_path = os.path.join(save_folder, image_bbox_name)

    img = cv2.imread(image_path, cv2.COLOR_BGR2RGB)
    cv2.rectangle(img, (x, y), (x_width, y_height), color=(255,0,0), thickness=2)
    cv2.rectangle(img, (dx, dy), (dx_width, dy_height), color=(0,255,0), thickness=2)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(save_image_path, img)
    shutil.copy2(image_path, save_folder)

# showme(2)

len_ = len(ii)
idx_list = disease_idx
import random
random.shuffle(idx_list)

for i in range(10):
    showme(idx_list[i])