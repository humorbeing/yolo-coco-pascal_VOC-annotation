import cv2


image = '0e1f9578-20220629_181429_jpg.rf.3a8a6299af5d1677932c9b6defd32330.jpg'

# # #  ---------------

import json

coco_path = '_annotations.coco.json'

f = open(coco_path)
data = json.load(f)
f.close()

ii = data['images']
aa = data['annotations']
look_for = '0e1f9578-20220629_181429_jpg.rf.3a8a6299af5d1677932c9b6defd32330.jpg'

for i in ii:
    f_name = i['file_name']
    if look_for in f_name:        
        image_id = i['id']


coco_labels = []

for a in aa:
    iid = a['image_id']
    if iid == image_id:
        ca_id = a['category_id']
        name = data['categories'][ca_id]['name']
        bbox = a['bbox']
        temp11 = [name]+bbox
        coco_labels.append(temp11)

img = cv2.imread(image, cv2.COLOR_BGR2RGB)
for coco in coco_labels:
    category = coco[0]
    bbox = coco[1:]
    [xmin, ymin, width, height] = bbox
    xmax = xmin + width
    ymax = ymin + height
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color=(255,255,0), thickness=3)
    cv2.putText(img, category, (xmin, ymin-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3, cv2.LINE_AA) 

img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)    
cv2.imwrite("coco.jpg", img)

# # # ----------------

import xml.etree.ElementTree as ET

pascal_voc_path = '0e1f9578-20220629_181429_jpg.rf.3a8a6299af5d1677932c9b6defd32330.xml'

with open(pascal_voc_path) as f :
    tree = ET.parse(f)
    root = tree.getroot()

objs = root.findall('object')

pascal_voc_labels = []
for c in objs:
    name = c.find("name").text
    xmin = c.find("bndbox").find("xmin").text
    xmax = c.find("bndbox").find("xmax").text
    ymin = c.find("bndbox").find("ymin").text
    ymax = c.find("bndbox").find("ymax").text
    temp11 = [name, xmin, xmax, ymin, ymax]
    pascal_voc_labels.append(temp11)


img = cv2.imread(image, cv2.COLOR_BGR2RGB)
for voc in pascal_voc_labels:
    category = voc[0]
    xmin = int(voc[1])
    xmax = int(voc[2])
    ymin = int(voc[3])
    ymax = int(voc[4])
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color=(255,255,0), thickness=3)
    cv2.putText(img, category, (xmin, ymin-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3, cv2.LINE_AA) 

img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)    
cv2.imwrite("pascal-voc.jpg", img)


# # # # ----------------------------

yolo_path = '0e1f9578-20220629_181429_jpg.rf.3a8a6299af5d1677932c9b6defd32330.txt'

f = open(yolo_path)
yolo_labels = f.readlines()
f.close()

img = cv2.imread(image, cv2.COLOR_BGR2RGB)
img_height = img.shape[0]
img_width = img.shape[1]
for raw_data in yolo_labels:
    yolo = raw_data.split()
    ca_id = int(yolo[0])
    x_center_norm = float(yolo[1])
    y_center_norm = float(yolo[2])
    width_norm = float(yolo[3])
    height_norm = float(yolo[4])
    x_center = int(x_center_norm * img_width)
    y_center = int(y_center_norm * img_height)
    width = int(width_norm * img_width)
    height = int(height_norm * img_height)

    half_w = width/2
    half_h = height/2

    xmin = int(x_center - half_w)
    xmax = int(x_center + half_w)
    ymin = int(y_center - half_h)
    ymax = int(y_center + half_h)
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color=(255,255,0), thickness=3)
    cv2.putText(img, str(ca_id), (xmin, ymin-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3, cv2.LINE_AA) 

img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)    
cv2.imwrite("yolo.jpg", img)