import cv2 #opencv
import time #delay
import imutils #resize

cam =cv2.VideoCapture(0) #cam id
time.sleep(1)

FirstFrame=None
area = 500

while True:
    _,img = cam.read() #read from the camera
    text = "Normal"
    img= imutils.resize(img, width=1000) #resize
    graying=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #color 2 gray scale img
    gaussian=cv2.GaussianBlur(graying,(21,21),0) #Smoothened
    if FirstFrame is None:
            FirstFrame = gaussian #capturing the first frame
            continue
    imgDuff=cv2.absdiff(FirstFrame,gaussian) #absolute difference
    thresh=cv2.threshold(imgDuff,25,255,cv2.THRESH_BINARY)[1]
    thresh=cv2.dilate(thresh,None,iterations=2) #left overs- erotion or dilation

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, #make Complete contours
            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
            if cv2.contourArea(c) < area: #make full area
                    continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Moving Object detected"
    print(text)
    cv2.putText(img, text, (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2) 
   

    cv2.imshow("cameraFeed",img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    
cam.release()
cv2.destroyAllWindows() 