import handTrackingModule as htm
import mouse
import cv2
from screeninfo import get_monitors

monitor = [monitor for monitor in get_monitors() if monitor.is_primary][0]
monitor_width = monitor.width
monitor_height = monitor.height
screen_mid_x = monitor_width / 2
screen_mid_y = monitor_height / 2

cap = cv2.VideoCapture(0)
tracker = htm.handTracker()

capture_width  = cap.get(3)
capture_height = cap.get(4)

INDEX_FINGER = [5, 8] # MCP, TIP

while True:
    success, image = cap.read()
    image = tracker.handsFinder(image)
    lmList = tracker.positionFinder(image)
    
    if len(lmList) != 0:
        # Get the coordinates of the index finger
        x1, y1 = lmList[INDEX_FINGER[0]][1:]
        x2, y2 = lmList[INDEX_FINGER[1]][1:]

        # dx = x2 - x1
        # dy = y2 - y1

        # mouse_x = screen_mid_x - dx # - due to flipped x axis
        # mouse_y = screen_mid_y + dy

        # Get the mouse_x by mapping the x1 to the screen width
        mouse_x = int(monitor_width - x1 * (monitor_width / capture_width)) # due to flipped x axis
        mouse_y = int(y1 * (monitor_height / capture_height))
        
        

        mouse.move(mouse_x, mouse_y, duration=0.1)

    image_flip = cv2.flip(image, 1)
    cv2.imshow("Video",image_flip)
    cv2.waitKey(1)