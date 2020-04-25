import cv2
import numpy as np

refPt1 = []
refPt2 = []
control = []

#to check if a given triangle resides inside a rectangle or not.
def contains(rect, point):
    if (point[0] < rect[0]):
        return False
    elif (point[1] < rect[1]):
        return False
    elif (point[0] > rect[2]):
        return False
    elif (point[1] > rect[3]):
        return False
    return True

#FUnction To draw Delaungy's Triangle
def draw_delaunay(img, subdiv, color):
    triangle = subdiv.getTriangleList()
    size = img.shape

    r = (0, 0, size[1], size[0])

    for t in triangle:
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])
        if (contains(r, pt1) and contains(r, pt2) and contains(r, pt3)):
            cv2.line(img, pt1, pt2, color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt2, pt3, color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt3, pt1, color, 1, cv2.LINE_AA, 0)

#Mouse click for Bush Image
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow('image', img)
        mouseX = x
        mouseY = y
        refPt1.append(x)
        refPt2.append(y)
    # control.append((x, y))


# print((mouseX,mouseY))

#Mouse Click for Clinton Image
def click_event_2(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img2, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow('image2', img2)
        mouseX = x
        mouseY = y
        refPt21.append(x)
        refPt22.append(y)

#To get intermediate cordinates for triangle t1 and t2
def intermediate_points(p,t1,t2):
    inter_points = []
    pts1 = (t1[0], t1[1])
    pts2 = (t1[2], t1[3])
    pts3 = (t1[4], t1[5])

    ptd1 = (t2[0], t2[1])
    ptd2 = (t2[2], t2[3])
    ptd3 = (t2[4], t2[5])

    xk1 = (((frames-p)/(frames))*pts1[0] + ((p/frames))*ptd1[0])
    yk1 = (((frames-p)/(frames))*pts1[1] + ((p/frames))*ptd1[1])
    inter_points.append((int(xk1), int(yk1)))

    xk2 = (((frames - p) / (frames)) * pts2[0] + ((p / frames)) * ptd2[0])
    yk2 = (((frames - p) / (frames)) * pts2[1] + ((p / frames)) * ptd2[1])
    inter_points.append((int(xk2), int(yk2)))

    xk3 = (((frames - p) / (frames)) * pts3[0] + ((p / frames)) * ptd3[0])
    yk3 = (((frames - p) / (frames)) * pts3[1] + ((p / frames)) * ptd3[1])
    inter_points.append((int(xk3), int(yk3)))

    return inter_points
#returns the area of a triangle
def area(x1, x2, x3, y1, y2, y3):
    return abs((x1*(y2-y3) + x2*(y3-y1)+ x3*(y1-y2))/2.0)

#to check weather the goven point lies inside the triangle or not.
def is_inside(x1, x2, x3, y1, y2, y3, xk, yk):
    a=area(x1,x2,x3,y1,y2,y3)
    b=area(xk,x1,x2,yk,y1,y2)
    c=area(xk,x1,x3,yk,y1,y3)
    d=area(xk,x2,x3,yk,y2,y3)
    if(a==b+c+d):
        return 1
    else:
        return 0
#To get the value of alpha and beta with given cordinates.
def feature_points(x1, x2, x3, y1, y2, y3, x, y):
    alpha = (((x3 - x1) * (y - y1)) - ((y3 - y1) * (x - x1))) / (((y2 - y1) * (x3 - x1)) - ((x2 - x1) * (y3 - y1)))
    beta = (((x2 - x1) * (y - y1)) - ((y2 - y1) * (x - x1))) / (((x2 - x1) * (y3 - y1)) - ((y2 - y1) * (x3 - x1)))
    return alpha, beta


#Here face Morphing happens for every triangular Region.
def face_morph(p, t1, t2, n,img_Morph):
    inter_points = intermediate_points(p,t1,t2)
    x1, x2, x3 = inter_points[0][0], inter_points[1][0], inter_points[2][0]
    y1, y2, y3 = inter_points[0][1], inter_points[1][1], inter_points[2][1]

    pts1 = (t1[0], t1[1])
    pts2 = (t1[2], t1[3])
    pts3 = (t1[4], t1[5])

    ptd1 = (t2[0], t2[1])
    ptd2 = (t2[2], t2[3])
    ptd3 = (t2[4], t2[5])
    #img_Morph = np.zeros((img_orig.shape[0], img_orig.shape[1], 3), np.uint8)

    for i in range(row):
        for j in range(col):
            if is_inside(x1, x2, x3, y1, y2, y3, i, j) == 1:
                alpha, beta = feature_points(x1, x2, x3, y1, y2, y3, i, j)

                src_x = alpha * (pts2[0] - pts1[0]) + beta * (pts3[0] - pts1[0]) + pts1[0]
                src_y = alpha * (pts2[1] - pts1[1]) + beta * (pts3[1] - pts1[1]) + pts1[1]

                des_x = alpha * (ptd2[0] - ptd1[0]) + beta * (ptd3[0] - ptd1[0]) + ptd1[0]
                des_y = alpha * (ptd2[1] - ptd1[1]) + beta * (ptd3[1] - ptd1[1]) + ptd1[1]
                try:
                    img_Morph[i][j] = ((frames - p) / frames) * (img_orig[int(src_x)][int(src_y)]) + (p / frames) * (img2_orig[int(des_x)][int(des_y)])
                except:
                    img_Morph[i][j]=img2_orig[i][j]
    cv2.imshow("Morphing", img_Morph1 + img_Morph)
    if n < 10:
        cv2.imwrite("Morphed_Image_000" + str(n) + ".jpg", img_Morph1 + img_Morph)
    else:
        cv2.imwrite("Morphed_Image_00" + str(n) + ".jpg", img_Morph1 + img_Morph)
    cv2.waitKey(1)

#Bush Image is Read
img = cv2.imread(r'/home/abhay/Desktop/Bush.jpg')
img_orig = img.copy()
row = img.shape[0]
col = img.shape[1]

print(row, col)
cv2.namedWindow("image")
## Mouse clicks are handled here.
cv2.setMouseCallback("image", click_event)

cv2.imshow("image", img)

cv2.waitKey(0)
#stores control point of Bush Image.
control = [(refPt1[0], refPt2[0]), (refPt1[1], refPt2[1]), (refPt1[2], refPt2[2])]
control.append((0, 0))
control.append((0, col-1))
control.append((row-1, 0))
control.append((row-1, col-1))
# print(control)

refPt21 = []
refPt22 = []

#Clinton is Read
img2 = cv2.imread(r'/home/abhay/Desktop/Clinton.jpg')
img2_orig = img2.copy()
row2 = img2.shape[0]
col2 = img2.shape[1]

img2_orig = img2.copy()
cv2.namedWindow("image2")
cv2.setMouseCallback("image2", click_event_2)

cv2.imshow("image2", img2)
cv2.waitKey(0)

#stores control points for Clinton
control2 = [(refPt21[0], refPt22[0]), (refPt21[1], refPt22[1]), (refPt21[2], refPt22[2])]
control2.append((0, 0))
control2.append((0, col2-1))
control2.append((row2-1, 0))
control2.append((row2-1, col2-1))

#Holds list of cordinates of triangle for bush
triangle_list1 = []
rect = (0, 0, row, col)
subdiv = cv2.Subdiv2D(rect)
animate = True
for p in control:
    subdiv.insert(p)
    triangle_list1 = subdiv.getTriangleList()
    if animate:
        img_copy = img_orig.copy()
        draw_delaunay(img_copy, subdiv, (255, 255, 255))
        cv2.imshow("Delaunays's Triangle", img_copy)
        cv2.waitKey(300)
#Delaunays Triangle is drawn
draw_delaunay(img, subdiv, (255, 255, 255))

for p in control:
    cv2.circle(img, p, 2, (255, 0, 0), -1, cv2.LINE_AA, 0)

cv2.destroyAllWindows()
cv2.imshow("Triangulated Image1", img);
cv2.waitKey(0)
#Holds list of cordinates of triangle for Clinton
triangle_list2 = []
rect = (0, 0, row, col)
subdiv = cv2.Subdiv2D(rect)
animate = True
for p in control2:
    subdiv.insert(p)
    triangle_list2 = subdiv.getTriangleList()
    if animate:
        img_copy = img2_orig.copy()
        draw_delaunay(img_copy, subdiv, (255, 255, 255))
        cv2.imshow("Delaunays's Triangle", img_copy)
        cv2.waitKey(300)
##Delaunys Drawn on clinton
draw_delaunay(img2, subdiv, (255, 255, 255))

for p in control2:
    cv2.circle(img2, p, 2, (255, 0, 0), -1, cv2.LINE_AA, 0)

cv2.destroyAllWindows()
n=0
frames = 10
#Varaible that will store the final Image
img_Morph1 = np.zeros((img_orig.shape[0],img_orig.shape[1],3), np.uint8)

# We choose every triangle one by one and allpy moring to it..
for i in range(len(triangle_list1)):
    for j in range(1, frames):
        img_Morph = np.zeros((img_orig.shape[0], img_orig.shape[1], 3), np.uint8)
        face_morph(j,triangle_list1[i],triangle_list2[i],n,img_Morph)
        n+=1
    img_Morph1 = img_Morph1 + img_Morph

cv2.imshow("Morphed Image",img_Morph1)
cv2.imshow("Triangulated Image1", img)
cv2.imshow("Triangulated Image2", img2);
cv2.imwrite("Triangulated_Image1.jpg", img)
cv2.imwrite("Triangulated_Image2.jpg", img2)
cv2.imwrite("Final_Morphed.jpg",img_Morph1)
cv2.waitKey(0)
