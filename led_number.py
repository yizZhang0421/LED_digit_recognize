import cv2
img=cv2.imread('66274.jpg')
gray=img[:, :, 0]
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
binary = cv2.Canny(blurred, 10, 100)

(cnts, _) = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
rectangles=dict()
for contour in cnts:
    (x,y,w,h) = cv2.boundingRect(contour)
    rectangles[w*h]=(x,y,w,h)
rectangles={k:rectangles[k] for k in sorted(rectangles.keys())}

keys=[i for i in rectangles.keys()]
for i in range(len(keys)-1, -1, -1):
    rect=rectangles[keys[i]]
    if rect[2]/rect[3]>=0.9:
        screen_rect = rect
        break
(x,y,w,h)=screen_rect
test=img[y:y+h+1, x:x+w+1]

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img
test = increase_brightness(test, 100)
test = cv2.cvtColor(test , cv2.COLOR_BGR2GRAY)
ret2, binary= cv2.threshold(test, 130, 255, cv2.THRESH_BINARY)
# 統一高度734以便抓數字大小
test=cv2.resize(test, (round((734*test.shape[1])/test.shape[0]), 734), interpolation=cv2.INTER_CUBIC)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9, 9))
binary = cv2.dilate(binary, kernel)
binary = cv2.erode(binary, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(11, 19))
for_bounding = cv2.erode(binary, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9, 9))
binary = cv2.erode(binary, kernel)

def is_bar(mat):
    return True if (mat == 0).sum()>(mat.shape[0]*mat.shape[1]/2) else False
def get_value(digit_box, binary_mat):
    result=''
    (x,y,w,h)=digit_box
    if w<=72:
        result+='1'
    else:
        bar_width=40
        crop=binary_mat[y:(y+h)-1, x:(x+w)-1]
        top=is_bar(crop[0:bar_width, 0:crop.shape[1]])
        upper_left=is_bar(crop[0:round(crop.shape[0]/2), 0:bar_width])
        upper_right=is_bar(crop[0:round(crop.shape[0]/2), crop.shape[1]-bar_width+1:crop.shape[1]])
        center=is_bar(crop[round(crop.shape[0]/2)-round(bar_width/2):round(crop.shape[0]/2)+round(bar_width/2), 0:crop.shape[1]])
        lower_left=is_bar(crop[round(crop.shape[0]/2):crop.shape[0], 0:bar_width])
        lower_right=is_bar(crop[round(crop.shape[0]/2):crop.shape[0], crop.shape[1]-bar_width+1:crop.shape[1]])
        bottom=is_bar(crop[crop.shape[0]-bar_width:crop.shape[0], 0:crop.shape[1]])
        if top and upper_left==False and upper_right and center and lower_left and lower_right==False and bottom:
            result+='2'
        elif top and upper_left==False and upper_right and center and lower_left==False and lower_right and bottom:
            result+='3'
        elif top==False and upper_left and upper_right and center and lower_left==False and lower_right and bottom==False:
            result+='4'
        elif top and upper_left and upper_right==False and center and lower_left==False and lower_right and bottom:
            result+='5'
        elif top and upper_left and upper_right==False and center and lower_left and lower_right and bottom:
            result+='6'
        elif top and upper_left==False and upper_right and center==False and lower_left==False and lower_right and bottom==False:
            result+='7'
        elif top and upper_left and upper_right and center and lower_left and lower_right and bottom:
            result+='8'
        elif top and upper_left and upper_right and center and lower_left==False and lower_right and bottom:
            result+='9'
        elif top and upper_left and upper_right and center==False and lower_left and lower_right and bottom:
            result+='0'
    return result


# bounding box並過濾、加工
(cnts, _) = cv2.findContours(for_bounding, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
digit_boxes=[]
for contour in cnts:
    (x,y,w,h) = cv2.boundingRect(contour)
    if h>=179 and h<=506:
        digit_boxes.append((x,y,w,h))

digit_lines=dict()
for (x,y,w,h) in digit_boxes:
    if len(digit_lines)==0:
        digit_lines[y+round(h/2)-1]=[(x,y,w,h)]
    else:
        center=y+round(h/2)-1
        finded=False
        for i in digit_lines.keys():
            if abs(center-i)<=72:
                old_key=i
                old_list=digit_lines[i]
                old_list.append((x,y,w,h))
                del digit_lines[i]
                digit_lines[round((i+center)/2)]=old_list
                finded=True
                break
        if finded==False:
            digit_lines[y+round(h/2)-1]=[(x,y,w,h)]
digit_lines={key:digit_lines[key] for key in sorted(digit_lines)}
for line_key in digit_lines.keys():
    line_list=digit_lines[line_key]
    line_list={box[0]:box for box in line_list}
    line_list=[line_list[key] for key in sorted(line_list)]
    digit_lines[line_key]=line_list

for y_key in digit_lines:
    result=''
    for box in digit_lines[y_key]:
        digit_recog=get_value(box, binary)
        result+=digit_recog
    print(result)