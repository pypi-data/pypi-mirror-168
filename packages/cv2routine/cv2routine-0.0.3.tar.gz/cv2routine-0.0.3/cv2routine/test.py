import transform
import figures
import cv2

# videocapture from 192.168.88.228 login admin password maser000
# cap = cv2.VideoCapture("rtsp://admin:master000@192.168.88.229:554")
# ret, frame = cap.read()
frame = cv2.imread('contours.png')
img = frame.copy()
img2 = frame.copy()
img3 = frame.copy()


#1 min area = 1000
# dilated1, dil1 = figures.draw_rect_frame(img, (173, 82, 213), (180, 235, 255), "", 0, 0, 1000, False, (30, 255, 100))
# dilated2, dil2 = figures.draw_rect_frame(img2, (56, 194, 162), (80, 229, 229), "", 0, 0, 1000, False, (30, 255, 100))
# dilated3, dil3 = figures.draw_rect_frame(img3, (118, 194, 177), (175, 255, 255), "", 0, 0, 1000, False, (30, 255, 100))

#2 min area = 10
# dilated1, dil1 = figures.draw_rect_frame(img, (173, 82, 213), (180, 235, 255), "", 0, 0, 10, False, (30, 255, 100))
# dilated2, dil2 = figures.draw_rect_frame(img2, (56, 194, 162), (80, 229, 229), "", 0, 0, 10, False, (30, 255, 100))
# dilated3, dil3 = figures.draw_rect_frame(img3, (118, 194, 177), (175, 255, 255), "", 0, 0, 10, False, (30, 255, 100))

#3 Only max = True
# dilated1, dil1 = figures.draw_rect_frame(img, (173, 82, 213), (180, 235, 255), "", 0, 0, 10, True, (30, 255, 100))
# dilated2, dil2 = figures.draw_rect_frame(img2, (56, 194, 162), (80, 229, 229), "", 0, 0, 10, True, (30, 255, 100))
# dilated3, dil3 = figures.draw_rect_frame(img3, (118, 194, 177), (175, 255, 255), "", 0, 0, 10, True, (30, 255, 100))

#4 Text + color
# dilated1, dil1 = figures.draw_rect_frame(img, (173, 82, 213), (180, 235, 255), "Red", 0, 0, 10, True, (255, 255, 0))
# dilated2, dil2 = figures.draw_rect_frame(img2, (56, 194, 162), (80, 229, 229), "Green", 0, 0, 10, True, (255, 0, 255))
# dilated3, dil3 = figures.draw_rect_frame(img3, (118, 194, 177), (175, 255, 255), "Blue", 0, 0, 10, True, (0, 255, 255))

#4 Complex
dilated1, dil1 = figures.draw_rect_frame(img, (173, 82, 213), (180, 235, 255), "Red", 1, 0, 10, False, (255, 255, 0))
dilated2, dil2 = figures.draw_rect_frame(img2, (173, 82, 213), (180, 235, 255), "Red", 2, 0, 100, True, (255, 255, 0))
dilated3, dil3 = figures.draw_rect_frame(img3, (173, 82, 213), (180, 235, 255), "Red", 4, 0, 1000, False, (255, 255, 0))

#
cv2.imshow('Initial', frame)
cv2.imshow('1 - Red', dilated1)
cv2.imshow('1 - Red (dil)', dil1)
cv2.imshow('2 - Red', dilated2)
cv2.imshow('2 - Red (dil)', dil2)
cv2.imshow('3 - Red', dilated3)
cv2.imshow('3 - Red (dil)', dil3)

cv2.waitKey(0)
cv2.destroyAllWindows()
