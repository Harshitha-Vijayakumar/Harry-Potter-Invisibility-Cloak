import cv2
import numpy as np
import time

print(cv2.__version__)

time.sleep(1)
count = 0
background = 0

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera!")

for i in range(60): 
    return_val, background = cap.read() 
    if return_val == False : 
        continue 
  
background = np.flip(background, axis = 1)

while cap.isOpened(): 
    ret_val, frame = cap.read()
    if not ret_val:
        break
    count = count + 1
    frame = np.flip(frame, axis=1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Add chosen color of the "cloak" (Black in this case)
    lower_black = np.array([0, 0, 0])       
    upper_black = np.array([180, 255, 50])

    mask1 = cv2.inRange(hsv, lower_black, upper_black)

    # Removing noise
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations=1)
    mask2 = cv2.bitwise_not(mask1)

    fg = cv2.bitwise_and(frame, frame, mask=mask2)
    bg = cv2.bitwise_and(background, background, mask=mask1)
    res = cv2.addWeighted(bg, 1, fg, 1, 0)
    cv2.imshow("Invisible", res)
    k = cv2.waitKey(10) 
    if k == 27: 
        break

cap.release()
cv2.destroyAllWindows()