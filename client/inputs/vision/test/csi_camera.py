import cv2 as cv

def video_demo():
    capture=cv.VideoCapture(0)
    while True :
        ref,frame=capture.read()
        cv.imshow("1",frame)
        c= cv.waitKey(30) & 0xff
        if c==27:
            capture.release()
            break
video_demo()
cv.waitKey()
cv.destroyAllWindows()
